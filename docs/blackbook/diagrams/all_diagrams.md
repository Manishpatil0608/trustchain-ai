# TrustChain-AI — System Architecture Diagrams

All diagrams are in Mermaid syntax. Render with any Mermaid-compatible renderer.

---

## Figure 1: Overall System Architecture

```mermaid
flowchart TB
    subgraph UI["Frontend — React 19 / Vite 8"]
        A1[DashboardHome]
        A2[AgentExplorer]
        A3[TrustAnalytics]
        A4[CollaborationCenter]
        A5[WorkflowCenter]
        A6[IdentityCredentials]
        A7[AuditTrail]
        A8[SystemHealth]
        A9[AuthorizationVisualizer]
        A10[TelemetryCenter]
    end

    subgraph API["Backend — FastAPI 0.141 / Uvicorn"]
        B1[Auth Router /auth]
        B2[Registry Router /registry]
        B3[VDR Router /vdr]
        B4[Health Endpoint /health]
    end

    subgraph CORE["Trust Intelligence Core"]
        C1[TrustEngine]
        C2[AdaptivePolicyEnforcer]
        C3[LocalAgentConnector]
        C4[DIDKey Generator]
        C5[VerifiableCredential]
    end

    subgraph DB["Local SQLite VDR — vdr.db"]
        D1[(agent_trust_states)]
        D2[(telemetry_logs)]
        D3[(trust_audit_trails)]
        D4[(agents)]
        D5[(stored_vcs)]
        D6[(workflows / nodes)]
        D7[(collaboration_sessions)]
        D8[(users / tokens)]
    end

    UI -->|Axios HTTP / JWT Bearer| API
    API --> CORE
    CORE --> DB
    B1 --> D8
    B2 --> D4
    B2 --> D1
    B2 --> D2
    B2 --> D3
    B2 --> D6
    B2 --> D7
    B3 --> D5
    C1 --> D1
    C1 --> D2
    C2 --> C1
    C3 --> D4
```

---

## Figure 2: Layered Architecture

```mermaid
flowchart TB
    L1["Presentation Layer\nReact 19 · Vite 8 · Recharts · Tailwind CSS 4\nDark / Light Theme Toggle"]
    L2["API Gateway Layer\nFastAPI · JWT Authentication · RBAC\nPydantic v2 Validation · OpenTelemetry Instrumentation"]
    L3["Trust Intelligence Layer\nTrustEngine — Temporal EMA Trust Scoring\nAdaptivePolicyEnforcer — Operation-level Authorization\nLocalAgentConnector — Structured Task Execution Engine"]
    L4["Identity & Credential Layer\nDID:key — Ed25519 Multibase\nVerifiableCredential — Ed25519Signature2020\nJSON-LD Canonicalization · PyNaCl Crypto"]
    L5["Persistence Layer\nSQLite VDR — WAL Mode\nSQLAlchemy 2.0 ORM\n14 Tables · Trust Audit Trail"]

    L1 --> L2 --> L3 --> L4 --> L5
```

---

## Figure 3: Trust Evaluation Flowchart

```mermaid
flowchart TD
    A[Telemetry Event Submitted] --> B[Load Last 10 Events for Agent]
    B --> C["Compute S_i(t) = success_count / n"]
    C --> D["Compute C_i(t) = compliance_count / n"]
    D --> E["Compute L_i(t) = avg_latency_ms / 2000 capped at 1.0"]
    E --> F["P_i(t) = 0.6 × S_i(t) + 0.3 × C_i(t) + 0.1 × (1 − L_i(t))"]
    F --> G[Load prior T_i(t-1) from agent_trust_states]
    G --> H["T_i(t) = 0.7 × P_i(t) + 0.3 × T_i(t-1)"]
    H --> I{T_i(t) threshold?}
    I -->|T >= 0.8| J[State = TRUSTED]
    I -->|0.5 <= T < 0.8| K[State = SUSPICIOUS]
    I -->|T < 0.5| L[State = QUARANTINED]
    J --> M[Update agent_trust_states]
    K --> M
    L --> M
    M --> N[Write trust_audit_trail record]
    N --> O[Return updated trust score + state]
```

---

## Figure 4: Trust State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> TRUSTED : Agent Registered (initial score = 1.0)
    TRUSTED --> SUSPICIOUS : T drops below 0.8 (behavioural degradation)
    TRUSTED --> QUARANTINED : T drops below 0.5 (severe failures)
    SUSPICIOUS --> TRUSTED : T recovers >= 0.8
    SUSPICIOUS --> QUARANTINED : T drops below 0.5
    QUARANTINED --> SUSPICIOUS : T recovers >= 0.5
    QUARANTINED --> REVOKED : Admin revocation command
    SUSPICIOUS --> REVOKED : Admin revocation command
    TRUSTED --> REVOKED : Admin revocation command
    REVOKED --> [*] : Terminal — no automatic recovery
```

---

## Figure 5: Adaptive Authorization Flow

```mermaid
flowchart TD
    A[Operation Request] --> B[Lookup Agent Trust State]
    B --> C{Trust State?}
    C -->|REVOKED| D[HTTP 403 — Permanently Revoked]
    C -->|QUARANTINED| E[HTTP 403 — Agent Quarantined]
    C -->|TRUSTED| F[Permit Operation — Log Audit]
    C -->|SUSPICIOUS| G{Operation Type?}
    G -->|PRIVILEGED| H["HTTP 403 — AuthorizationError\nPrivileged ops denied for SUSPICIOUS agents"]
    G -->|STANDARD| I["Permit with Audit Record\nLow-risk ops allowed with heightened monitoring"]
    H --> J[Write security_audit_event]
    I --> J
    F --> J
```

---

## Figure 6: Agent Discovery and Matching

```mermaid
flowchart TD
    A[Discovery Request with required_capability] --> B[Filter Registry: active agents]
    B --> C[Filter: agent has required_capability]
    C --> D[Filter: trust_state NOT QUARANTINED or REVOKED]
    D --> E[For each candidate agent compute match_score]
    E --> F["match_score = 0.4 × trust_score\n+ 0.3 × (reputation_score / 5.0)\n+ 0.2 × success_rate\n+ 0.1 × (1 − normalized_latency)"]
    F --> G[Sort by match_score descending]
    G --> H[Return ranked candidate list]
```

---

## Figure 7: Sequential Workflow Execution

```mermaid
sequenceDiagram
    participant O as Operator
    participant API as Registry API
    participant N1 as Node 1 — Research Agent
    participant N2 as Node 2 — Analysis Agent
    participant N3 as Node 3 — Verification Agent
    participant DB as SQLite VDR

    O->>API: POST /registry/workflows (SEQUENTIAL pattern)
    API->>DB: Insert workflow + nodes (step_order 0,1,2)
    O->>API: POST /registry/workflows/{id}/execute
    API->>N1: Execute step 0 via LocalAgentConnector
    N1-->>API: Output data (research result)
    API->>DB: Update node 0 status=completed, output_data
    API->>N2: Execute step 1 with node 0 output as input
    N2-->>API: Output data (analysis result)
    API->>DB: Update node 1 status=completed
    API->>N3: Execute step 2 with node 1 output as input
    N3-->>API: Output data (verification result)
    API->>DB: Update node 2 + workflow status=completed
    API-->>O: Workflow result
```

---

## Figure 8: Collaboration Session Lifecycle

```mermaid
sequenceDiagram
    participant R as Requester Agent
    participant API as Registry API
    participant T as Target Agent
    participant DB as SQLite VDR

    R->>API: POST /registry/collaborate (requester_did, target_did, task)
    API->>DB: Check both agents trust_state != QUARANTINED/REVOKED
    API->>DB: Insert collaboration_session (status=active)
    API-->>R: session_id

    R->>API: POST /collaborations/{id}/message (task_request)
    API->>DB: Insert collaboration_event
    API->>T: Invoke LocalAgentConnector for task
    T-->>API: Task response
    API->>DB: Insert collaboration_event (response)
    API-->>R: Response content

    R->>API: POST /collaborations/{id}/complete
    API->>DB: Update session status=completed, task_result, productivity_score
    API->>DB: Submit telemetry for both agents
    API-->>R: Completed session details
```

---

## Figure 9: Database Entity-Relationship Diagram

```mermaid
erDiagram
    agents {
        varchar agent_id PK
        varchar did UK
        varchar name
        text capabilities
        varchar status
        float reputation_score
        integer successful_tasks
        integer total_tasks
    }
    agent_trust_states {
        integer id PK
        varchar agent_did FK
        float temporal_trust_score
        varchar trust_state
        datetime last_updated
    }
    telemetry_logs {
        integer id PK
        varchar agent_did FK
        boolean success
        boolean compliance_event
        float latency_ms
        datetime timestamp
    }
    trust_audit_trails {
        integer id PK
        varchar agent_did FK
        varchar previous_state
        varchar new_state
        float previous_score
        float new_score
        text reason
        datetime timestamp
    }
    stored_vcs {
        varchar vc_id PK
        varchar issuer_did
        varchar subject_did
        varchar credential_type
        text credential_data
    }
    collaboration_sessions {
        varchar session_id PK
        varchar requester_did FK
        varchar target_did FK
        varchar status
        text task_result
    }
    collaboration_events {
        varchar event_id PK
        varchar session_id FK
        varchar sender_did
        varchar message_type
        text content
    }
    workflows {
        varchar workflow_id PK
        varchar name
        varchar pattern
        varchar status
    }
    workflow_nodes {
        varchar node_id PK
        varchar workflow_id FK
        varchar agent_did FK
        integer step_order
        varchar status
        text output_data
    }
    users {
        integer user_id PK
        varchar username UK
        varchar role
        varchar password_hash
        boolean is_active
    }
    refresh_tokens {
        integer id PK
        varchar jti UK
        integer user_id FK
        datetime expires_at
        datetime revoked_at
    }
    security_audit_events {
        integer event_id PK
        integer user_id FK
        varchar event_type
        varchar ip_address
        datetime timestamp
    }

    agents ||--o{ agent_trust_states : "tracked by"
    agents ||--o{ telemetry_logs : "submits"
    agents ||--o{ trust_audit_trails : "audited in"
    agents ||--o{ workflow_nodes : "assigned to"
    workflows ||--|{ workflow_nodes : "contains"
    collaboration_sessions ||--|{ collaboration_events : "contains"
    users ||--o{ refresh_tokens : "holds"
    users ||--o{ security_audit_events : "generates"
```

---

## Figure 10: DID Key Generation Flowchart

```mermaid
flowchart TD
    A[Generate DID Request] --> B[Generate Ed25519 keypair via PyNaCl]
    B --> C["Extract 32-byte public key"]
    C --> D["Prepend multicodec prefix: 0xED 0x01"]
    D --> E["Base58-encode prefixed bytes → multibase string (z-prefix)"]
    E --> F["Construct DID: did:key:z{multibase_string}"]
    F --> G["Build DID Document:\n- id = DID\n- verificationMethod: Ed25519VerificationKey2020\n- authentication, assertionMethod references"]
    G --> H[Return DID + DID Document + private key]
```

---

## Figure 11: System Context Diagram

```mermaid
flowchart TB
    subgraph EXT["External Actors"]
        U1[ADMIN Operator]
        U2[OPERATOR User]
        U3[VIEWER User]
        AI[Autonomous AI Agents]
    end

    subgraph SYS["TrustChain-AI Platform"]
        FE[React Dashboard Frontend]
        BE[FastAPI Backend]
        TC[Trust Intelligence Core]
        VDR[Local SQLite VDR]
    end

    U1 -->|HTTPS Browser| FE
    U2 -->|HTTPS Browser| FE
    U3 -->|HTTPS Browser| FE
    AI -->|REST API / JWT| BE
    FE -->|REST API / JWT| BE
    BE --> TC
    TC --> VDR
```

---

## Figure 12: Security Architecture

```mermaid
flowchart LR
    subgraph AUTH["Authentication Layer"]
        A1[Argon2id Password Hashing]
        A2[JWT Access Token — 30 min TTL]
        A3[JWT Refresh Token — 7 day TTL with rotation]
        A4[Account Lockout after 5 failed attempts]
    end
    subgraph AUTHZ["Authorization Layer"]
        B1[RBAC — ADMIN / OPERATOR / VIEWER]
        B2[Trust-Aware Adaptive Policy — PRIVILEGED vs STANDARD ops]
        B3[QUARANTINED / REVOKED block all operations]
    end
    subgraph CRYPTO["Cryptographic Layer"]
        C1[Ed25519 keypair generation via PyNaCl]
        C2[did:key method — Ed25519VerificationKey2020]
        C3[Ed25519Signature2020 — VC signing and verification]
        C4[JSON-LD canonicalization via PyLD]
    end
    subgraph AUDIT["Audit Layer"]
        D1[security_audit_events table]
        D2[trust_audit_trails table]
        D3[collaboration_events log]
    end

    AUTH --> AUTHZ --> CRYPTO
    AUTHZ --> AUDIT
```
