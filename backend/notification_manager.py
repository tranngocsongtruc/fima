"""
macOS notification system for file organization alerts
Uses native macOS UserNotifications framework
"""
import subprocess
import platform
from typing import Optional


class NotificationManager:
    """Manages system notifications for file operations"""
    
    def __init__(self):
        self.system = platform.system()
        self.app_name = "Smart File Organizer"
    
    def show_notification(self, title: str, message: str, sound: bool = False):
        """
        Show a native macOS notification
        
        Args:
            title: Notification title
            message: Notification message
            sound: Whether to play a sound
        """
        if self.system == "Darwin":  # macOS
            self._show_macos_notification(title, message, sound)
        else:
            # Fallback for other systems
            print(f"📢 {title}: {message}")
    
    def _show_macos_notification(self, title: str, message: str, sound: bool):
        """Show notification using macOS osascript"""
        try:
            # Build AppleScript command
            script = f'''
                display notification "{message}" with title "{self.app_name}" subtitle "{title}"
            '''
            
            if sound:
                script += ' sound name "Glass"'
            
            # Execute AppleScript
            subprocess.run(
                ['osascript', '-e', script],
                check=True,
                capture_output=True
            )
        
        except Exception as e:
            print(f"Error showing notification: {e}")
            # Fallback to console
            print(f"📢 {title}: {message}")
    
    def show_progress_notification(self, title: str, progress: int, total: int):
        """
        Show a progress notification
        
        Args:
            title: Notification title
            progress: Current progress count
            total: Total items
        """
        percentage = int((progress / total) * 100) if total > 0 else 0
        message = f"Progress: {progress}/{total} ({percentage}%)"
        
        # Show at specific milestones
        if percentage in [50, 90, 100]:
            self.show_notification(title, message, sound=(percentage == 100))
    
    def show_file_moved_notification(self, filename: str, from_folder: str, to_folder: str):
        """Show notification when a file is moved"""
        title = "File Organized"
        message = f"{filename}\n{from_folder} → {to_folder}"
        self.show_notification(title, message, sound=True)
    
    def show_reminder_notification(self, filename: str, custom_message: Optional[str] = None):
        """Show a file reminder notification with sound"""
        title = "File Reminder"
        message = custom_message or f"Don't forget to check: {filename}"
        self.show_notification(title, message, sound=True)
    
    def show_optimization_complete(self, files_moved: int, folders_created: int):
        """Show notification when optimization is complete"""
        title = "Optimization Complete! 🎉"
        message = f"Moved {files_moved} files, created {folders_created} folders"
        self.show_notification(title, message, sound=True)
    
    def show_user_choice_confirmation(self, choice: str):
        """Show confirmation of user's organization choice"""
        if choice == "keep":
            title = "Choice Confirmed"
            message = "I support your decision and will try the best to help you keep track of all files"
        else:
            title = "Optimization Starting"
            message = "Beginning file organization process..."
        
        self.show_notification(title, message, sound=False)
    
    def show_error_notification(self, error_message: str):
        """Show error notification"""
        title = "Error"
        self.show_notification(title, error_message, sound=True)


# Test notifications
if __name__ == "__main__":
    notifier = NotificationManager()
    
    print("Testing notifications...")
    
    # Test basic notification
    notifier.show_notification(
        "Test Notification",
        "This is a test message",
        sound=True
    )
    
    import time
    time.sleep(2)
    
    # Test file moved notification
    notifier.show_file_moved_notification(
        "homework.pdf",
        "Downloads",
        "uc_berkeley/fall_2025/cs170"
    )
    
    time.sleep(2)
    
    # Test progress notification
    notifier.show_progress_notification("Organizing Files", 50, 100)
    
    time.sleep(2)
    
    # Test reminder
    notifier.show_reminder_notification("important_document.pdf")
    
    print("✅ Notification tests complete")
