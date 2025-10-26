"""
AI-powered file classification using Claude (Anthropic)
Provides intelligent file categorization with high accuracy

Optionally routes requests through Lava API gateway for cost tracking
"""
import os
import json
import mimetypes
from pathlib import Path
from typing import Dict, Optional, Tuple
from anthropic import Anthropic
from config import settings
from lava_integration import lava_gateway, use_lava_if_available


class AIFileClassifier:
    """
    Intelligent file classification using Claude (Anthropic)
    
    Claude provides accurate categorization and context-aware folder suggestions
    """
    
    def __init__(self):
        """Initialize Claude client"""
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        self.use_lava = use_lava_if_available()
    
    def scan_existing_folders(self) -> str:
        """Scan user's existing folder structure to find ideal locations"""
        home = Path.home()
        relevant_folders = []
        
        # Scan Desktop for course folders
        desktop = home / "Desktop"
        if desktop.exists():
            for item in desktop.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Look for course-related folders
                    if any(keyword in item.name.lower() for keyword in ['cal', 'cs', 'eecs', 'math', 'eng']):
                        relevant_folders.append(str(item.relative_to(home)))
                        # Check subdirectories
                        for subitem in item.iterdir():
                            if subitem.is_dir() and not subitem.name.startswith('.'):
                                relevant_folders.append(str(subitem.relative_to(home)))
        
        # Scan Documents
        documents = home / "Documents"
        if documents.exists():
            for item in documents.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    relevant_folders.append(str(item.relative_to(home)))
        
        if relevant_folders:
            return "\n".join(f"- {folder}" for folder in relevant_folders[:20])  # Limit to 20
        return "No existing folders found"
    
    def extract_file_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from file for classification"""
        try:
            stat = file_path.stat()
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = "application/octet-stream"
            
            metadata = {
                'filename': file_path.name,
                'extension': file_path.suffix.lower(),
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'mime_type': mime_type,
                'created_at': stat.st_ctime,
                'modified_at': stat.st_mtime
            }
            
            # Try to extract text from PDFs for better classification
            if file_path.suffix.lower() == '.pdf':
                metadata['content_preview'] = self._extract_pdf_text(file_path)
            
            return metadata
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {'filename': file_path.name, 'extension': file_path.suffix}
    
    def _extract_pdf_text(self, file_path: Path, max_chars: int = None) -> str:
        """
        Extract first few characters from PDF for context
        Respects privacy settings
        """
        # Check privacy settings
        if not settings.extract_pdf_text:
            return ""
        
        if settings.privacy_mode == "strict":
            return ""
        
        # Use configured max_chars or default based on privacy mode
        if max_chars is None:
            if settings.privacy_mode == "balanced":
                max_chars = 200
            else:  # standard
                max_chars = settings.max_pdf_chars
        
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(file_path))
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()
                return text[:max_chars] if text else ""
        except Exception:
            return ""
        return ""
    
    def classify_file(self, file_path: Path) -> Tuple[Dict, float]:
        """
        Classify a file and determine its optimal folder location
        
        Returns:
            Tuple of (classification_result, confidence_score)
            
        Classification result includes:
        - category: homework, work, personal, receipt, media, etc.
        - suggested_path: folder hierarchy (e.g., uc_berkeley/fall_2025/cs170/homework)
        - reasoning: why this classification was chosen
        """
        metadata = self.extract_file_metadata(file_path)
        
        # Build prompt for Claude
        prompt = self._build_classification_prompt(metadata)
        
        # Log AI request if auditing is enabled
        if settings.log_ai_requests:
            self._log_ai_request(metadata)
        
        try:
            # Call Claude API for intelligent classification
            system_prompt = """You are an expert file organization assistant. 
Analyze files and suggest optimal folder structures.
Always respond in valid JSON format with these fields:
{
    "category": "homework|work|personal|receipt|media|document|code|other",
    "subcategory": "specific type",
    "suggested_path": "folder/hierarchy/path",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation",
    "metadata": {
        "school": "if applicable",
        "course": "if applicable", 
        "semester": "if applicable",
        "company": "if work-related",
        "project": "if applicable"
    }
}"""
            
            # Route through Lava if configured, otherwise direct to Claude
            if self.use_lava:
                try:
                    print("📊 Routing through Lava API gateway for cost tracking...")
                    response = lava_gateway.forward_claude_request(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        system=system_prompt,
                        max_tokens=settings.max_tokens,
                        temperature=settings.ai_temperature
                    )
                    # Lava returns the same format as Claude
                    content = response['content'][0]['text']
                except Exception as lava_error:
                    print(f"⚠️  Lava gateway failed, falling back to direct Claude API: {lava_error}")
                    # Fallback to direct Claude API
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=settings.max_tokens,
                        temperature=settings.ai_temperature,
                        system=system_prompt,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                    content = response.content[0].text
            else:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=settings.max_tokens,
                    temperature=settings.ai_temperature,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                content = response.content[0].text
            
            # Extract JSON from response
            if '{' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
            else:
                result = json.loads(content)
            
            confidence = result.get('confidence', 0.5)
            
            return result, confidence
            
        except Exception as e:
            print(f"Error classifying file: {e}")
            # Fallback to basic classification
            return self._fallback_classification(metadata), 0.3
    
    def _build_classification_prompt(self, metadata: Dict) -> str:
        """Build a detailed prompt for file classification"""
        # Scan existing folders
        existing_folders = self.scan_existing_folders()
        
        prompt = f"""Classify this file and suggest an optimal folder structure:

Filename: {metadata.get('filename', 'unknown')}
Extension: {metadata.get('extension', 'unknown')}
Size: {metadata.get('size_mb', 0)} MB
MIME Type: {metadata.get('mime_type', 'unknown')}
"""
        
        if 'content_preview' in metadata and metadata['content_preview']:
            prompt += f"\nContent Preview:\n{metadata['content_preview']}\n"
        
        prompt += f"""
IMPORTANT: The user has these existing folders:
{existing_folders}

RULES:
1. PREFER using existing folders when appropriate (e.g., if "Desktop/calundergrad/cs170" exists, use it for CS170 files)
2. If a suitable existing folder exists, use it instead of creating new folders
3. For course files, check if Desktop/calundergrad/[course_name] exists
4. Only suggest new folders if no existing folder is suitable

Examples:
- "hw08.pdf" for CS170 → If "Desktop/calundergrad/cs170" exists, suggest: Desktop/calundergrad/cs170/homework
- "receipt.pdf" → If "Documents/receipts" exists, use it; otherwise create: Documents/fima/receipts
- New course file → If no existing folder, create: Documents/fima/school/[course]/[category]

Analyze the filename, content, and existing folders to determine:
1. What type of file this is
2. Whether an existing folder is suitable
3. The optimal folder path (prefer existing folders!)
"""
        return prompt
    
    def _fallback_classification(self, metadata: Dict) -> Dict:
        """Fallback classification based on file extension"""
        ext = metadata.get('extension', '').lower()
        filename = metadata.get('filename', '').lower()
        
        # Simple rule-based classification
        if ext in ['.pdf', '.docx', '.doc', '.txt']:
            if 'hw' in filename or 'homework' in filename or 'assignment' in filename:
                return {
                    'category': 'homework',
                    'subcategory': 'assignment',
                    'suggested_path': 'school/homework',
                    'confidence': 0.6,
                    'reasoning': 'Detected homework-related keywords'
                }
            elif 'receipt' in filename or 'invoice' in filename:
                return {
                    'category': 'receipt',
                    'subcategory': 'financial',
                    'suggested_path': 'personal/receipts',
                    'confidence': 0.7,
                    'reasoning': 'Detected receipt/invoice keywords'
                }
            else:
                return {
                    'category': 'document',
                    'subcategory': 'general',
                    'suggested_path': 'documents',
                    'confidence': 0.5,
                    'reasoning': 'Generic document'
                }
        
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.heic']:
            return {
                'category': 'media',
                'subcategory': 'image',
                'suggested_path': 'media/images',
                'confidence': 0.8,
                'reasoning': 'Image file'
            }
        
        elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
            return {
                'category': 'media',
                'subcategory': 'video',
                'suggested_path': 'media/videos',
                'confidence': 0.8,
                'reasoning': 'Video file'
            }
        
        elif ext in ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css']:
            return {
                'category': 'code',
                'subcategory': 'source',
                'suggested_path': 'code/projects',
                'confidence': 0.7,
                'reasoning': 'Source code file'
            }
        
        else:
            return {
                'category': 'other',
                'subcategory': 'unknown',
                'suggested_path': 'misc',
                'confidence': 0.3,
                'reasoning': 'Unknown file type'
            }
    
    def _log_ai_request(self, metadata: Dict):
        """
        Log what data is being sent to AI for auditing
        Only logs if LOG_AI_REQUESTS=true in .env
        """
        import datetime
        from pathlib import Path
        
        log_dir = Path.home() / ".smart_file_organizer" / "audit_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"ai_requests_{datetime.date.today()}.log"
        
        with open(log_file, 'a') as f:
            timestamp = datetime.datetime.now().isoformat()
            f.write(f"\n[{timestamp}] AI Request:\n")
            f.write(f"  Filename: {metadata.get('filename', 'N/A')}\n")
            f.write(f"  Extension: {metadata.get('extension', 'N/A')}\n")
            f.write(f"  Size: {metadata.get('size_mb', 0)} MB\n")
            f.write(f"  MIME: {metadata.get('mime_type', 'N/A')}\n")
            
            if 'content_preview' in metadata and metadata['content_preview']:
                preview_len = len(metadata['content_preview'])
                f.write(f"  Content Preview: {preview_len} chars sent\n")
                f.write(f"  Preview: {metadata['content_preview'][:100]}...\n")
            else:
                f.write(f"  Content Preview: None (privacy mode: {settings.privacy_mode})\n")
            
            f.write(f"  Privacy Mode: {settings.privacy_mode}\n")
            f.write("-" * 60 + "\n")
    
    def batch_classify(self, file_paths: list[Path]) -> list[Tuple[Dict, float]]:
        """Classify multiple files efficiently"""
        results = []
        for file_path in file_paths:
            try:
                result = self.classify_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"Error classifying {file_path}: {e}")
                results.append((self._fallback_classification({'filename': file_path.name}), 0.3))
        return results
