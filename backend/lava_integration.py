"""
Lava API Gateway Integration
Provides unified API access with automatic cost tracking and usage analytics
"""
import requests
from typing import Dict, Optional, Any
from config import settings
import json


class LavaGateway:
    """
    Lava API Gateway for routing AI requests with cost tracking
    
    Benefits:
    - Unified API access to multiple AI providers
    - Automatic usage tracking and cost analytics
    - Real-time monitoring of API consumption
    - No need to manage multiple API keys
    """
    
    def __init__(self):
        """Initialize Lava gateway"""
        self.base_url = settings.lava_base_url
        self.forward_token = settings.lava_forward_token
        self.enabled = bool(self.forward_token)
        
        if self.enabled:
            print("✅ Lava API gateway enabled - cost tracking active")
        else:
            print("ℹ️  Lava API gateway not configured - using direct API calls")
    
    def forward_claude_request(self, 
                               model: str,
                               messages: list,
                               system: Optional[str] = None,
                               max_tokens: int = 2000,
                               temperature: float = 0.3) -> Dict[str, Any]:
        """
        Forward a Claude API request through Lava gateway
        
        Args:
            model: Claude model name
            messages: List of message dictionaries
            system: System prompt (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Claude API response with Lava metadata
        """
        if not self.enabled:
            raise ValueError("Lava gateway not configured. Set LAVA_FORWARD_TOKEN in .env")
        
        # Build Claude API request
        request_body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if system:
            request_body["system"] = system
        
        # Forward through Lava
        # The 'u' parameter tells Lava which upstream provider to route to
        forward_url = f"{self.base_url}/forward?u=https://api.anthropic.com/v1/messages"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.forward_token}",
            "anthropic-version": "2023-06-01"  # Required by Claude API
        }
        
        try:
            response = requests.post(
                forward_url,
                headers=headers,
                json=request_body,
                timeout=60
            )
            
            response.raise_for_status()
            
            # Get Lava request ID for tracking
            lava_request_id = response.headers.get('x-lava-request-id')
            
            result = response.json()
            
            # Add Lava metadata to response
            result['_lava_metadata'] = {
                'request_id': lava_request_id,
                'tracked': True,
                'provider': 'anthropic'
            }
            
            if lava_request_id:
                print(f"📊 Lava tracking ID: {lava_request_id}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Lava gateway error: {e}")
            raise
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        Get usage statistics from Lava dashboard
        
        Returns:
            Dictionary with usage metrics
        """
        if not self.enabled:
            return {'error': 'Lava not configured'}
        
        try:
            # Call Lava usage API
            url = f"{self.base_url}/usage"
            headers = {
                "Authorization": f"Bearer {self.forward_token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching usage stats: {e}")
            return {'error': str(e)}
    
    def get_request_details(self, request_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific request
        
        Args:
            request_id: Lava request ID from x-lava-request-id header
            
        Returns:
            Request details including cost breakdown
        """
        if not self.enabled:
            return {'error': 'Lava not configured'}
        
        try:
            url = f"{self.base_url}/requests/{request_id}"
            headers = {
                "Authorization": f"Bearer {self.forward_token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching request details: {e}")
            return {'error': str(e)}


# Global instance
lava_gateway = LavaGateway()


def use_lava_if_available() -> bool:
    """Check if Lava should be used"""
    return lava_gateway.enabled
