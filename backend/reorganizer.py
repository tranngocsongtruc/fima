"""
File reorganization orchestrator
Handles the actual moving of files during optimization
"""
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Callable
from datetime import datetime
from database import Database
from notification_manager import NotificationManager
import time


class FileReorganizer:
    """Orchestrates file reorganization operations"""
    
    def __init__(self, db: Database, notifier: NotificationManager):
        self.db = db
        self.notifier = notifier
        self.operations_log = []
    
    def execute_reorganization(self, 
                              migration_plan: List[Dict],
                              progress_callback: Callable[[int, int], None] = None) -> Dict:
        """
        Execute a reorganization plan
        
        Args:
            migration_plan: List of operations to perform
            progress_callback: Function to call with progress updates
            
        Returns:
            Summary of operations performed
        """
        total_operations = len(migration_plan)
        completed = 0
        files_moved = 0
        folders_created = 0
        folders_archived = 0
        errors = []
        
        print(f"\n🚀 Starting reorganization: {total_operations} operations")
        
        for i, operation in enumerate(migration_plan):
            try:
                action = operation.get('action', 'unknown')
                
                if action == 'move':
                    success = self._move_file(operation)
                    if success:
                        files_moved += 1
                
                elif action == 'create':
                    success = self._create_folder(operation)
                    if success:
                        folders_created += 1
                
                elif action == 'archive':
                    success = self._archive_folder(operation)
                    if success:
                        folders_archived += 1
                
                completed += 1
                
                # Progress notifications at 50%, 90%, 100%
                percentage = int((completed / total_operations) * 100)
                if percentage in [50, 90, 100]:
                    self._show_progress_notification(completed, total_operations, percentage)
                
                # Call progress callback
                if progress_callback:
                    progress_callback(completed, total_operations)
                
            except Exception as e:
                error_msg = f"Error in operation {i+1}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        # Final notification
        self.notifier.show_optimization_complete(files_moved, folders_created)
        
        summary = {
            'total_operations': total_operations,
            'completed': completed,
            'files_moved': files_moved,
            'folders_created': folders_created,
            'folders_archived': folders_archived,
            'errors': errors,
            'operations_log': self.operations_log
        }
        
        print(f"\n✅ Reorganization complete!")
        print(f"   Files moved: {files_moved}")
        print(f"   Folders created: {folders_created}")
        print(f"   Folders archived: {folders_archived}")
        
        return summary
    
    def _move_file(self, operation: Dict) -> bool:
        """Move a file from source to destination"""
        try:
            source = Path(operation['source']).expanduser()
            destination = Path(operation['destination']).expanduser()
            
            if not source.exists():
                print(f"⚠️  Source file not found: {source}")
                return False
            
            # Create destination directory
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle duplicates
            if destination.exists():
                destination = self._get_unique_path(destination)
            
            # Move file
            shutil.move(str(source), str(destination))
            
            # Log operation
            self.db.log_file_operation(
                filename=source.name,
                original_path=str(source),
                new_path=str(destination),
                operation_type='moved',
                file_type=None,
                classification=operation.get('reason', 'reorganization'),
                confidence=1.0
            )
            
            self.operations_log.append({
                'action': 'move',
                'filename': source.name,
                'from': str(source.parent),
                'to': str(destination.parent),
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✓ Moved: {source.name} → {destination.parent.name}/")
            
            return True
        
        except Exception as e:
            print(f"❌ Error moving file: {e}")
            return False
    
    def _create_folder(self, operation: Dict) -> bool:
        """Create a new folder"""
        try:
            folder_path = Path(operation['destination']).expanduser()
            folder_path.mkdir(parents=True, exist_ok=True)
            
            self.operations_log.append({
                'action': 'create',
                'folder': str(folder_path),
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✓ Created folder: {folder_path}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
            return False
    
    def _archive_folder(self, operation: Dict) -> bool:
        """Archive a folder (move to archive location)"""
        try:
            source = Path(operation['source']).expanduser()
            
            if not source.exists():
                print(f"⚠️  Folder not found: {source}")
                return False
            
            # Create archive directory
            archive_base = Path.home() / "Documents" / "SmartFileOrganizer" / "_archived"
            archive_base.mkdir(parents=True, exist_ok=True)
            
            # Create timestamped archive folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dest = archive_base / f"{source.name}_{timestamp}"
            
            # Move to archive
            shutil.move(str(source), str(archive_dest))
            
            self.operations_log.append({
                'action': 'archive',
                'folder': source.name,
                'archived_to': str(archive_dest),
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✓ Archived: {source.name} → _archived/")
            
            return True
        
        except Exception as e:
            print(f"❌ Error archiving folder: {e}")
            return False
    
    def _get_unique_path(self, path: Path) -> Path:
        """Generate a unique path if file already exists"""
        counter = 1
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        
        while path.exists():
            path = parent / f"{stem}_{counter}{suffix}"
            counter += 1
        
        return path
    
    def _show_progress_notification(self, completed: int, total: int, percentage: int):
        """Show progress notification at milestones"""
        if percentage == 50:
            message = f"Halfway there! {completed}/{total} operations completed"
            self.notifier.show_notification("Reorganization Progress", message, sound=False)
            
            # Show some file movements
            recent_ops = self.operations_log[-5:]
            for op in recent_ops:
                if op['action'] == 'move':
                    print(f"   📄 {op['filename']}: {op['from']} → {op['to']}")
        
        elif percentage == 90:
            message = f"Almost done! {completed}/{total} operations completed"
            self.notifier.show_notification("Reorganization Progress", message, sound=False)
        
        elif percentage == 100:
            # Final notification handled by caller
            pass
    
    def create_archive_folder(self, folders_to_archive: List[str]) -> Path:
        """
        Create a single archive folder containing all folders marked for deletion
        
        Returns:
            Path to the archive folder
        """
        if not folders_to_archive:
            return None
        
        # Create archive directory
        archive_base = Path.home() / "Documents" / "SmartFileOrganizer" / "_to_review"
        archive_base.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_folder = archive_base / f"archived_{timestamp}"
        archive_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📦 Creating archive folder: {archive_folder}")
        
        for folder_path in folders_to_archive:
            try:
                source = Path(folder_path).expanduser()
                if source.exists() and source.is_dir():
                    dest = archive_folder / source.name
                    shutil.move(str(source), str(dest))
                    print(f"   ✓ Archived: {source.name}")
            except Exception as e:
                print(f"   ❌ Error archiving {folder_path}: {e}")
        
        self.notifier.show_notification(
            "Folders Archived",
            f"Review archived folders in: {archive_folder.name}",
            sound=False
        )
        
        return archive_folder
