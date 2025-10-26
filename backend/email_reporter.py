"""
Email reporting system for file organization summaries
Sends detailed reports of file operations to user's email
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List
from config import settings
from database import Database


class EmailReporter:
    """Generates and sends email reports of file operations"""
    
    def __init__(self):
        self.db = Database()
        self.smtp_configured = bool(settings.smtp_user and settings.smtp_password)
    
    async def send_organization_report(self, recipient_email: str, 
                                      operations: List[Dict],
                                      summary: Dict):
        """
        Send a detailed organization report via email
        
        Args:
            recipient_email: Recipient's email address
            operations: List of file operations performed
            summary: Summary statistics
        """
        if not self.smtp_configured:
            print("⚠️  Email not configured. Report saved to database only.")
            self._save_report_to_db(recipient_email, operations, summary)
            return False
        
        # Generate HTML email
        html_content = self._generate_html_report(operations, summary)
        
        # Create email message
        message = MIMEMultipart('alternative')
        message['Subject'] = f"Smart File Organizer Report - {datetime.now().strftime('%Y-%m-%d')}"
        message['From'] = settings.smtp_user
        message['To'] = recipient_email
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        try:
            # Send email
            await aiosmtplib.send(
                message,
                hostname=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_user,
                password=settings.smtp_password,
                start_tls=True
            )
            
            print(f"✅ Report sent to {recipient_email}")
            
            # Save to database
            self._save_report_to_db(recipient_email, operations, summary)
            
            return True
        
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _generate_html_report(self, operations: List[Dict], summary: Dict) -> str:
        """Generate HTML email content"""
        
        # Build operations table
        operations_html = ""
        for op in operations:
            operations_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{op.get('filename', 'N/A')}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{op.get('original_path', 'N/A')}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{op.get('new_path', 'N/A')}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{op.get('classification', 'N/A')}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{op.get('timestamp', 'N/A')}</td>
            </tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .summary {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }}
                .summary-item {{
                    display: inline-block;
                    margin: 10px 20px 10px 0;
                }}
                .summary-number {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                }}
                .summary-label {{
                    font-size: 14px;
                    color: #666;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th {{
                    background: #667eea;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                tr:nth-child(even) {{
                    background: #f8f9fa;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #eee;
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📁 Smart File Organizer Report</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Summary</h2>
                <div class="summary-item">
                    <div class="summary-number">{summary.get('files_moved', 0)}</div>
                    <div class="summary-label">Files Moved</div>
                </div>
                <div class="summary-item">
                    <div class="summary-number">{summary.get('folders_created', 0)}</div>
                    <div class="summary-label">Folders Created</div>
                </div>
                <div class="summary-item">
                    <div class="summary-number">{summary.get('folders_archived', 0)}</div>
                    <div class="summary-label">Folders Archived</div>
                </div>
            </div>
            
            <h2>📋 Detailed Operations</h2>
            <table>
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>From</th>
                        <th>To</th>
                        <th>Category</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {operations_html}
                </tbody>
            </table>
            
            <div class="footer">
                <p>🤖 Generated by Smart File Organizer</p>
                <p>Built for CalHacks 12 - October 2025</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _save_report_to_db(self, recipient: str, operations: List[Dict], summary: Dict):
        """Save report to database"""
        import json
        
        report_data = {
            'operations': operations,
            'summary': summary,
            'generated_at': datetime.now().isoformat()
        }
        
        self.db.save_email_report(recipient, report_data)
    
    def generate_text_report(self, operations: List[Dict], summary: Dict) -> str:
        """Generate a plain text report for console output"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           SMART FILE ORGANIZER - OPERATION REPORT            ║
╚══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
───────────────────────────────────────────────────────────────
📦 Files Moved:        {summary.get('files_moved', 0)}
📁 Folders Created:    {summary.get('folders_created', 0)}
🗂️  Folders Archived:  {summary.get('folders_archived', 0)}

DETAILED OPERATIONS
───────────────────────────────────────────────────────────────
"""
        
        for i, op in enumerate(operations, 1):
            report += f"""
{i}. {op.get('filename', 'N/A')}
   From: {op.get('original_path', 'N/A')}
   To:   {op.get('new_path', 'N/A')}
   Type: {op.get('classification', 'N/A')}
   Time: {op.get('timestamp', 'N/A')}
"""
        
        report += """
───────────────────────────────────────────────────────────────
🤖 Smart File Organizer - CalHacks 12
"""
        
        return report


# Test email reporter
if __name__ == "__main__":
    import asyncio
    
    reporter = EmailReporter()
    
    # Sample data
    operations = [
        {
            'filename': 'CS170_HW7.pdf',
            'original_path': '~/Downloads/CS170_HW7.pdf',
            'new_path': '~/Documents/SmartFileOrganizer/uc_berkeley/fall_2025/cs170/homework/CS170_HW7.pdf',
            'classification': 'homework',
            'timestamp': datetime.now().isoformat()
        },
        {
            'filename': 'receipt.pdf',
            'original_path': '~/Downloads/receipt.pdf',
            'new_path': '~/Documents/SmartFileOrganizer/personal/receipts/2025/receipt.pdf',
            'classification': 'receipt',
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    summary = {
        'files_moved': 2,
        'folders_created': 3,
        'folders_archived': 0
    }
    
    # Generate text report
    text_report = reporter.generate_text_report(operations, summary)
    print(text_report)
