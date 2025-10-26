"""
Database management for file tracking and organization history
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from contextlib import contextmanager


class Database:
    """SQLite database for tracking file operations"""
    
    def __init__(self, db_path: str = "./data/file_organizer.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # File operations history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_path TEXT NOT NULL,
                    new_path TEXT,
                    operation_type TEXT NOT NULL,
                    file_type TEXT,
                    classification TEXT,
                    confidence REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending'
                )
            """)
            
            # Folder structure analysis
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS folder_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_files INTEGER,
                    folder_structure TEXT,
                    optimization_suggestions TEXT,
                    user_choice TEXT
                )
            """)
            
            # File reminders
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    reminder_time DATETIME NOT NULL,
                    message TEXT,
                    status TEXT DEFAULT 'active',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User preferences
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Email reports
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient_email TEXT NOT NULL,
                    report_data TEXT,
                    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'sent'
                )
            """)
    
    def log_file_operation(self, filename: str, original_path: str, 
                          new_path: Optional[str], operation_type: str,
                          file_type: Optional[str] = None,
                          classification: Optional[str] = None,
                          confidence: Optional[float] = None) -> int:
        """Log a file operation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO file_operations 
                (filename, original_path, new_path, operation_type, file_type, classification, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (filename, original_path, new_path, operation_type, file_type, classification, confidence))
            return cursor.lastrowid
    
    def update_operation_status(self, operation_id: int, status: str):
        """Update the status of a file operation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE file_operations SET status = ? WHERE id = ?
            """, (status, operation_id))
    
    def save_folder_analysis(self, total_files: int, folder_structure: Dict,
                            optimization_suggestions: Dict, user_choice: str = None):
        """Save folder structure analysis"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO folder_analysis 
                (total_files, folder_structure, optimization_suggestions, user_choice)
                VALUES (?, ?, ?, ?)
            """, (total_files, json.dumps(folder_structure), 
                  json.dumps(optimization_suggestions), user_choice))
            return cursor.lastrowid
    
    def create_reminder(self, file_path: str, reminder_time: datetime, message: str = None) -> int:
        """Create a file reminder"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reminders (file_path, reminder_time, message)
                VALUES (?, ?, ?)
            """, (file_path, reminder_time, message))
            return cursor.lastrowid
    
    def get_active_reminders(self) -> List[Dict]:
        """Get all active reminders"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reminders 
                WHERE status = 'active' AND reminder_time <= datetime('now')
                ORDER BY reminder_time
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_reminder_completed(self, reminder_id: int):
        """Mark a reminder as completed"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reminders SET status = 'completed' WHERE id = ?
            """, (reminder_id,))
    
    def save_preference(self, key: str, value: str):
        """Save a user preference"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO preferences (key, value, updated_at)
                VALUES (?, ?, datetime('now'))
            """, (key, value))
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Get a user preference"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row['value'] if row else default
    
    def get_recent_operations(self, limit: int = 100) -> List[Dict]:
        """Get recent file operations"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM file_operations 
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def save_email_report(self, recipient: str, report_data: Dict):
        """Save email report record"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO email_reports (recipient_email, report_data)
                VALUES (?, ?)
            """, (recipient, json.dumps(report_data)))
            return cursor.lastrowid
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total operations
            cursor.execute("SELECT COUNT(*) as count FROM file_operations")
            total_ops = cursor.fetchone()['count']
            
            # Operations by type
            cursor.execute("""
                SELECT operation_type, COUNT(*) as count 
                FROM file_operations 
                GROUP BY operation_type
            """)
            ops_by_type = {row['operation_type']: row['count'] for row in cursor.fetchall()}
            
            # Files organized today
            cursor.execute("""
                SELECT COUNT(*) as count FROM file_operations 
                WHERE date(timestamp) = date('now')
            """)
            today_count = cursor.fetchone()['count']
            
            return {
                'total_operations': total_ops,
                'operations_by_type': ops_by_type,
                'files_organized_today': today_count
            }
