# Lava API Gateway Integration Guide

## What is Lava?

Lava is a unified API gateway that provides:
- **Single API key** for multiple AI providers (Claude, OpenAI, etc.)
- **Automatic cost tracking** - see exactly how much each file classification costs
- **Usage analytics** - real-time monitoring of API consumption
- **No code changes** - transparent proxy that works with existing code

## Why Use Lava in This Project?

### Benefits for Smart File Organizer

1. **Cost Transparency**
   - See the cost of each file classification in real-time
   - Track total spending on AI operations
   - Identify expensive operations

2. **Usage Analytics**
   - Monitor how many files are being classified
   - Track API request patterns
   - Optimize usage based on data

3. **Simplified Management**
   - One API key instead of managing multiple provider keys
   - Centralized billing and usage tracking
   - Easy to switch between providers if needed

4. **Demo Value**
   - Show judges real-time cost tracking during demo
   - Display usage analytics dashboard
   - Demonstrate production-ready monitoring

## Setup Instructions

### Step 1: Get Lava Credentials

1. Visit https://www.lavapayments.com
2. Sign up for an account
3. Use promo code `LAVA10` for $10 free credits
4. Navigate to your dashboard

### Step 2: Get Your Forward Token

Lava uses "forward tokens" to route requests:

1. Go to **Build > Secret Keys** in dashboard
2. Find your "Self Forward Token" (auto-generated)
3. Copy the token (starts with a base64-encoded string)

### Step 3: Add to .env File

Create or update your `.env` file:

```env
# Claude API Key (still required as fallback)
ANTHROPIC_API_KEY=sk-ant-your_key_here

# Lava Configuration
LAVA_API_KEY=aks_live_your_key_here
LAVA_FORWARD_TOKEN=your_forward_token_here
LAVA_BASE_URL=https://api.lavapayments.com/v1
```

### Step 4: Test the Integration

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test
python backend/test_lava.py
```

## How It Works

### Request Flow

```
Your App → Lava Gateway → Claude API → Response
              ↓
         Cost Tracking
         Usage Analytics
```

### Code Integration

The integration is automatic! When Lava credentials are configured:

```python
# In ai_classifier.py
if self.use_lava:
    # Routes through Lava automatically
    response = lava_gateway.forward_claude_request(...)
else:
    # Direct Claude API call
    response = self.client.messages.create(...)
```

### What Gets Tracked

For each file classification request, Lava tracks:
- **Request ID**: Unique identifier
- **Model Used**: claude-3-5-sonnet-20241022
- **Token Usage**: Input tokens, output tokens, total
- **Cost**: Exact cost in dollars
- **Timestamp**: When the request was made
- **Latency**: How long the request took

## Viewing Analytics

### Dashboard Access

1. Log into https://www.lavapayments.com/dashboard
2. Navigate to **Monetize > Explore**
3. View all requests with detailed breakdowns

### What You'll See

- **Request List**: All API calls made through Lava
- **Cost Breakdown**: Per-request and cumulative costs
- **Usage Graphs**: Visual representation of API usage over time
- **Token Metrics**: Input/output token consumption

### Example Request Details

```json
{
  "request_id": "req_abc123...",
  "timestamp": "2025-10-26T03:00:00Z",
  "model": "claude-3-5-sonnet-20241022",
  "provider": "anthropic",
  "tokens": {
    "input": 245,
    "output": 156,
    "total": 401
  },
  "cost": {
    "base_cost": 0.0012,
    "total": 0.0012
  },
  "latency_ms": 187
}
```

## Demo Tips

### Show Judges Real-Time Tracking

1. **Before Demo**:
   - Open Lava dashboard in a browser tab
   - Navigate to the Explore page
   - Set filter to "Last 1 hour"

2. **During Demo**:
   - Download a test file (triggers classification)
   - Switch to Lava dashboard tab
   - Refresh to show the new request
   - Click on request to show cost breakdown

3. **Talking Points**:
   - "Every file classification is automatically tracked"
   - "We can see this request cost $0.0012"
   - "Over time, we can optimize based on usage patterns"
   - "This is production-ready monitoring"

### Highlight Cost Efficiency

```
Example costs per file:
- Small PDF (CS170_HW7.pdf): ~$0.001
- Large document with preview: ~$0.003
- Simple image file: ~$0.0005

Average cost per file: $0.0015
100 files/day = $0.15/day = $4.50/month
```

## Troubleshooting

### Lava Not Working

**Check 1**: Verify credentials in `.env`
```bash
# Should see:
LAVA_FORWARD_TOKEN=<long_base64_string>
```

**Check 2**: Test connection
```bash
curl -H "Authorization: Bearer $LAVA_FORWARD_TOKEN" \
  https://api.lavapayments.com/v1/usage
```

**Check 3**: Check console output
```
✅ Lava API gateway enabled - cost tracking active
📊 Routing through Lava API gateway for cost tracking...
📊 Lava tracking ID: req_abc123...
```

### Fallback to Direct API

If Lava is not configured, the app automatically falls back to direct Claude API calls:

```
ℹ️  Lava API gateway not configured - using direct API calls
```

This ensures the app works even without Lava.

## Cost Comparison

### With Lava
- **Visibility**: See every request and its cost
- **Overhead**: <20ms added latency
- **Benefit**: Production-ready monitoring

### Without Lava
- **Visibility**: None (manual tracking required)
- **Overhead**: 0ms
- **Benefit**: Slightly faster (but no insights)

**Recommendation**: Use Lava for demos and production. The monitoring value far outweighs the minimal latency.

## Advanced Features

### Usage Statistics API

Get programmatic access to usage data:

```python
from lava_integration import lava_gateway

# Get usage stats
stats = lava_gateway.get_usage_statistics()
print(f"Total requests: {stats['total_requests']}")
print(f"Total cost: ${stats['total_cost']}")
```

### Request Details API

Get details about a specific request:

```python
# Get request details by ID
details = lava_gateway.get_request_details("req_abc123...")
print(f"Cost: ${details['cost']['total']}")
print(f"Tokens: {details['tokens']['total']}")
```

## Integration Checklist

- [ ] Lava account created
- [ ] Promo code `LAVA10` applied ($10 credit)
- [ ] Forward token copied from dashboard
- [ ] `.env` file updated with credentials
- [ ] Test request successful
- [ ] Dashboard showing tracked requests
- [ ] Demo browser tab prepared

## Support

### Lava Documentation
- Main docs: https://www.lavapayments.com/docs
- Quickstart: https://www.lavapayments.com/docs/quickstart-build
- API Reference: https://www.lavapayments.com/docs/api-reference

### Common Issues

**Issue**: "Invalid forward token"
**Solution**: Regenerate token in dashboard, ensure no extra spaces

**Issue**: "Insufficient balance"
**Solution**: Add credits to your Lava wallet

**Issue**: "CORS error"
**Solution**: Lava requires backend calls (not frontend)

## Summary

Lava integration provides:
- ✅ Automatic cost tracking
- ✅ Real-time usage analytics
- ✅ Production-ready monitoring
- ✅ Minimal code changes
- ✅ Great demo value

**Total setup time**: ~5 minutes
**Value for hackathon**: High (shows production thinking)
**Required**: No (optional but recommended)
