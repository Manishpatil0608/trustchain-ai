"""
Generates TrustChain_AI_Architecture_and_Diagrams.pdf
Contains all system architecture and workflow diagrams formatted for documentation.
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

BASE_DIR = Path(__file__).parent
PDF_OUT = BASE_DIR / "TrustChain_AI_Architecture_and_Diagrams.pdf"

doc = SimpleDocTemplate(
    str(PDF_OUT),
    pagesize=A4,
    leftMargin=1.0*inch, rightMargin=1.0*inch,
    topMargin=1.0*inch, bottomMargin=1.0*inch,
    title="TrustChain-AI Architecture & Diagrams Collection",
    author="TrustChain-AI Project Team",
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', fontName='Times-Bold', fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=12)
sub_style = ParagraphStyle('Sub', fontName='Times-Roman', fontSize=14, leading=18, alignment=TA_CENTER, spaceAfter=20)
h1_style = ParagraphStyle('H1', fontName='Times-Bold', fontSize=16, leading=22, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#1a365d'))
h2_style = ParagraphStyle('H2', fontName='Times-Bold', fontSize=12, leading=16, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#2d3748'))
body_style = ParagraphStyle('Body', fontName='Times-Roman', fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
code_style = ParagraphStyle('Code', fontName='Courier', fontSize=8, leading=10, leftIndent=0.2*inch, spaceAfter=6)
caption_style = ParagraphStyle('Caption', fontName='Times-Italic', fontSize=10, leading=12, alignment=TA_CENTER, spaceAfter=8, textColor=colors.HexColor('#4a5568'))

diagrams = [
    {
        "num": "1",
        "title": "Overall System Architecture",
        "category": "High-Level Architecture",
        "desc": "Illustrates the end-to-end integration across the React 19 Frontend SPA, FastAPI ASGI Backend, Trust Intelligence Core (TrustEngine, AdaptivePolicyEnforcer, LocalAgentConnector), and the 14-table local SQLite Verifiable Data Registry.",
        "mermaid": """flowchart TB
    subgraph UI["Frontend — React 19 / Vite 8"]
        A1[DashboardHome]
        A2[AgentExplorer]
        A3[TrustAnalytics]
        A4[CollaborationCenter]
        A5[WorkflowCenter]
        A6[IdentityCredentials]
        A7[AuditTrail]
        A8[SystemHealth]
    end

    subgraph API["Backend — FastAPI 0.141 / Uvicorn"]
        B1[Auth Router /auth]
        B2[Registry Router /registry]
        B3[VDR Router /vdr]
        B4[Health Endpoint /health]
    end

    subgraph CORE["Trust Intelligence Core"]
        C1[TrustEngine — EMA Math]
        C2[AdaptivePolicyEnforcer]
        C3[LocalAgentConnector]
        C4[DIDKey Generator]
        C5[VerifiableCredential]
    end

    subgraph DB["Local SQLite VDR — vdr.db (WAL Mode)"]
        D1[(agent_trust_states)]
        D2[(telemetry_logs)]
        D3[(trust_audit_trails)]
        D4[(agents)]
        D5[(stored_vcs)]
        D6[(workflows & nodes)]
        D7[(collaboration_sessions)]
        D8[(users & refresh_tokens)]
    end

    UI -->|Axios REST / JWT Bearer| API
    API --> CORE
    CORE --> DB"""
    },
    {
        "num": "2",
        "title": "Five-Layer Layered Architecture",
        "category": "Architectural Design",
        "desc": "Details the strict separation of concerns from presentation down to persistence, ensuring modularity, testability, and standard-aligned interoperability.",
        "mermaid": """flowchart TB
    L1["Layer 1: Presentation Layer
React 19.2 · Vite 8.2 · Recharts · Tailwind CSS · Dark/Light Mode"]
    L2["Layer 2: API Gateway Layer
FastAPI 0.141 · Uvicorn ASGI · JWT Authentication · RBAC · Pydantic v2"]
    L3["Layer 3: Trust Intelligence Layer
TrustEngine (EMA Scoring) · AdaptivePolicyEnforcer · LocalAgentConnector"]
    L4["Layer 4: Identity & Credential Layer
DID:key (Ed25519 Multibase) · VerifiableCredential (Ed25519Signature2020)"]
    L5["Layer 5: Persistence Layer
SQLite VDR (WAL Mode) · SQLAlchemy 2.0 ORM · 14 Relational Tables"]

    L1 --> L2 --> L3 --> L4 --> L5"""
    },
    {
        "num": "3",
        "title": "System Context Diagram (C4 Level 1)",
        "category": "Context & Boundaries",
        "desc": "Depicts external human actors (Admin, Operator, Viewer) and Autonomous AI Agents interfacing with the TrustChain-AI boundary over HTTPS and REST interfaces.",
        "mermaid": """flowchart TB
    subgraph Actors["External Actors"]
        A1[System Administrator — Full RBAC]
        A2[Operations Engineer — Agent Operator]
        A3[Security Auditor — Read-Only Viewer]
        A4[Autonomous AI Agents — Workflows & Tasks]
    end

    subgraph Platform["TrustChain-AI Platform Boundary"]
        FE[React 19 Web Dashboard]
        BE[FastAPI REST Application (:8050)]
        TE[Trust & Policy Evaluation Core]
        DB[(SQLite Verifiable Data Registry)]
    end

    A1 -->|Browser / HTTPS| FE
    A2 -->|Browser / HTTPS| FE
    A3 -->|Browser / HTTPS| FE
    A4 -->|REST API / Bearer Token| BE
    FE -->|JSON REST Requests| BE
    BE --> TE
    TE --> DB"""
    },
    {
        "num": "4",
        "title": "DID:key Generation & Verification Flowchart",
        "category": "Identity & Cryptography",
        "desc": "Step-by-step cryptographic sequence for generating W3C-conformant did:key identifiers using PyNaCl Ed25519 keypairs and multibase base58btc encoding.",
        "mermaid": """flowchart TD
    Start([Generate Key Request]) --> K[PyNaCl: Generate Ed25519 Keypair]
    K --> Raw[Extract 32-Byte Public Key]
    Raw --> Pre[Prepend Multicodec Header: 0xED 0x01]
    Pre --> B58[Base58BTC Encode Prefixed Bytes]
    B58 --> Z[Prefix with 'z' -> Multibase String]
    Z --> DID[Format URI: did:key:z{multibase}]
    DID --> Doc[Assemble W3C DID Document:
- VerificationMethod: Ed25519VerificationKey2020
- Relationships: authentication, assertionMethod]
    Doc --> Out([Return DID + Document + Private Key])"""
    },
    {
        "num": "5",
        "title": "Verifiable Credential Issuance & Verification Sequence",
        "category": "Credential Lifecycle",
        "desc": "UML sequence diagram illustrating VC creation, URDNA2015 canonicalization via PyLD, Ed25519 signing via PyNaCl, and cryptographic verification against issuer public keys.",
        "mermaid": """sequenceDiagram
    participant Issuer as Issuer Agent / Admin
    participant VDR as VDR Service (/vdr)
    participant PyLD as PyLD (URDNA2015)
    participant PyNaCl as PyNaCl (Ed25519)
    participant DB as SQLite stored_vcs

    Issuer->>VDR: POST /vdr/credentials (claims, subject_did)
    VDR->>PyLD: Canonicalize JSON-LD structure (URDNA2015)
    PyLD-->>VDR: Deterministic byte payload
    VDR->>PyNaCl: Sign canonical payload with Issuer Private Key
    PyNaCl-->>VDR: 64-byte Ed25519 digital signature
    VDR->>VDR: Assemble Ed25519Signature2020 proof block
    VDR->>DB: Persist complete VC in stored_vcs
    VDR-->>Issuer: Return Verified Credential JSON-LD"""
    },
    {
        "num": "6",
        "title": "Behavioral Trust Evaluation Flowchart",
        "category": "Trust Mathematics",
        "desc": "Flowchart representing the ingestion of telemetry events, calculation of multi-factor performance score P_i(t), temporal smoothing via EMA T_i(t), and state transition evaluation.",
        "mermaid": """flowchart TD
    A[Telemetry Submission: success, compliance, latency] --> B[Log into telemetry_logs]
    B --> C[Query Last n=10 Events for Agent DID]
    C --> D["Calculate Success Rate S_i = successes / n"]
    D --> E["Calculate Compliance Rate C_i = compliances / n"]
    E --> F["Calculate Normalised Latency L_i = min(avg_lat/2000, 1.0)"]
    F --> G["Compute Performance: P_i(t) = 0.6*S_i + 0.3*C_i + 0.1*(1-L_i)"]
    G --> H["Load Prior Temporal Score T_i(t-1) (default 1.0)"]
    H --> I["Compute EMA: T_i(t) = 0.7*P_i(t) + 0.3*T_i(t-1)"]
    I --> J{T_i(t) Threshold Check}
    J -->|T >= 0.8| K[State: TRUSTED]
    J -->|0.5 <= T < 0.8| L[State: SUSPICIOUS]
    J -->|T < 0.5| M[State: QUARANTINED]
    K --> N[Update agent_trust_states]
    L --> N
    M --> N
    N --> O[Write audit trail record into trust_audit_trails]"""
    },
    {
        "num": "7",
        "title": "Trust State Transition Finite State Machine",
        "category": "State Machine",
        "desc": "Finite State Automaton showing bidirectional dynamic transitions between TRUSTED, SUSPICIOUS, and QUARANTINED states, and the one-way terminal transition to REVOKED.",
        "mermaid": """stateDiagram-v2
    [*] --> TRUSTED: Agent Registered (T_0 = 1.0)
    TRUSTED --> SUSPICIOUS: T drops below 0.8 (Degradation)
    TRUSTED --> QUARANTINED: T drops below 0.5 (Severe Failure)
    SUSPICIOUS --> TRUSTED: T recovers >= 0.8 (Healthy Telemetry)
    SUSPICIOUS --> QUARANTINED: T drops below 0.5 (Continued Failure)
    QUARANTINED --> SUSPICIOUS: T recovers >= 0.5 (Telemetry Recovery)
    TRUSTED --> REVOKED: Administrative Revocation
    SUSPICIOUS --> REVOKED: Administrative Revocation
    QUARANTINED --> REVOKED: Administrative Revocation
    REVOKED --> [*]: Terminal State (No Recovery)"""
    },
    {
        "num": "8",
        "title": "Adaptive Authorization Flow",
        "category": "Security & Policy",
        "desc": "Decision tree executed by AdaptivePolicyEnforcer for gating incoming operations based on the requesting agent's live trust classification.",
        "mermaid": """flowchart TD
    Req[Incoming Agent Request: DID + Operation] --> Query[Fetch Live Trust State from VDR]
    Query --> Check{Trust State?}
    Check -->|REVOKED| DenyRev[HTTP 403 Forbidden: Permanently Revoked]
    Check -->|QUARANTINED| DenyQ[HTTP 403 Forbidden: Quarantined Agent]
    Check -->|TRUSTED| Allow[HTTP 200: Authorize Operation]
    Check -->|SUSPICIOUS| OpCheck{Operation Category?}
    OpCheck -->|PRIVILEGED| DenyPriv[HTTP 403 Forbidden: Privileged Op Denied]
    OpCheck -->|STANDARD| AllowAudit[HTTP 200: Authorize + Log Security Audit Event]"""
    },
    {
        "num": "9",
        "title": "Agent Discovery & Trust-Weighted Candidate Matching",
        "category": "Multi-Agent Coordination",
        "desc": "Algorithmic pipeline for filtering available agents by requested capability and computing ranked composite scores based on trust, reputation, success rate, and latency.",
        "mermaid": """flowchart TD
    Req[Task Request: Required Capability] --> FilterCap[Filter agents table by capability tag]
    FilterCap --> FilterState[Exclude agents in QUARANTINED or REVOKED states]
    FilterState --> ScoreLoop[For each qualifying agent:]
    ScoreLoop --> MatchMath["Compute match_score =
0.4*T_i + 0.3*(reputation/5.0) + 0.2*success_rate + 0.1*(1 - norm_latency)"]
    MatchMath --> Rank[Sort candidates descending by match_score]
    Rank --> Result[Return ordered list of ranked agent endpoints]"""
    },
    {
        "num": "10",
        "title": "Sequential Multi-Agent Workflow Execution",
        "category": "Workflow Orchestration",
        "desc": "End-to-end execution of a 3-stage sequential workflow pipeline (Research -> Analysis -> Verification) showing data chaining and per-step trust validation.",
        "mermaid": """sequenceDiagram
    participant Op as Human Operator / API Client
    participant WF as Workflow Orchestrator
    participant Disc as Discovery & Trust Engine
    participant Ag1 as Node 1 (Research Agent)
    participant Ag2 as Node 2 (Analysis Agent)
    participant Ag3 as Node 3 (Verification Agent)

    Op->>WF: POST /registry/workflows/{id}/execute
    WF->>Disc: Verify Node 1 Agent Trust State
    Disc-->>WF: Trust OK (TRUSTED)
    WF->>Ag1: Execute Task (Initial Input Data)
    Ag1-->>WF: Output 1 (Research Dossier)
    WF->>Disc: Verify Node 2 Agent Trust State
    Disc-->>WF: Trust OK (TRUSTED)
    WF->>Ag2: Execute Task (Input = Output 1)
    Ag2-->>WF: Output 2 (Structured Analysis)
    WF->>Disc: Verify Node 3 Agent Trust State
    Disc-->>WF: Trust OK (TRUSTED)
    WF->>Ag3: Execute Task (Input = Output 2)
    Ag3-->>WF: Output 3 (Verification Verdict)
    WF->>Op: Return Workflow Result (Status: completed)"""
    },
    {
        "num": "11",
        "title": "Database Entity-Relationship Diagram (14 Relational Tables)",
        "category": "Database Architecture",
        "desc": "Entity relationship overview showing primary keys, foreign keys, and relational cardinality across the 14 SQLite VDR tables.",
        "mermaid": """erDiagram
    agents ||--o{ agent_trust_states : tracks
    agents ||--o{ telemetry_logs : records
    agents ||--o{ trust_audit_trails : logs
    agents ||--o{ agent_ratings : receives
    agents ||--o{ workflow_nodes : assigned
    workflows ||--|{ workflow_nodes : contains
    collaboration_sessions ||--|{ collaboration_events : logs
    users ||--o{ refresh_tokens : owns
    users ||--o{ security_audit_events : generates"""
    },
    {
        "num": "12",
        "title": "Security Architecture & Defense-in-Depth",
        "category": "Cybersecurity & Governance",
        "desc": "Holistic view of security enforcement layers including Argon2id hashing, JWT access/refresh rotation, RBAC, W3C cryptographic signatures, and immutable audit logs.",
        "mermaid": """flowchart LR
    subgraph AuthN["Authentication Layer"]
        A1[Argon2id Password Hashes]
        A2[JWT Access Token 30m]
        A3[JWT Refresh Rotation 7d]
        A4[5-Strike Account Lockout]
    end

    subgraph AuthZ["Authorization Layer"]
        B1[RBAC: ADMIN / OPERATOR / VIEWER]
        B2[Adaptive Policy: PRIVILEGED vs STANDARD]
        B3[Trust Gating: SUSPICIOUS / QUARANTINED]
    end

    subgraph Crypto["Cryptographic Primitives"]
        C1[Ed25519 Keypairs via PyNaCl]
        C2[W3C did:key Multibase Resolution]
        C3[Ed25519Signature2020 Proofs]
        C4[URDNA2015 JSON-LD Canonicalization]
    end

    subgraph Audit["Audit & Observability"]
        D1[security_audit_events]
        D2[trust_audit_trails]
        D3[telemetry_logs]
        D4[OpenTelemetry Tracing]
    end

    AuthN --> AuthZ --> Crypto --> Audit"""
    }
]

story = []

# Title Page
story += [
    Spacer(1, 40),
    Paragraph("TrustChain-AI", title_style),
    Paragraph("Architecture & Diagrams Technical Reference Collection", sub_style),
    HRFlowable(width="90%", thickness=1.5, color=colors.HexColor('#1a365d')),
    Spacer(1, 15),
    Paragraph("<b>Project:</b> A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration", body_style),
    Paragraph("<b>Department:</b> Computer Engineering, MPSTME, SVKM's NMIMS University, Mumbai", body_style),
    Paragraph("<b>Document Purpose:</b> Official diagrammatic specification for academic and technical examination", body_style),
    Spacer(1, 10),
    HRFlowable(width="90%", thickness=0.5, color=colors.grey),
    Spacer(1, 25),
    Paragraph("<b>Index of Included Diagrams:</b>", h2_style),
]

summary_rows = [["#", "Diagram Title", "Category"]]
for d in diagrams:
    summary_rows.append([d["num"], d["title"], d["category"]])

t_summary = Table(summary_rows, colWidths=[0.5*inch, 4.0*inch, 2.0*inch])
t_summary.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a365d')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f7fafc')]),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_summary)
story.append(PageBreak())

# Diagram Pages
for d in diagrams:
    story.append(Paragraph(f"Figure {d['num']}: {d['title']}", h1_style))
    story.append(Paragraph(f"<b>Category:</b> {d['category']}", h2_style))
    story.append(Paragraph(f"<b>Technical Description:</b> {d['desc']}", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Mermaid Diagram Specification:</b>", h2_style))
    
    # Format mermaid code box
    cleaned_code = d['mermaid'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>').replace(' ', '&nbsp;')
    story.append(Paragraph(cleaned_code, code_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<i>Figure {d['num']} — {d['title']} (TrustChain-AI Specification)</i>", caption_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e0')))
    story.append(PageBreak())

doc.build(story)
print(f"[OK] Diagram PDF generated: {PDF_OUT}")
