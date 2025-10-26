"""
Real-time file system monitoring for Downloads folder
Detects new files and triggers AI classification
"""
import time
import asyncio
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from config import settings, get_downloads_folder
from ai_classifier import AIFileClassifier
from database import Database
from notification_manager import NotificationManager
import shutil


class DownloadHandler(FileSystemEventHandler):
    """Handles file system events in the Downloads folder"""
    
    def __init__(self, classifier: AIFileClassifier, db: Database, 
                 notifier: NotificationManager, enabled: bool = True):
        super().__init__()
        self.classifier = classifier
        self.db = db
        self.notifier = notifier
        self.enabled = enabled
        self.processing_files = set()  # Track files being processed
    
    def on_created(self, event):
        """Called when a file is created in the Downloads folder"""
        if event.is_directory:
            return
        
        # Only process files, not directories
        if isinstance(event, FileCreatedEvent):
            file_path = Path(event.src_path)
            
            # Skip temporary files and hidden files
            if file_path.name.startswith('.') or file_path.name.startswith('~'):
                return
            
            # Skip if already processing
            if str(file_path) in self.processing_files:
                return
            
            # Wait a bit for the file to finish downloading
            time.sleep(1)
            
            # Process the file
            if self.enabled:
                self.processing_files.add(str(file_path))
                try:
                    self.process_new_file(file_path)
                finally:
                    self.processing_files.discard(str(file_path))
    
    def process_new_file(self, file_path: Path):
        """Process a newly downloaded file"""
        if not file_path.exists():
            return
        
        print(f"\n🔔 New file detected: {file_path.name}")
        
        try:
            # Classify the file using Groq AI
            print(f"🤖 Classifying file with AI...")
            classification, confidence = self.classifier.classify_file(file_path)
            
            print(f"📋 Classification: {classification.get('category', 'unknown')}")
            print(f"📊 Confidence: {confidence:.2%}")
            print(f"📁 Suggested path: {classification.get('suggested_path', 'unknown')}")
            
            # Log to database
            operation_id = self.db.log_file_operation(
                filename=file_path.name,
                original_path=str(file_path),
                new_path=None,
                operation_type='detected',
                file_type=classification.get('category'),
                classification=classification.get('subcategory'),
                confidence=confidence
            )
            
            # Determine destination path
            suggested_path = classification.get('suggested_path', 'misc')
            destination = self._build_destination_path(file_path, suggested_path)
            
            # Move the file
            if confidence > 0.25:  # Only auto-move if reasonably confident
                success = self.move_file(file_path, destination, operation_id)
                
                if success:
                    # Show notification
                    self.notifier.show_notification(
                        title="File Organized",
                        message=f"{file_path.name} → {destination.parent.name}/",
                        sound=True
                    )
                    
                    print(f"✅ File moved to: {destination}")
                else:
                    print(f"❌ Failed to move file")
            else:
                # Low confidence - notify user for manual decision
                self.notifier.show_notification(
                    title="File Needs Review",
                    message=f"{file_path.name} - Low confidence classification",
                    sound=False
                )
                print(f"⚠️  Low confidence - file left in Downloads")
        
        except Exception as e:
            print(f"❌ Error processing file: {e}")
            self.notifier.show_notification(
                title="Error Processing File",
                message=f"Could not process {file_path.name}",
                sound=False
            )
    
    def _build_destination_path(self, file_path: Path, suggested_path: str) -> Path:
        """Build the full destination path for a file"""
        # Get user's home directory
        home = Path.home()
        
        # AI already provides the full path relative to home
        # Just use it directly - AI is smart enough to find existing folders
        destination_dir = home / suggested_path
        
        # Create directory if it doesn't exist
        destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle duplicate filenames
        destination = destination_dir / file_path.name
        counter = 1
        while destination.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            destination = destination_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        return destination
    
    def move_file(self, source: Path, destination: Path, operation_id: int) -> bool:
        """Move a file from source to destination"""
        try:
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(source), str(destination))
            
            # Update database
            self.db.update_operation_status(operation_id, 'completed')
            self.db.log_file_operation(
                filename=destination.name,
                original_path=str(source),
                new_path=str(destination),
                operation_type='moved',
                file_type=None,
                classification=None,
                confidence=None
            )
            
            return True
        
        except Exception as e:
            print(f"Error moving file: {e}")
            self.db.update_operation_status(operation_id, 'failed')
            return False


class FileMonitor:
    """Main file monitoring service"""
    
    def __init__(self):
        self.classifier = AIFileClassifier()
        self.db = Database()
        self.notifier = NotificationManager()
        self.observer: Optional[Observer] = None
        self.handler: Optional[DownloadHandler] = None
        self.enabled = True
    
    def start(self):
        """Start monitoring the Downloads folder"""
        downloads_path = get_downloads_folder()
        
        if not downloads_path.exists():
            print(f"❌ Downloads folder not found: {downloads_path}")
            return
        
        print(f"👀 Starting file monitor...")
        print(f"📂 Monitoring: {downloads_path}")
        
        # Create handler
        self.handler = DownloadHandler(
            classifier=self.classifier,
            db=self.db,
            notifier=self.notifier,
            enabled=self.enabled
        )
        
        # Create observer
        self.observer = Observer()
        self.observer.schedule(self.handler, str(downloads_path), recursive=False)
        self.observer.start()
        
        print(f"✅ File monitor started successfully")
        
        # Show startup notification
        self.notifier.show_notification(
            title="Smart File Organizer Active",
            message="Monitoring Downloads folder for new files",
            sound=False
        )
    
    def stop(self):
        """Stop monitoring"""
        if self.observer:
            print(f"🛑 Stopping file monitor...")
            self.observer.stop()
            self.observer.join()
            print(f"✅ File monitor stopped")
    
    def toggle(self, enabled: bool):
        """Enable or disable auto-organization"""
        self.enabled = enabled
        if self.handler:
            self.handler.enabled = enabled
        
        status = "enabled" if enabled else "disabled"
        print(f"🔄 Auto-organization {status}")
        
        self.notifier.show_notification(
            title=f"Auto-Organization {status.title()}",
            message=f"File organization is now {status}",
            sound=False
        )
    
    def run_forever(self):
        """Run the monitor indefinitely"""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


if __name__ == "__main__":
    # Test the file monitor
    monitor = FileMonitor()
    monitor.start()
    
    try:
        monitor.run_forever()
    except KeyboardInterrupt:
        monitor.stop()
