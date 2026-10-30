## Description
Briefly describe the purpose of this Pull Request and the changes introduced.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement / Refactoring

## Subsystems Modified
- [ ] Decentralized Identity (`did:key`, Verifiable Credentials)
- [ ] Behavioral Trust Engine & EMA Scoring
- [ ] Zero-Trust Policy Interception (`AdaptivePolicyEnforcer`)
- [ ] Agent Discovery & Multi-Factor Matching Algorithm
- [ ] Collaboration Sessions & Sequential Workflows
- [ ] SQLite VDR & Database Schema
- [ ] React 19 Frontend SOC Dashboard
- [ ] Automated Test Suite & CI

## Verification Checklist
- [ ] My code follows the code style and architectural principles of TrustChain-AI.
- [ ] I have executed the automated test suite (`pytest tests/`) and all tests pass (80/80).
- [ ] I have executed the frontend build (`npm run build` in `frontend/`) and it builds without errors.
- [ ] I have verified that no hardcoded paths or sensitive credentials (`.env`, `vdr.db`) are introduced.
- [ ] Relevant documentation has been updated.
