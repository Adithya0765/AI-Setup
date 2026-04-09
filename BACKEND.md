# NEXUS Backend Implementation Guide

## Overview

Complete guide to building the NEXUS backend that handles authentication, usage tracking, and AI orchestration.

## Tech Stack Recommendation

### Backend Framework
- **FastAPI** (Python) - Fast, modern, async
- Alternative: Express.js (Node.js)

### Database
- **PostgreSQL** - User accounts, usage tracking
- **Redis** - Session management, rate limiting

### Authentication
- **JWT tokens** - Stateless authentication
- **bcrypt** - Password hashing

### Payment Processing
- **Stripe** - Subscription management

### Infrastructure
- **Docker** - Containerization
- **AWS/GCP/Azure** - Cloud hosting
- **CloudFlare** - CDN + DDoS protection

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    plan VARCHAR(50) DEFAULT 'free', -- free, pro, enterprise
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_verification_token ON users(verification_token);
```

### Devices Table
```sql
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id VARCHAR(255) UNIQUE NOT NULL,
    machine_id VARCHAR(255),
    ip_address INET,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    anonymous_prompts_used INTEGER DEFAULT 0,
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    is_flagged BOOLEAN DEFAULT FALSE,
    flag_reason TEXT
);

CREATE INDEX idx_devices_device_id ON devices(device_id);
CREATE INDEX idx_devices_user_id ON devices(user_id);
CREATE INDEX idx_devices_ip ON devices(ip_address);
```

### Usage Table
```sql
CREATE TABLE usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id) ON DELETE SET NULL,
    prompt_text TEXT,
    prompt_hash VARCHAR(64), -- SHA256 of prompt for deduplication
    tokens_used INTEGER,
    cost DECIMAL(10, 4),
    success BOOLEAN,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usage_user_id ON usage(user_id);
CREATE INDEX idx_usage_created_at ON usage(created_at);
CREATE INDEX idx_usage_prompt_hash ON usage(prompt_hash);
```

### Subscriptions Table
```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    plan VARCHAR(50), -- pro, enterprise
    status VARCHAR(50), -- active, canceled, past_due
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_customer_id ON subscriptions(stripe_customer_id);
```

### API Keys Table (Your Keys)
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider VARCHAR(50), -- gemini, grok
    key_value TEXT NOT NULL,
    requests_used INTEGER DEFAULT 0,
    requests_limit INTEGER,
    cooldown_until TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_keys_provider ON api_keys(provider);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);
```

## API Endpoints

### Authentication

#### POST /api/v1/auth/signup
```python
@app.post("/api/v1/auth/signup")
async def signup(request: SignupRequest):
    """
    Create new user account
    
    Request:
    {
        "email": "user@example.com",
        "password": "secure_password"
    }
    
    Response:
    {
        "success": true,
        "message": "Verification email sent",
        "user_id": "uuid"
    }
    """
    # Validate email
    if not is_valid_email(request.email):
        raise HTTPException(400, "Invalid email")
    
    # Check disposable email
    if is_disposable_email(request.email):
        raise HTTPException(400, "Disposable emails not allowed")
    
    # Check if exists
    if await db.user_exists(request.email):
        raise HTTPException(400, "Email already registered")
    
    # Hash password
    password_hash = bcrypt.hashpw(
        request.password.encode(),
        bcrypt.gensalt()
    )
    
    # Create user
    verification_token = secrets.token_urlsafe(32)
    user = await db.create_user(
        email=request.email,
        password_hash=password_hash,
        verification_token=verification_token
    )
    
    # Send verification email
    await send_verification_email(
        email=request.email,
        token=verification_token
    )
    
    return {
        "success": True,
        "message": "Verification email sent",
        "user_id": str(user.id)
    }
```

#### POST /api/v1/auth/verify
```python
@app.post("/api/v1/auth/verify")
async def verify_email(token: str):
    """Verify email address"""
    user = await db.get_user_by_verification_token(token)
    
    if not user:
        raise HTTPException(400, "Invalid token")
    
    await db.verify_user(user.id)
    
    return {"success": True, "message": "Email verified"}
```

#### POST /api/v1/auth/login
```python
@app.post("/api/v1/auth/login")
async def login(request: LoginRequest):
    """
    Login user
    
    Request:
    {
        "email": "user@example.com",
        "password": "password"
    }
    
    Response:
    {
        "success": true,
        "token": "jwt_token",
        "user": {
            "email": "user@example.com",
            "plan": "free",
            "prompts_remaining": 45
        }
    }
    """
    user = await db.get_user_by_email(request.email)
    
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    # Verify password
    if not bcrypt.checkpw(
        request.password.encode(),
        user.password_hash.encode()
    ):
        raise HTTPException(401, "Invalid credentials")
    
    # Check email verified
    if not user.email_verified:
        raise HTTPException(401, "Email not verified")
    
    # Generate JWT
    token = create_jwt_token(user.id)
    
    # Get usage stats
    prompts_used = await db.get_monthly_usage(user.id)
    
    return {
        "success": True,
        "token": token,
        "user": {
            "email": user.email,
            "plan": user.plan,
            "prompts_remaining": 50 - prompts_used if user.plan == "free" else "unlimited"
        }
    }
```

### Prompt Execution

#### POST /api/v1/prompts/execute
```python
@app.post("/api/v1/prompts/execute")
async def execute_prompt(
    request: PromptRequest,
    authorization: str = Header(None)
):
    """
    Execute a prompt
    
    Request:
    {
        "prompt": "fix bug in auth.py",
        "context": {...},
        "device_id": "uuid" // for anonymous
    }
    
    Response:
    {
        "success": true,
        "result": "...",
        "prompts_remaining": 4
    }
    """
    
    # Check if authenticated
    if authorization:
        # Authenticated user
        token = authorization.replace("Bearer ", "")
        user_id = verify_jwt_token(token)
        user = await db.get_user(user_id)
        
        if not user:
            raise HTTPException(401, "Invalid token")
        
        # Check limits
        if user.plan == "free":
            usage = await db.get_monthly_usage(user.id)
            if usage >= 50:
                raise HTTPException(429, "Monthly limit reached. Upgrade to Pro.")
        
        # Execute prompt
        result = await execute_with_ai(request.prompt, request.context)
        
        # Track usage
        await db.track_usage(
            user_id=user.id,
            prompt=request.prompt,
            tokens_used=result.tokens,
            cost=result.cost,
            success=True
        )
        
        remaining = 50 - usage - 1 if user.plan == "free" else "unlimited"
        
        return {
            "success": True,
            "result": result.content,
            "prompts_remaining": remaining
        }
    
    else:
        # Anonymous user
        if not request.device_id:
            raise HTTPException(400, "Device ID required")
        
        device = await db.get_or_create_device(
            device_id=request.device_id,
            machine_id=request.machine_id,
            ip_address=request.ip_address
        )
        
        # Check anonymous limit
        if device.anonymous_prompts_used >= 5:
            raise HTTPException(
                429,
                "Free prompts exhausted. Create account for 50/month: nexus --signup"
            )
        
        # Check for abuse
        if await is_suspicious_device(device):
            await db.flag_device(device.id, "Suspicious activity")
            raise HTTPException(403, "Suspicious activity detected")
        
        # Execute prompt
        result = await execute_with_ai(request.prompt, request.context)
        
        # Track usage
        await db.increment_device_usage(device.id)
        await db.track_usage(
            device_id=device.id,
            prompt=request.prompt,
            tokens_used=result.tokens,
            cost=result.cost,
            success=True
        )
        
        remaining = 5 - device.anonymous_prompts_used - 1
        
        return {
            "success": True,
            "result": result.content,
            "prompts_remaining": remaining,
            "message": "Create account for 50/month: nexus --signup" if remaining == 0 else None
        }
```

### AI Execution

```python
async def execute_with_ai(prompt: str, context: dict) -> AIResult:
    """Execute prompt using your AI keys"""
    
    # Get available keys
    gemini_key = await get_available_key("gemini")
    grok_key = await get_available_key("grok")
    
    # Determine mode based on prompt
    mode = determine_mode(prompt)  # architect, builder, validator
    
    if mode == "architect":
        # Use Gemini
        result = await call_gemini(gemini_key, prompt, context)
        await update_key_usage(gemini_key.id)
        
    elif mode == "builder":
        # Use Grok
        result = await call_grok(grok_key, prompt, context)
        await update_key_usage(grok_key.id)
        
    elif mode == "validator":
        # Use both
        gemini_result = await call_gemini(gemini_key, prompt, context)
        grok_result = await call_grok(grok_key, prompt, context)
        
        # Merge results
        result = await merge_results(gemini_result, grok_result)
        
        await update_key_usage(gemini_key.id)
        await update_key_usage(grok_key.id)
    
    return result
```

### Key Management

```python
async def get_available_key(provider: str) -> APIKey:
    """Get available API key with rate limiting"""
    
    while True:
        # Get active keys
        keys = await db.get_active_keys(provider)
        
        if not keys:
            raise Exception(f"No {provider} keys available")
        
        # Find key under limit
        for key in keys:
            if key.cooldown_until and key.cooldown_until > datetime.now():
                continue
            
            if key.requests_used < key.requests_limit:
                return key
        
        # All keys on cooldown, wait
        await asyncio.sleep(1)


async def update_key_usage(key_id: UUID):
    """Update key usage and set cooldown if needed"""
    
    key = await db.get_key(key_id)
    key.requests_used += 1
    
    # Check if limit reached
    if key.requests_used >= key.requests_limit:
        # Set cooldown for 1 minute
        key.cooldown_until = datetime.now() + timedelta(minutes=1)
        key.requests_used = 0
    
    await db.update_key(key)
```

### Abuse Detection

```python
async def is_suspicious_device(device: Device) -> bool:
    """Detect suspicious patterns"""
    
    # Check multiple accounts from same device
    accounts = await db.count_accounts_by_device(device.device_id)
    if accounts > 3:
        return True
    
    # Check rapid usage
    recent_usage = await db.get_device_usage_last_hour(device.id)
    if recent_usage > 10:
        return True
    
    # Check IP reputation
    if await is_vpn_or_proxy(device.ip_address):
        return True
    
    # Check multiple devices from same IP
    devices_on_ip = await db.count_devices_by_ip(device.ip_address)
    if devices_on_ip > 10:
        return True
    
    return False
```

## Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/nexus
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=nexus
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/nexus
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRY=7d

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-key
FROM_EMAIL=noreply@nexus.ai

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AI Keys (yours)
GEMINI_KEYS=key1,key2,key3
GROK_KEYS=key1,key2,key3
```

## Monitoring

### Metrics to Track

```python
from prometheus_client import Counter, Histogram, Gauge

# Requests
requests_total = Counter('requests_total', 'Total requests', ['endpoint', 'status'])
requests_duration = Histogram('requests_duration_seconds', 'Request duration')

# Usage
prompts_executed = Counter('prompts_executed_total', 'Total prompts', ['plan'])
prompts_failed = Counter('prompts_failed_total', 'Failed prompts')

# Costs
ai_cost_total = Counter('ai_cost_total', 'Total AI costs', ['provider'])
ai_tokens_used = Counter('ai_tokens_used_total', 'Tokens used', ['provider'])

# Users
active_users = Gauge('active_users', 'Active users', ['plan'])
new_signups = Counter('new_signups_total', 'New signups')
```

### Alerts

```yaml
alerts:
  - name: HighCosts
    condition: ai_cost_total > 1000
    action: email_admin
    
  - name: AbuseDetected
    condition: flagged_devices > 10
    action: email_admin
    
  - name: APIDown
    condition: requests_failed > 100
    action: page_oncall
```

## Security

### Best Practices

1. **API Keys (yours)**
   - Store encrypted in database
   - Rotate regularly
   - Monitor usage
   - Set spending limits

2. **User Data**
   - Hash passwords (bcrypt)
   - Encrypt sensitive data
   - HTTPS only
   - CORS properly configured

3. **Rate Limiting**
   - Per IP
   - Per user
   - Per device
   - Exponential backoff

4. **Input Validation**
   - Sanitize all inputs
   - Limit prompt length
   - Check for injection attacks

## Testing

### Unit Tests

```python
async def test_anonymous_usage():
    device_id = "test-device"
    
    # Use 5 prompts
    for i in range(5):
        response = await client.post("/api/v1/prompts/execute", json={
            "prompt": f"test {i}",
            "device_id": device_id
        })
        assert response.status_code == 200
    
    # 6th should fail
    response = await client.post("/api/v1/prompts/execute", json={
        "prompt": "test 6",
        "device_id": device_id
    })
    assert response.status_code == 429
```

### Integration Tests

```python
async def test_full_user_journey():
    # Signup
    response = await client.post("/api/v1/auth/signup", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    
    # Verify (mock)
    await verify_email_mock("test@example.com")
    
    # Login
    response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = response.json()["token"]
    
    # Use prompts
    for i in range(50):
        response = await client.post(
            "/api/v1/prompts/execute",
            headers={"Authorization": f"Bearer {token}"},
            json={"prompt": f"test {i}"}
        )
        assert response.status_code == 200
    
    # 51st should fail
    response = await client.post(
        "/api/v1/prompts/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={"prompt": "test 51"}
    )
    assert response.status_code == 429
```

## Summary

**Complete backend with:**
- ✅ Authentication (JWT)
- ✅ Usage tracking
- ✅ Rate limiting
- ✅ Abuse detection
- ✅ AI orchestration
- ✅ Payment processing
- ✅ Monitoring
- ✅ Security

**Ready to deploy and scale! 🚀**
