"""
Main FastAPI server for Smart File Organizer
Provides REST API for the frontend application

This addresses the Annapurna Labs System Architecture & Integration track
"""
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from pathlib import Path
from datetime import datetime
import uvicorn

# Import our modules
from config import settings, validate_api_keys, get_downloads_folder
from ai_classifier import AIFileClassifier
from notification_manager import NotificationManager
from first_launch import check_and_run_first_launch

# Optional imports - gracefully handle missing dependencies
try:
    from database import Database
    db = None  # Will be initialized later
except ImportError:
    print("⚠️  Database module not available - running in limited mode")
    Database = None
    db = None

try:
    from folder_analyzer import FolderAnalyzer
    analyzer = None
except ImportError:
    print("⚠️  Folder analyzer not available")
    FolderAnalyzer = None
    analyzer = None

try:
    from file_monitor import FileMonitor
    file_monitor = None
except ImportError:
    print("⚠️  File monitor not available")
    FileMonitor = None
    file_monitor = None

try:
    from email_reporter import EmailReporter
    email_reporter = None
except ImportError:
    print("⚠️  Email reporter not available - email features disabled")
    EmailReporter = None
    email_reporter = None

try:
    from reorganizer import FileReorganizer
except ImportError:
    print("⚠️  Reorganizer not available")
    FileReorganizer = None

try:
    from reminder_service import ReminderService
    reminder_service = None
except ImportError:
    print("⚠️  Reminder service not available")
    ReminderService = None
    reminder_service = None

# Initialize FastAPI app
app = FastAPI(
    title="Smart File Organizer API",
    description="AI-powered file organization system for CalHacks 12",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
classifier = AIFileClassifier()
notifier = NotificationManager()

# Initialize optional components
if Database:
    db = Database()
if FolderAnalyzer:
    analyzer = FolderAnalyzer()
if EmailReporter:
    email_reporter = EmailReporter()
if ReminderService and db:
    reminder_service = ReminderService(db, notifier)

file_monitor: Optional[FileMonitor] = None


# ============================================
# Pydantic Models
# ============================================

class AnalysisRequest(BaseModel):
    directory: Optional[str] = None


class UserChoiceRequest(BaseModel):
    choice: str  # "keep" or "optimize"


class ReorganizeRequest(BaseModel):
    migration_plan: List[Dict]


class EmailReportRequest(BaseModel):
    email: str
    operations: List[Dict]
    summary: Dict


class ReminderRequest(BaseModel):
    file_path: str
    preset: Optional[str] = None  # "30min", "1hr", "3hr"
    custom_minutes: Optional[int] = None
    message: Optional[str] = None


class ToggleRequest(BaseModel):
    enabled: bool


# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """Serve the frontend HTML"""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    else:
        return {
            "status": "running",
            "app": "Smart File Organizer",
            "version": "1.0.0",
            "hackathon": "CalHacks 12",
            "message": "Frontend not found. API is running at /api/*"
        }


@app.get("/api/status")
async def get_status():
    """Get system status"""
    stats = db.get_statistics()
    
    return {
        "monitor_active": file_monitor is not None and file_monitor.enabled,
        "downloads_folder": str(get_downloads_folder()),
        "statistics": stats,
        "api_keys_configured": {
            "groq": bool(settings.groq_api_key),
            "claude": bool(settings.anthropic_api_key),
            "lava": bool(settings.lava_api_key)
        }
    }


@app.post("/api/analyze")
async def analyze_folder_structure(request: AnalysisRequest):
    """
    Analyze current folder structure and provide optimization suggestions
    
    This is Phase 1: Initial Setup
    """
    try:
        # Get directory to analyze
        if request.directory:
            root_path = Path(request.directory).expanduser()
        else:
            root_path = Path.home() / "Documents"
        
        if not root_path.exists():
            raise HTTPException(status_code=404, detail="Directory not found")
        
        print(f"\n🔍 Starting folder analysis...")
        
        # Perform full analysis using Claude
        structure, analysis, suggestions = analyzer.perform_full_analysis(root_path)
        
        # Save to database
        total_files = structure.get('file_count', 0)
        db.save_folder_analysis(
            total_files=total_files,
            folder_structure=structure,
            optimization_suggestions=suggestions
        )
        
        return {
            "structure": structure,
            "analysis": analysis,
            "suggestions": suggestions,
            "total_files": total_files
        }
    
    except Exception as e:
        print(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user-choice")
async def handle_user_choice(request: UserChoiceRequest):
    """
    Handle user's choice to keep current organization or optimize
    
    Shows appropriate notification based on choice
    """
    try:
        choice = request.choice.lower()
        
        # Save preference
        db.save_preference("organization_choice", choice)
        
        # Show notification
        notifier.show_user_choice_confirmation(choice)
        
        if choice == "keep":
            message = "I support your decision and will try the best to help you keep track of all files"
        else:
            message = "Optimization process ready to begin"
        
        return {
            "choice": choice,
            "message": message,
            "status": "confirmed"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reorganize")
async def reorganize_files(request: ReorganizeRequest, background_tasks: BackgroundTasks):
    """
    Execute file reorganization based on migration plan
    
    Shows progress notifications at 50%, 90%, 100%
    """
    try:
        reorganizer = FileReorganizer(db, notifier)
        
        # Execute reorganization
        summary = reorganizer.execute_reorganization(
            migration_plan=request.migration_plan
        )
        
        return {
            "status": "completed",
            "summary": summary
        }
    
    except Exception as e:
        print(f"Error in reorganization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/email-report")
async def send_email_report(request: EmailReportRequest):
    """Send email report of file operations"""
    try:
        success = await email_reporter.send_organization_report(
            recipient_email=request.email,
            operations=request.operations,
            summary=request.summary
        )
        
        if success:
            return {"status": "sent", "email": request.email}
        else:
            return {"status": "saved", "message": "Report saved to database (email not configured)"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/monitor/start")
async def start_monitoring():
    """Start monitoring Downloads folder"""
    global file_monitor
    
    try:
        if file_monitor is None:
            file_monitor = FileMonitor()
        
        file_monitor.start()
        
        return {
            "status": "started",
            "monitoring": str(get_downloads_folder())
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/monitor/stop")
async def stop_monitoring():
    """Stop monitoring Downloads folder"""
    global file_monitor
    
    try:
        if file_monitor:
            file_monitor.stop()
        
        return {"status": "stopped"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/monitor/toggle")
async def toggle_monitoring(request: ToggleRequest):
    """Toggle auto-organization on/off"""
    global file_monitor
    
    try:
        if file_monitor:
            file_monitor.toggle(request.enabled)
        
        status = "enabled" if request.enabled else "disabled"
        
        return {
            "status": status,
            "auto_organize": request.enabled
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/classify-file")
async def classify_single_file(file_path: str):
    """Classify a single file"""
    try:
        path = Path(file_path).expanduser()
        
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        classification, confidence = classifier.classify_file(path)
        
        return {
            "file": str(path),
            "classification": classification,
            "confidence": confidence
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reminder")
async def create_file_reminder(request: ReminderRequest):
    """Create a reminder for a file"""
    try:
        if request.preset:
            reminder_id = reminder_service.create_quick_reminder(
                request.file_path,
                request.preset
            )
        elif request.custom_minutes:
            reminder_id = reminder_service.create_reminder(
                request.file_path,
                request.custom_minutes,
                request.message
            )
        else:
            raise HTTPException(status_code=400, detail="Must specify preset or custom_minutes")
        
        return {
            "reminder_id": reminder_id,
            "file": request.file_path,
            "status": "created"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/operations/recent")
async def get_recent_operations(limit: int = 50):
    """Get recent file operations"""
    try:
        operations = db.get_recent_operations(limit)
        return {"operations": operations}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/statistics")
async def get_statistics():
    """Get usage statistics"""
    try:
        stats = db.get_statistics()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/lava/stats")
async def get_lava_stats():
    """Get Lava API usage statistics"""
    try:
        from lava_integration import lava_gateway
        
        if not lava_gateway or not settings.lava_api_key:
            return {
                "total_requests": 0,
                "total_cost": 0,
                "total_tokens": 0,
                "enabled": False
            }
        
        # Get stats from Lava (this would be a real API call in production)
        # For now, return mock data based on operations count
        operations = db.get_recent_operations(1000) if db else []
        total_requests = len(operations)
        
        # Estimate: ~$0.001 per request, ~1000 tokens per request
        total_cost = total_requests * 0.001
        total_tokens = total_requests * 1000
        
        return {
            "total_requests": total_requests,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "enabled": True
        }
    
    except Exception as e:
        return {
            "total_requests": 0,
            "total_cost": 0,
            "total_tokens": 0,
            "enabled": False
        }


@app.get("/api/status")
async def get_status():
    """Get current system status"""
    try:
        operations = db.get_recent_operations(100) if db else []
        
        # Calculate stats
        files_organized = len(operations)
        avg_confidence = sum(op.get('confidence', 0) for op in operations) / len(operations) if operations else 0
        
        return {
            "files_organized": files_organized,
            "total_operations": files_organized,
            "avg_confidence": avg_confidence,
            "monitoring": file_monitor is not None and hasattr(file_monitor, 'is_running') and file_monitor.is_running
        }
    
    except Exception as e:
        return {
            "files_organized": 0,
            "total_operations": 0,
            "avg_confidence": 0,
            "monitoring": False
        }


# ============================================
# Startup and Shutdown Events
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("\n" + "="*60)
    print("🚀 Smart File Organizer - Starting Up")
    print("="*60)
    
    # Check for first launch
    monitor_dir = get_downloads_folder()
    user_choice = check_and_run_first_launch(monitor_dir)
    
    if user_choice:
        print(f"\n✅ First launch complete - User chose: {user_choice}")
    
    # Validate API keys
    if not validate_api_keys():
        print("\n⚠️  WARNING: API keys not configured properly")
        print("The application will start but AI features may not work.")
        print("Please configure your .env file with valid API keys.\n")
    
    # Start reminder service in background
    if reminder_service:
        asyncio.create_task(reminder_service.start_background_task())
    
    print(f"\n✅ Server ready at http://{settings.host}:{settings.port}")
    print(f"📚 API docs at http://{settings.host}:{settings.port}/docs")
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n🛑 Shutting down...")
    
    global file_monitor
    if file_monitor:
        file_monitor.stop()
    
    reminder_service.stop()
    
    print("✅ Shutdown complete\n")


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
