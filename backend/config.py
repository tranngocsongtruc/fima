"""
Configuration management for Smart File Organizer
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ============================================
    # AI API KEYS
    # ============================================
    # ⭐ CLAUDE API KEY - Primary for file classification and folder analysis
    # THIS IS WHERE YOU PUT YOUR CLAUDE/ANTHROPIC API KEY
    anthropic_api_key: str = ""
    
    # Optional: Lava API gateway for cost tracking
    lava_api_key: Optional[str] = None
    lava_forward_token: Optional[str] = None
    lava_base_url: str = "https://api.lavapayments.com/v1"
    
    # ============================================
    # EMAIL CONFIGURATION
    # ============================================
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # ============================================
    # APPLICATION SETTINGS
    # ============================================
    # Directory to monitor
    monitor_directory: str = str(Path.home() / "Downloads")
    
    # Enable/disable features
    auto_organize_enabled: bool = True
    enable_notifications: bool = True
    enable_sound_alerts: bool = True
    
    # ============================================
    # PRIVACY & SECURITY SETTINGS
    # ============================================
    # Privacy mode: strict, balanced, standard
    # - strict: filename only, no content
    # - balanced: filename + 200 chars from PDFs
    # - standard: filename + 500 chars from PDFs
    privacy_mode: str = "standard"
    
    # Extract text from PDFs for better classification
    extract_pdf_text: bool = True
    
    # Maximum characters to extract from PDFs
    max_pdf_chars: int = 500
    
    # Log what data is sent to AI (for auditing)
    log_ai_requests: bool = False
    
    # Database
    database_path: str = "./data/file_organizer.db"
    
    # Logging
    log_level: str = "INFO"
    
    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    
    # ============================================
    # AI MODEL SETTINGS
    # ============================================
    # Claude model for classification and analysis
    claude_model: str = "claude-3-5-sonnet-20241022"
    
    # Temperature for AI responses
    ai_temperature: float = 0.3
    
    # Max tokens
    max_tokens: int = 2000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_api_keys():
    """Validate that required API keys are present"""
    errors = []
    
    if not settings.anthropic_api_key or settings.anthropic_api_key == "sk-ant-your_claude_api_key_here":
        errors.append("❌ ANTHROPIC_API_KEY is missing or invalid. Get it at https://console.anthropic.com")
    
    if errors:
        print("\n" + "="*60)
        print("⚠️  API KEY CONFIGURATION ERRORS")
        print("="*60)
        for error in errors:
            print(error)
        print("\nPlease update your .env file with valid API keys.")
        print("See .env.example for the correct format.")
        print("="*60 + "\n")
        return False
    
    print("✅ All required API keys are configured")
    
    # Optional: Check Lava configuration
    if settings.lava_api_key and settings.lava_forward_token:
        print("✅ Lava API gateway configured (optional)")
    
    return True


def get_downloads_folder() -> Path:
    """Get the user's Downloads folder path"""
    if settings.monitor_directory.startswith("~"):
        return Path(settings.monitor_directory).expanduser()
    return Path(settings.monitor_directory)
