# Limitations

This document explicitly defines the boundaries and known limitations of the TrustChain-AI implementation.

1. **Telemetry Authenticity Limitation**: Telemetry is currently ingested directly from the API gateway executing the agent's request. There is no decentralized consensus attesting to the telemetry, nor are the telemetry events currently signed by the API provider to guarantee non-repudiation.
2. **Prototype Trust Boundary**: The framework currently operates entirely within a single Python instance. Agents do not negotiate trust peer-to-peer across distributed networks in this prototype.
3. **SQLite Limitations**: Trust states and logs are persisted in a local `vdr.db` SQLite database. This provides zero Byzantine fault tolerance, limited concurrency, and no decentralized immutability.
4. **No Blockchain Claim**: This system is explicitly **NOT** blockchain-backed. Historical claims in the research draft proposing blockchain integration were not supported by the implementation phase.
5. **No Production-Security Claim**: This is an academic research prototype. It is NOT production-ready, enterprise-ready, or fully secure against determined cryptographic or side-channel attacks.
