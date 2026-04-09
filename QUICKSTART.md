# NEXUS Quick Start Guide

## One-Line Installation

### Linux / macOS
```bash
curl -fsSL https://nexus.ai/install.sh | bash
```

Or with wget:
```bash
wget -qO- https://nexus.ai/install.sh | bash
```

### Windows (PowerShell)
```powershell
iex (iwr -Uri "https://nexus.ai/install.ps1").Content
```

The installer will set up everything automatically!

## First Use - No Signup Required!

Try NEXUS immediately with **5 free prompts**:

```bash
$ nexus "list all Python files in this directory"

✓ Task complete!

Free prompts remaining: 4/5
Want unlimited? Run: nexus --signup
```

**No account needed for your first 5 prompts!**

## After Free Prompts

Once you've used your 5 free prompts:

```bash
$ nexus "another task"

⚠️  Free prompts used (5/5)

Create a free account for 50 more prompts/month:
  nexus --signup

Or upgrade to Pro for unlimited:
  nexus --upgrade
```

## Create Account (Free Tier)

```bash
$ nexus --signup

Create your NEXUS account

Email: you@example.com
Password: ********
Confirm: ********

✓ Account created!
✓ 50 prompts/month activated

Prompts remaining: 50/50
```

## Pricing

### Try It Free
- **5 prompts** - No signup required
- Perfect for testing

### Free Tier
- **50 prompts/month** - Requires free account
- Basic features
- Community support

### Pro ($29/month)
- **Unlimited prompts**
- Advanced features
- Priority support
- Faster execution

### Enterprise (Custom)
- Custom deployment
- SLA guarantees
- Dedicated support
- Team features

**Start with 5 free prompts - no signup needed!**

## Basic Usage

### Single Task Execution

```bash
# Fix a bug
nexus "fix the authentication bug in auth.py"

# Add a feature
nexus "add input validation to the user registration form"

# Refactor code
nexus "refactor the database queries to use connection pooling"
```

### Interactive Mode

```bash
nexus --interactive

nexus> analyze the codebase structure
nexus> find all TODO comments
nexus> optimize the slow database queries
nexus> exit
```

### Check Status

```bash
nexus --status
```

Shows:
- Prompts used this month
- Remaining prompts
- Account tier
- Success rate

## Example Session

```bash
$ nexus "add error handling to api.py"

╭─────────────────────────────────────╮
│ NEXUS Starting                      │
│ Task: add error handling to api.py  │
╰─────────────────────────────────────╯

  → Analyzing code...
  → Planning approach...
  → Executing changes...
  → Validating results...

╭─────────────────────────────────────╮
│ Result                              │
│                                     │
│ Added error handling to api.py:     │
│ - Wrapped database calls in try     │
│ - Added custom exception classes    │
│ - Implemented error logging         │
│ - Added user-friendly error msgs    │
╰─────────────────────────────────────╯

Free prompts remaining: 3/5
Create account for 50/month: nexus --signup
```

## Account Management

### Create Account (Free)
```bash
nexus --signup

Email: you@example.com
Password: ********

✓ Account created!
✓ 50 prompts/month activated
```

### Login
```bash
nexus --login

Email: you@example.com
Password: ********

✓ Logged in
Prompts: 42/50 remaining
```

### Check Usage
```bash
nexus --usage

Account: you@example.com
Plan: Free
Prompts used: 8/50
Resets: Jan 1, 2026
```

### Upgrade Plan
```bash
nexus --upgrade

Current: Free (8/50 prompts)

Upgrade to Pro?
✓ Unlimited prompts
✓ Priority support
✓ Advanced features

$29/month

Visit: https://nexus.ai/upgrade
```

### Logout
```bash
nexus --logout
✓ Logged out

Note: You still have 5 free prompts (no account)
```

## How It Works

1. **You describe the task** in natural language
2. **Planner analyzes** and creates steps
3. **Executor performs** each step
4. **Evaluator checks** correctness
5. **System learns** from the execution
6. **You get results** with clear output

## Tips

### Be Specific
❌ "fix the bug"
✓ "fix the null pointer exception in user_service.py line 45"

### Provide Context
❌ "add tests"
✓ "add unit tests for the authentication module using pytest"

### One Task at a Time
❌ "fix bugs and add features and refactor everything"
✓ "fix the login timeout bug" (then run again for next task)

## Understanding Output

### Step Messages
- `→` indicates current action
- Green panel = success
- Red panel = error
- Yellow = warning/retry

### Result Types
- **Code changes**: Shows what was modified
- **Analysis**: Provides insights
- **Errors**: Explains what went wrong

## Troubleshooting

## Troubleshooting

### "Free prompts exhausted"
```bash
# Create free account for 50/month
nexus --signup

# Or upgrade to unlimited
nexus --upgrade
```

### "Authentication failed"
```bash
# Re-login
nexus --login
```

### "Account limit reached"
```bash
# Check usage
nexus --usage

# Upgrade to Pro for unlimited
nexus --upgrade
```

### "Command not found: nexus"
```bash
# Add to PATH (Linux/Mac)
export PATH="$HOME/.local/bin:$PATH"

# Windows: Restart terminal after installation
```

### "Cannot create multiple accounts"
```bash
# Device limit reached
# Each device gets 5 free prompts
# Create one account per person
# Contact support for legitimate multi-device use
```

## Anti-Abuse Protection

NEXUS uses device fingerprinting to prevent abuse:
- 5 free prompts per device (no signup)
- One free account per person
- Device tracking prevents multiple account creation
- Fair use for legitimate users

If you need multiple devices:
- Use the same account on all devices
- Pro plan supports unlimited devices
- Enterprise for teams

## Support

- Documentation: https://docs.nexus.ai
- Support: support@nexus.ai
- Status: https://status.nexus.ai
- Community: https://community.nexus.ai

## Privacy & Security

- Device fingerprinting for abuse prevention only
- Your code never leaves your machine during analysis
- Only task descriptions and results sent to servers
- All data encrypted in transit and at rest
- See privacy policy: https://nexus.ai/privacy

## Next Steps

1. ✅ Try your 5 free prompts
2. ✅ Create account for 50/month
3. ✅ Explore interactive mode
4. ✅ Upgrade to Pro if you love it
5. ✅ Join our community

## Advanced Usage

### Custom Strategies

NEXUS learns automatically, but you can seed strategies:

```bash
# Create .nexus/strategies/my_strategy.json
{
  "name": "my_custom_approach",
  "description": "Always write tests first",
  "success_rate": 0.5,
  "usage_count": 0
}
```

### Memory Inspection

```bash
# View past executions
ls .nexus/memory/

# Read specific memory
cat .nexus/memory/memory_20260409_143022.json
```

### Integration with Git

```bash
# Create a git alias
git config alias.ai '!python -m nexus'

# Use it
git ai "fix the merge conflicts in config.py"
```

## Next Steps

1. Try the examples above
2. Run on your own codebase
3. Check `ARCHITECTURE.md` for details
4. See `ROADMAP.md` for upcoming features
5. Contribute improvements!

## Getting Help

- Check logs in `.nexus/`
- Run with `--status` to see system state
- Review `ARCHITECTURE.md` for internals
- Open an issue on GitHub
