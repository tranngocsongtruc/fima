"""
First launch experience for Smart File Organizer
Handles initial setup, permissions, and user choice
"""
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional
from notification_manager import NotificationManager


class FirstLaunchManager:
    """Manages the first-launch experience"""
    
    def __init__(self):
        self.config_file = Path.home() / ".smart_file_organizer" / "config.json"
        self.notifier = NotificationManager()
        
    def is_first_launch(self) -> bool:
        """Check if this is the first time the app is launched"""
        return not self.config_file.exists()
    
    def request_finder_permissions(self) -> bool:
        """
        Request permission to access Finder/Files
        On macOS, this shows a system dialog
        """
        try:
            # Request Full Disk Access via AppleScript
            script = '''
            tell application "System Events"
                display dialog "Smart File Organizer needs permission to access your files to organize them.

Please grant Full Disk Access in System Settings > Privacy & Security > Full Disk Access" buttons {"Open Settings", "Cancel"} default button "Open Settings"
                
                if button returned of result is "Open Settings" then
                    do shell script "open x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
                end if
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error requesting permissions: {e}")
            return False
    
    def analyze_existing_structure(self, directory: Path) -> Dict:
        """
        Analyze user's existing file organization
        Returns statistics and structure info
        """
        stats = {
            'total_files': 0,
            'total_folders': 0,
            'file_types': {},
            'largest_folders': [],
            'organization_score': 0
        }
        
        try:
            # Count files and folders
            for item in directory.rglob('*'):
                if item.is_file():
                    stats['total_files'] += 1
                    ext = item.suffix.lower()
                    stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
                elif item.is_dir():
                    stats['total_folders'] += 1
            
            # Calculate organization score (0-100)
            # Higher score = better organized
            if stats['total_files'] > 0:
                files_per_folder = stats['total_files'] / max(stats['total_folders'], 1)
                stats['organization_score'] = min(100, int(files_per_folder * 10))
            
            return stats
            
        except Exception as e:
            print(f"Error analyzing structure: {e}")
            return stats
    
    def show_choice_dialog(self, stats: Dict) -> str:
        """
        Show dialog asking user to keep current structure or optimize
        Returns: 'keep' or 'optimize'
        """
        try:
            # Create AppleScript dialog
            script = f'''
            set dialogText to "📊 Analysis Complete!

We analyzed your files:
• {stats['total_files']} files
• {stats['total_folders']} folders
• Organization score: {stats['organization_score']}/100

Would you like to:"

            set buttonList to {{"Keep Current Structure", "Optimize with AI"}}
            
            display dialog dialogText buttons buttonList default button 2 with title "Smart File Organizer" with icon note
            
            set userChoice to button returned of result
            
            if userChoice is "Keep Current Structure" then
                return "keep"
            else
                return "optimize"
            end if
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            
            choice = result.stdout.strip()
            return choice if choice in ['keep', 'optimize'] else 'keep'
            
        except Exception as e:
            print(f"Error showing dialog: {e}")
            return 'keep'
    
    def show_supportive_notification(self):
        """
        Show supportive notification when user chooses to keep structure
        """
        self.notifier.show_notification(
            title="We Support Your Choice! 💚",
            message="Your current organization works for you. We'll help keep it that way by organizing new files automatically.",
            sound=True
        )
    
    def show_optimization_notification(self):
        """
        Show notification when user chooses to optimize
        """
        self.notifier.show_notification(
            title="Optimizing Your Files! 🚀",
            message="AI is analyzing your files and creating an optimized structure. This may take a few minutes.",
            sound=True
        )
    
    def save_user_choice(self, choice: str, stats: Dict):
        """Save user's choice and configuration"""
        config = {
            'first_launch_complete': True,
            'user_choice': choice,
            'analysis_stats': stats,
            'setup_date': str(Path.home())
        }
        
        # Create config directory
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def run_first_launch_flow(self, monitor_directory: Path) -> str:
        """
        Run the complete first-launch flow
        Returns the user's choice: 'keep' or 'optimize'
        """
        print("\n" + "="*60)
        print("🎉 Welcome to Smart File Organizer!")
        print("="*60 + "\n")
        
        # Step 1: Request permissions
        print("📋 Step 1: Requesting permissions...")
        self.request_finder_permissions()
        
        # Step 2: Analyze existing structure
        print("🔍 Step 2: Analyzing your files...")
        stats = self.analyze_existing_structure(monitor_directory)
        
        print(f"\n📊 Analysis Results:")
        print(f"   • Files: {stats['total_files']}")
        print(f"   • Folders: {stats['total_folders']}")
        print(f"   • Organization Score: {stats['organization_score']}/100")
        
        # Step 3: Show choice dialog
        print("\n💭 Step 3: Asking for your preference...")
        choice = self.show_choice_dialog(stats)
        
        # Step 4: Show appropriate notification
        if choice == 'keep':
            print("✅ User chose to keep current structure")
            self.show_supportive_notification()
        else:
            print("✅ User chose to optimize")
            self.show_optimization_notification()
        
        # Step 5: Save configuration
        self.save_user_choice(choice, stats)
        
        print("\n✅ First launch complete!")
        print("="*60 + "\n")
        
        return choice


def check_and_run_first_launch(monitor_directory: Path) -> Optional[str]:
    """
    Check if first launch is needed and run it
    Returns user choice if first launch, None otherwise
    """
    manager = FirstLaunchManager()
    
    if manager.is_first_launch():
        return manager.run_first_launch_flow(monitor_directory)
    
    return None
