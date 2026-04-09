# NEXUS - Self-Evolving AI Coding Assistant

A multi-model AI coding system powered by NEX1, our advanced AI model that understands repos, plans tasks, executes changes, and learns from experience.

## What is NEXUS?

NEXUS is a CLI tool that uses the NEX1 AI model to help you code. It's designed as a SaaS where users never manage API keys - everything is handled on the backend.

**Key Features:**
- Powered by NEX1 advanced AI model
- Self-improving strategy engine
- Learns from past executions
- Simple CLI interface like Claude Code

## Quick Start

### Installation

**Linux/Mac:**
```bash
curl -fsSL https://nexus.ai/install.sh | bash
```

**Windows:**
```powershell
iex (iwr -Uri "https://nexus.ai/install.ps1").Content
```

### Usage

```bash
# Try it free - 5 prompts, no signup needed
nexus "list all Python files"

# Create account for 50 prompts/month (free)
nexus --signup

# Upgrade to Pro for unlimited
nexus --upgrade
```

## Pricing

- **Try Free**: 5 prompts (no signup)
- **Free Tier**: 50 prompts/month
- **Pro**: $29/month - Unlimited
- **Enterprise**: Custom pricing

## Architecture

```
CLI → Backend API → AI Key Pool → Gemini/Grok
```

Users interact with the CLI. Backend manages authentication, usage tracking, and AI orchestration.

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - User guide for the CLI
- **[TEST_CLI_NOW.md](TEST_CLI_NOW.md)** - How to test the CLI locally
- **[BACKEND.md](BACKEND.md)** - Backend implementation guide
- **[SAAS_MODEL.md](SAAS_MODEL.md)** - Business model and pricing

## Current Status

**Phase 1 (Complete):**
- ✅ CLI structure
- ✅ Orchestrator with planner/executor/evaluator agents
- ✅ Model abstraction (architect/builder/validator)
- ✅ Memory and strategy systems
- ✅ Rate limiting with key rotation

**Phase 2 (Next):**
- 🚧 Backend API (FastAPI)
- 🚧 Authentication system
- 🚧 Usage tracking
- 🚧 Stripe integration

## For Developers

### Testing Locally

1. Clone the repo
2. Add your API keys to `.env` (2-3 keys per provider, comma-separated)
3. Run `python demo.py` to see the UI
4. Run `python test_cli.py` to test functionality

See [TEST_CLI_NOW.md](TEST_CLI_NOW.md) for detailed testing instructions.

### Building the Backend

See [BACKEND.md](BACKEND.md) for complete backend implementation guide including:
- Database schema
- API endpoints
- Authentication flow
- Usage tracking
- Deployment guide

## License

MIT

## Support

- Documentation: https://docs.nexus.ai
- Support: support@nexus.ai
- Community: https://community.nexus.ai
