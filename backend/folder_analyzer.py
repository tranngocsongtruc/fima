"""
Deep folder structure analysis using Claude (Anthropic)
This provides comprehensive analysis of existing file organization patterns
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple
from anthropic import Anthropic
from config import settings
import os


class FolderAnalyzer:
    """
    Analyzes existing folder structures and provides optimization suggestions
    Uses Claude for deep reasoning about file organization patterns
    """
    
    def __init__(self):
        """Initialize Claude client"""
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        # ⭐ THIS IS WHERE THE CLAUDE API KEY IS USED ⭐
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
    
    def scan_directory_structure(self, root_path: Path, max_depth: int = 4) -> Dict:
        """
        Scan directory structure and build a tree representation
        
        Args:
            root_path: Root directory to scan
            max_depth: Maximum depth to traverse
            
        Returns:
            Dictionary representing folder structure with file counts
        """
        structure = {
            'path': str(root_path),
            'name': root_path.name,
            'type': 'directory',
            'children': [],
            'file_count': 0,
            'total_size': 0
        }
        
        try:
            items = list(root_path.iterdir())
            
            for item in items:
                # Skip hidden files and system folders
                if item.name.startswith('.'):
                    continue
                
                if item.is_file():
                    structure['file_count'] += 1
                    try:
                        structure['total_size'] += item.stat().st_size
                    except:
                        pass
                
                elif item.is_dir() and max_depth > 0:
                    child_structure = self.scan_directory_structure(item, max_depth - 1)
                    structure['children'].append(child_structure)
                    structure['file_count'] += child_structure['file_count']
                    structure['total_size'] += child_structure['total_size']
        
        except PermissionError:
            structure['error'] = 'Permission denied'
        except Exception as e:
            structure['error'] = str(e)
        
        return structure
    
    def analyze_organization_patterns(self, structure: Dict) -> Dict:
        """
        Use Claude to analyze folder organization patterns
        
        Returns insights about:
        - Current organization style
        - Strengths and weaknesses
        - Optimization opportunities
        """
        # Build a concise representation for Claude
        summary = self._build_structure_summary(structure)
        
        prompt = f"""Analyze this file/folder organization structure and provide insights:

{summary}

Please analyze:
1. What organizational patterns do you observe? (e.g., by date, by project, by type, mixed)
2. What are the strengths of the current organization?
3. What are the weaknesses or pain points?
4. How consistent is the organization?
5. Are there redundant or poorly organized areas?

Respond in JSON format:
{{
    "patterns_observed": ["list of patterns"],
    "organization_style": "description",
    "strengths": ["list of strengths"],
    "weaknesses": ["list of weaknesses"],
    "consistency_score": 0.0-1.0,
    "pain_points": ["specific issues"],
    "overall_assessment": "brief summary"
}}
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=settings.max_tokens,
                temperature=settings.ai_temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            # Try to find JSON in the response
            if '{' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                return {'error': 'Could not parse response'}
                
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            return {'error': str(e)}
    
    def generate_optimization_suggestions(self, structure: Dict, analysis: Dict) -> Dict:
        """
        Generate specific optimization suggestions using Claude
        
        Returns:
        - Suggested folder structure
        - Migration plan
        - Expected benefits
        """
        summary = self._build_structure_summary(structure)
        
        prompt = f"""Based on this folder structure and analysis, suggest an optimized organization:

CURRENT STRUCTURE:
{summary}

ANALYSIS:
{json.dumps(analysis, indent=2)}

Please suggest:
1. An improved folder hierarchy
2. Naming conventions to follow
3. Which files/folders should be moved where
4. Which empty or redundant folders should be archived
5. Expected benefits of the reorganization

Respond in JSON format:
{{
    "suggested_structure": {{
        "root_folders": ["folder1", "folder2"],
        "hierarchy_example": "detailed example path",
        "naming_conventions": ["convention1", "convention2"]
    }},
    "migration_plan": [
        {{
            "action": "move|create|archive",
            "source": "current/path",
            "destination": "new/path",
            "reason": "explanation"
        }}
    ],
    "folders_to_archive": ["folder/path"],
    "expected_benefits": ["benefit1", "benefit2"],
    "estimated_time": "time estimate",
    "risk_level": "low|medium|high"
}}
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=settings.ai_temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text
            if '{' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                return {'error': 'Could not parse response'}
                
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return {'error': str(e)}
    
    def _build_structure_summary(self, structure: Dict, indent: int = 0) -> str:
        """Build a readable summary of folder structure"""
        lines = []
        prefix = "  " * indent
        
        name = structure.get('name', 'root')
        file_count = structure.get('file_count', 0)
        size_mb = structure.get('total_size', 0) / (1024 * 1024)
        
        lines.append(f"{prefix}📁 {name}/ ({file_count} files, {size_mb:.1f} MB)")
        
        # Add children (limit depth to avoid token overflow)
        if indent < 3:
            for child in structure.get('children', [])[:20]:  # Limit to 20 children
                lines.append(self._build_structure_summary(child, indent + 1))
        
        return "\n".join(lines)
    
    def perform_full_analysis(self, root_path: Path) -> Tuple[Dict, Dict, Dict]:
        """
        Perform complete analysis: scan, analyze, and suggest
        
        Returns:
            Tuple of (structure, analysis, suggestions)
        """
        print(f"📊 Scanning folder structure: {root_path}")
        structure = self.scan_directory_structure(root_path)
        
        print(f"🔍 Analyzing organization patterns...")
        analysis = self.analyze_organization_patterns(structure)
        
        print(f"💡 Generating optimization suggestions...")
        suggestions = self.generate_optimization_suggestions(structure, analysis)
        
        return structure, analysis, suggestions
    
    def compare_structures(self, old_structure: Dict, new_structure: Dict) -> Dict:
        """
        Compare old and new structures to generate a change report
        """
        prompt = f"""Compare these two folder structures and generate a change report:

OLD STRUCTURE:
{self._build_structure_summary(old_structure)}

NEW STRUCTURE:
{self._build_structure_summary(new_structure)}

Provide a summary of changes in JSON:
{{
    "files_moved": number,
    "folders_created": number,
    "folders_archived": number,
    "major_changes": ["change1", "change2"],
    "improvement_summary": "brief description"
}}
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            if '{' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                return {'error': 'Could not parse response'}
                
        except Exception as e:
            print(f"Error comparing structures: {e}")
            return {'error': str(e)}
