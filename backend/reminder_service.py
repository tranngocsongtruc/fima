"""
File reminder service
Allows users to set reminders for files (30min, 1hr, 3hr, custom)
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
from database import Database
from notification_manager import NotificationManager


class ReminderService:
    """Manages file reminders and notifications"""
    
    def __init__(self, db: Database, notifier: NotificationManager):
        self.db = db
        self.notifier = notifier
        self.running = False
    
    def create_reminder(self, file_path: str, minutes: int, 
                       custom_message: Optional[str] = None) -> int:
        """
        Create a reminder for a file
        
        Args:
            file_path: Path to the file
            minutes: Minutes until reminder (30, 60, 180, or custom)
            custom_message: Optional custom reminder message
            
        Returns:
            Reminder ID
        """
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        
        message = custom_message or f"Check file: {Path(file_path).name}"
        
        reminder_id = self.db.create_reminder(file_path, reminder_time, message)
        
        print(f"⏰ Reminder set for {Path(file_path).name} in {minutes} minutes")
        
        return reminder_id
    
    def create_quick_reminder(self, file_path: str, preset: str) -> int:
        """
        Create a reminder using preset times
        
        Args:
            file_path: Path to the file
            preset: '30min', '1hr', '3hr'
            
        Returns:
            Reminder ID
        """
        preset_minutes = {
            '30min': 30,
            '1hr': 60,
            '3hr': 180
        }
        
        minutes = preset_minutes.get(preset, 30)
        return self.create_reminder(file_path, minutes)
    
    async def check_reminders_loop(self):
        """Background task to check for due reminders"""
        self.running = True
        print("⏰ Reminder service started")
        
        while self.running:
            try:
                # Check for active reminders
                active_reminders = self.db.get_active_reminders()
                
                for reminder in active_reminders:
                    # Show notification
                    file_path = reminder['file_path']
                    message = reminder['message']
                    
                    self.notifier.show_reminder_notification(
                        Path(file_path).name,
                        message
                    )
                    
                    print(f"🔔 Reminder triggered: {message}")
                    
                    # Mark as completed
                    self.db.mark_reminder_completed(reminder['id'])
                
                # Check every 30 seconds
                await asyncio.sleep(30)
            
            except Exception as e:
                print(f"Error in reminder loop: {e}")
                await asyncio.sleep(30)
    
    def stop(self):
        """Stop the reminder service"""
        self.running = False
        print("⏰ Reminder service stopped")
    
    async def start_background_task(self):
        """Start the reminder checking background task"""
        await self.check_reminders_loop()


# Test reminder service
if __name__ == "__main__":
    import asyncio
    
    db = Database()
    notifier = NotificationManager()
    service = ReminderService(db, notifier)
    
    # Create test reminder (1 minute)
    test_file = "~/Downloads/test_file.pdf"
    service.create_reminder(test_file, 1, "Test reminder - check this file!")
    
    print("Reminder created. Waiting...")
    
    # Run the service
    try:
        asyncio.run(service.start_background_task())
    except KeyboardInterrupt:
        service.stop()
