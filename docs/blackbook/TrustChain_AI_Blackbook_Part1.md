<!-- ============================================================
     TRUSTCHAIN-AI BLACKBOOK — PART 1
     Preliminary Pages · Chapter 1 · Chapter 2
     Primary deliverable: docs/blackbook/TrustChain_AI_Blackbook_Source.md
     ============================================================ -->

---

# TRUSTCHAIN-AI: A DECENTRALIZED TRUST INTELLIGENCE FRAMEWORK FOR SECURE AUTONOMOUS AI AGENT COLLABORATION

**A Project Report**
Submitted in Partial Fulfilment of the Requirements for the Degree of

**Bachelor of Technology in Computer Engineering**

---

Department of Computer Engineering
Mukesh Patel School of Technology Management & Engineering (MPSTME)
SVKM's NMIMS (Deemed-to-be University), Mumbai

---

**Submitted by:**

[STUDENT NAME 1] — Roll No: [ROLL NUMBER 1]
[STUDENT NAME 2] — Roll No: [ROLL NUMBER 2]

**Project Mentor:**
[MENTOR NAME]

**Academic Year:** 2026–2027

---

---

## CERTIFICATE

*Department of Computer Engineering*
*Mukesh Patel School of Technology Management & Engineering (MPSTME)*
*SVKM's NMIMS (Deemed-to-be University), Mumbai*

---

This is to certify that the project titled **"TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration"** has been submitted by the following students in partial fulfilment of the requirements for the award of the Degree of **Bachelor of Technology in Computer Engineering** of NMIMS University, Mumbai during the academic year 2026–2027.

| Student Name | Roll Number |
|-------------|-------------|
| [STUDENT NAME 1] | [ROLL NUMBER 1] |
| [STUDENT NAME 2] | [ROLL NUMBER 2] |

The project was carried out under our guidance and supervision. To the best of our knowledge and belief, the work presented in this report is genuine and has not been submitted for any other degree, diploma, or award.

---

**Internal Guide**
[MENTOR NAME]
Designation, Department of Computer Engineering, MPSTME, NMIMS

Signature: _________________________ Date: _____________

---

**Head of Department**
Department of Computer Engineering, MPSTME, NMIMS

Signature: _________________________ Date: _____________

---

**External Examiner**

Signature: _________________________ Date: _____________

---

*(University Seal)*

---

---

## ACKNOWLEDGEMENT

We express our sincere gratitude to our project mentor, **[MENTOR NAME]**, for their consistent guidance, valuable feedback, and encouragement throughout the development of this project. Their technical insights and scholarly direction were instrumental in shaping the depth and quality of this work.

We thank the **Department of Computer Engineering, MPSTME, NMIMS University, Mumbai** for providing the academic infrastructure, computing resources, and research environment that made this project possible.

We are grateful to the faculty members of the department for their teaching and mentorship over the course of our undergraduate programme, which equipped us with the theoretical foundations and practical skills applied in this project.

We also acknowledge the open-source communities behind FastAPI, React, SQLAlchemy, PyNaCl, and the W3C standards bodies whose published specifications — Decentralised Identifiers (DIDs) v1.0 and Verifiable Credentials Data Model v1.1 — provided the foundational standards upon which this system is built.

Finally, we thank our families and peers for their support and encouragement throughout this work.

[STUDENT NAME 1]
[STUDENT NAME 2]

---

---

## ABSTRACT

The rapid proliferation of autonomous AI agent systems has created an urgent need for robust mechanisms to establish, monitor, and enforce trust among collaborating agents. Existing multi-agent platforms lack cryptographically verifiable identity primitives, continuous behavioural trust monitoring, and dynamic authorization policies that respond to runtime agent behaviour. Without these foundations, AI agent systems are vulnerable to impersonation, credential forgery, policy bypass, and Byzantine agent behaviour, all of which can compromise the integrity of automated workflows.

This project presents **TrustChain-AI**, a decentralised trust intelligence framework designed for secure autonomous AI agent collaboration. The framework integrates W3C Decentralised Identifiers (DID:key method, Ed25519 cryptography) and W3C Verifiable Credentials (Ed25519Signature2020 proof suite with JSON-LD canonicalisation) to establish cryptographically verifiable agent identity. A temporal Exponential Moving Average (EMA) trust scoring engine continuously evaluates agent behaviour across three dimensions — task success rate, policy compliance rate, and response latency — producing a composite trust score and transitioning agents among four states: TRUSTED, SUSPICIOUS, QUARANTINED, and REVOKED. An adaptive policy enforcement module gates agent operations based on live trust state, denying high-privilege operations to behaviourally compromised agents even when they hold valid credentials.

The system is implemented as a FastAPI backend (Python 3.12.3, Uvicorn ASGI) with a 14-table SQLite-based local Verifiable Data Registry, a React 19 / Vite frontend dashboard, and a comprehensive REST API secured by JWT authentication and role-based access control. A trust-weighted agent discovery and matching engine ranks candidate agents by a composite score incorporating trust, reputation, task success rate, and response latency. Sequential multi-agent workflow orchestration coordinates capability-specific task pipelines with per-step trust verification. A structured local execution engine (LocalAgentConnector) simulates agent task responses for development and testing purposes.

The complete test suite of 77 automated tests passes without failures, covering end-to-end agent lifecycle, trust degradation and recovery paths, administrative revocation, multi-agent discovery, collaboration sessions, workflow orchestration, and system health monitoring. All six stated project objectives are verified as achieved.

**Keywords:** Decentralised Identifiers, Verifiable Credentials, Multi-Agent Systems, Trust Management, Exponential Moving Average, Adaptive Authorization, Zero Trust, Self-Sovereign Identity

---

---

## TABLE OF CONTENTS

| Section | Title | Page |
|---------|-------|------|
| — | Title Page | i |
| — | Certificate | ii |
| — | Acknowledgement | iii |
| — | Abstract | iv |
| — | Table of Contents | v |
| — | List of Figures | vii |
| — | List of Tables | viii |
| — | List of Abbreviations | ix |
| — | Symbols and Notations | x |
| **Chapter 1** | **Introduction** | **1** |
| 1.1 | Background and Motivation | 1 |
| 1.2 | Problem Statement | 3 |
| 1.3 | Project Objectives | 4 |
| 1.4 | Scope and Boundaries | 5 |
| 1.5 | Proposed Solution Overview | 6 |
| 1.6 | Key Contributions | 7 |
| 1.7 | Report Organisation | 8 |
| 1.8 | Chapter Summary | 9 |
| **Chapter 2** | **Literature Review** | **10** |
| 2.1 | Introduction to the Literature Review | 10 |
| 2.2 | Trust and Reputation in Distributed Systems | 11 |
| 2.3 | Trust in IoT and Cyber-Physical Systems | 14 |
| 2.4 | Decentralised Identity and Self-Sovereign Identity | 16 |
| 2.5 | Adaptive Authorization and Zero Trust | 19 |
| 2.6 | Multi-Agent Systems and Agent Coordination | 21 |
| 2.7 | Research Gap Analysis | 23 |
| 2.8 | Chapter Summary | 25 |
| **Chapter 3** | **System Design and Implementation** | **26** |
| 3.1 | Introduction | 26 |
| 3.2 | System Architecture | 26 |
| 3.3 | Identity Management | 30 |
| 3.4 | Trust Intelligence Engine | 34 |
| 3.5 | Adaptive Authorization | 40 |
| 3.6 | Agent Registry and Discovery | 43 |
| 3.7 | Multi-Agent Collaboration | 46 |
| 3.8 | Workflow Orchestration | 48 |
| 3.9 | Security Architecture | 50 |
| 3.10 | Database Design | 53 |
| 3.11 | REST API Design | 56 |
| 3.12 | Frontend Architecture | 58 |
| 3.13 | Chapter Summary | 61 |
| **Chapter 4** | **Results and Verification** | **62** |
| 4.1 | Introduction | 62 |
| 4.2 | Test Suite Results | 62 |
| 4.3 | System Health Verification | 66 |
| 4.4 | Trust Mathematics Verification | 67 |
| 4.5 | Adaptive Authorization Verification | 70 |
| 4.6 | Authentication and Security Verification | 71 |
| 4.7 | API Endpoint Verification | 72 |
| 4.8 | Frontend Dashboard | 73 |
| 4.9 | Objectives Achievement Matrix | 74 |
| 4.10 | Chapter Summary | 75 |
| **Chapter 5** | **Advantages, Limitations, and Applications** | **76** |
| 5.1 | Introduction | 76 |
| 5.2 | Advantages of TrustChain-AI | 76 |
| 5.3 | Limitations | 79 |
| 5.4 | Potential Applications | 82 |
| 5.5 | Chapter Summary | 84 |
| **Chapter 6** | **Conclusion and Future Scope** | **85** |
| 6.1 | Introduction | 85 |
| 6.2 | Project Conclusion | 85 |
| 6.3 | Contribution Summary | 87 |
| 6.4 | Future Scope | 88 |
| 6.5 | Final Remarks | 90 |
| — | References | 91 |
| **Appendix A** | API Endpoint Reference | 93 |
| **Appendix B** | Database Schema Reference | 96 |
| **Appendix C** | Test Results Summary | 99 |
| **Appendix D** | Trust Mathematics Reference | 101 |

---

---

## LIST OF FIGURES

| Figure No. | Title | Page |
|-----------|-------|------|
| Figure 1 | Overall System Architecture | 27 |
| Figure 2 | Layered Architecture | 29 |
| Figure 3 | Trust Evaluation Flowchart | 35 |
| Figure 4 | Trust State Transition Diagram | 38 |
| Figure 5 | Adaptive Authorization Flow | 41 |
| Figure 6 | Agent Discovery and Matching | 44 |
| Figure 7 | Sequential Workflow Execution | 49 |
| Figure 8 | Collaboration Session Lifecycle | 47 |
| Figure 9 | Database Entity-Relationship Diagram | 54 |
| Figure 10 | DID Key Generation Flowchart | 31 |
| Figure 11 | System Context Diagram | 28 |
| Figure 12 | Security Architecture | 51 |

---

---

## LIST OF TABLES

| Table No. | Title | Page |
|----------|-------|------|
| Table 1 | Trust Weight Configuration | 36 |
| Table 2 | Trust State Thresholds and Transitions | 39 |
| Table 3 | Adaptive Authorization Matrix | 42 |
| Table 4 | Agent Match Scoring Weights | 45 |
| Table 5 | Database Table Summary | 55 |
| Table 6 | Technology Stack Summary | 30 |
| Table 7 | API Endpoint Summary by Module | 57 |
| Table 8 | Test Suite Results Summary | 63 |
| Table 9 | Trust Math Worked Example | 68 |
| Table 10 | Project Objectives Achievement Matrix | 74 |

---

---

## LIST OF ABBREVIATIONS

| Abbreviation | Full Form |
|-------------|-----------|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| ASGI | Asynchronous Server Gateway Interface |
| DID | Decentralised Identifier |
| EMA | Exponential Moving Average |
| HTTP | Hypertext Transfer Protocol |
| HTTPS | Hypertext Transfer Protocol Secure |
| IoT | Internet of Things |
| JSON | JavaScript Object Notation |
| JSON-LD | JavaScript Object Notation for Linked Data |
| JTI | JWT Token Identifier |
| JWT | JSON Web Token |
| MAS | Multi-Agent System |
| MPSTME | Mukesh Patel School of Technology Management & Engineering |
| NMIMS | SVKM's Narsee Monjee Institute of Management Studies |
| RBAC | Role-Based Access Control |
| REST | Representational State Transfer |
| SDK | Software Development Kit |
| SOC | Security Operations Centre |
| SQLite | Self-Contained SQL Database Engine |
| SSI | Self-Sovereign Identity |
| URL | Uniform Resource Locator |
| UUID | Universally Unique Identifier |
| VDR | Verifiable Data Registry |
| VC | Verifiable Credential |
| W3C | World Wide Web Consortium |
| WAL | Write-Ahead Logging |

---

---

## SYMBOLS AND NOTATIONS

| Symbol | Definition |
|--------|-----------|
| $P_i(t)$ | Multi-factor performance score for agent $i$ at time $t$ |
| $T_i(t)$ | Temporal trust score for agent $i$ at time $t$ (EMA) |
| $S_i(t)$ | Task success rate for agent $i$ over evaluation window |
| $C_i(t)$ | Policy compliance rate for agent $i$ over evaluation window |
| $L_i(t)$ | Normalised response latency for agent $i$ |
| $w_1$ | Weight for task success factor ($w_1 = 0.6$) |
| $w_2$ | Weight for compliance factor ($w_2 = 0.3$) |
| $w_3$ | Weight for latency factor ($w_3 = 0.1$) |
| $\lambda$ | EMA decay factor ($\lambda = 0.7$) |
| $\tau_{\text{trusted}}$ | Trust threshold for TRUSTED state ($\tau_{\text{trusted}} = 0.8$) |
| $\tau_{\text{suspicious}}$ | Trust threshold for SUSPICIOUS state ($\tau_{\text{suspicious}} = 0.5$) |
| $r_i$ | Reputation score of agent $i$ (scale 1.0–5.0) |
| $\sigma_i$ | Task success rate of agent $i$ (proportion, 0.0–1.0) |
| $\bar{\ell}_i$ | Average response latency of agent $i$ in milliseconds |
| $n$ | Evaluation window size ($n = 10$ telemetry events) |

---

---

# CHAPTER 1: INTRODUCTION

## 1.1 Background and Motivation

The deployment of autonomous AI agents has accelerated across industry and research, driven by the increasing sophistication of large language models, task-specific ML pipelines, and orchestration frameworks that coordinate multiple agents towards shared objectives. In enterprise settings, AI agents perform data analysis, code generation, document summarisation, threat detection, and process automation with minimal human intervention. In security operations, autonomous agents hunt for threats, correlate alerts, and initiate incident response actions at machine speed. In scientific workflows, AI agents collaborate to execute multi-step research pipelines spanning data retrieval, statistical analysis, hypothesis generation, and result verification.

This growing deployment of autonomous AI agent systems introduces a class of problems that traditional software security and distributed systems research has not fully addressed. When a human operator delegates a sensitive task to an AI agent, or when one AI agent invokes another within a collaborative workflow, a fundamental question arises: **how does the system know whether it can trust the agent to behave correctly, honestly, and in accordance with its declared capabilities?**

Traditional approaches to this problem rely on two mechanisms. The first is **authentication** — verifying that the agent is who it claims to be, typically through API keys, TLS certificates, or OAuth tokens. The second is **static authorisation** — granting the agent a set of permissions at registration time and enforcing those permissions on each request. While these mechanisms address identity and access control, they fail to address the problem of **behavioural trust** — the degree to which an agent's runtime behaviour, across many interactions over time, warrants confidence that it will continue to act as expected.

An AI agent that holds a valid API key may nonetheless begin to produce incorrect results due to model drift, adversarial fine-tuning, or internal misconfiguration. An agent that was once reliable may become unreliable due to resource constraints, network instability, or deliberate manipulation. In collaborative multi-agent workflows, a compromised agent can corrupt the entire pipeline — submitting false intermediate results, bypassing policy checks, or silently delegating tasks to unauthorised sub-agents. None of these failure modes are detectable by authentication mechanisms alone.

The academic field of **trust and reputation management** in distributed systems has studied this problem for peer-to-peer networks, grid computing, IoT systems, and e-commerce platforms. Seminal works such as EigenTrust [4], the Jøsang et al. survey [3], and the Mui et al. computational trust model [5] provide formal frameworks for quantifying agent trustworthiness from interaction history. However, these models were designed for relatively homogeneous networks of peers with comparable roles, not for heterogeneous multi-agent AI systems where agents have diverse capabilities, play different roles in workflows, and must present verifiable credentials to one another.

The W3C has published two landmark standards that provide a foundation for decentralised digital identity: the **Decentralised Identifiers (DIDs) v1.0 specification** [1] and the **Verifiable Credentials Data Model v1.1** [2]. DIDs provide a method-independent, cryptographically verifiable identifier scheme that does not depend on centralised certificate authorities. Verifiable Credentials provide a standardised format for digitally-signed attestations that subjects can present to verifiers. Together, these standards form the basis of the **Self-Sovereign Identity (SSI)** ecosystem [14], which has seen adoption in government identity systems, healthcare credential management, and supply chain provenance. Their application to AI agent identity management is a natural extension that has not yet been comprehensively demonstrated in an integrated, testable system.

The **Zero Trust Architecture** model [15], articulated by NIST Special Publication 800-207, provides an organisational security philosophy aligned with the needs of multi-agent AI systems: "Never trust, always verify." Zero Trust requires continuous verification of identity and posture for every resource access, regardless of network location. Applying zero trust principles to AI agent systems means that an agent's prior history of trusted behaviour does not exempt it from continuous scrutiny. Its current behavioural posture must inform every authorisation decision.

TrustChain-AI integrates these three intellectual strands — trust and reputation management, self-sovereign identity, and zero trust architecture — into a coherent, implementable framework specifically designed for secure autonomous AI agent collaboration.

## 1.2 Problem Statement

The central problem addressed by this project is the **absence of a unified trust management framework for multi-agent AI systems** that combines cryptographic identity verification with continuous behavioural trust scoring and trust-state-aware dynamic authorisation.

More specifically, existing multi-agent platforms and AI orchestration systems lack:

**(a) Cryptographically Verifiable Agent Identity.** Most systems rely on opaque API keys or server-managed tokens that can be forged, shared, or stolen without cryptographic detection. There is no standard mechanism for an AI agent to present a verifiable, unforgeable identity that can be independently validated by any party possessing the agent's public key.

**(b) Continuous Behavioural Trust Monitoring.** Agent authorisation decisions are typically made once at registration or login. There is no mechanism to continuously reassess whether an agent's runtime behaviour — measured across task success, policy compliance, and response characteristics — warrants continued access at its current privilege level.

**(c) Trust-State-Aware Adaptive Authorisation.** Even where monitoring is implemented, the results are rarely connected to authorisation enforcement. An agent whose behaviour has degraded to an unsafe level continues to receive the same access rights it had when operating correctly.

**(d) Auditable Trust Evidence.** There is typically no persistent, structured record of the evidence supporting each trust decision — what telemetry was observed, how the trust score was computed, and why the agent's trust state changed. Without such evidence, trust decisions cannot be reviewed, challenged, or improved.

**(e) Trust-Weighted Capability Matching.** When orchestrating a multi-step workflow that requires specific agent capabilities, existing systems select agents purely by capability availability. There is no mechanism to prefer higher-trust agents or exclude agents whose behavioural history indicates unreliability.

These gaps expose multi-agent AI systems to several concrete threat classes: **impersonation** (false agent identity claims), **Byzantine agent behaviour** (agents that selectively fail or corrupt outputs), **privilege escalation** (agents that successfully complete a few tasks to achieve TRUSTED status before executing malicious high-privilege operations), and **credential forgery** (presentation of unverifiable or self-issued credentials).

## 1.3 Project Objectives

Based on the identified problem, this project defines six specific technical objectives:

**Objective 1: Decentralised Agent Identity.** Implement the W3C DID:key method with Ed25519 elliptic curve cryptography to provide each AI agent with a cryptographically verifiable decentralised identifier. The implementation must generate DID:key URIs with correct Ed25519 multibase/multicodec encoding, produce conformant DID Documents, and support Ed25519 signature verification.

**Objective 2: Verifiable Credentials for Agent Authorisation.** Implement the W3C Verifiable Credentials Data Model with Ed25519Signature2020 proof suites and JSON-LD canonicalisation to enable agents to issue, store, present, and verify structured attestations about identity, capabilities, and authorisation status.

**Objective 3: Temporal EMA Trust Scoring Engine.** Design and implement a multi-factor trust scoring engine that continuously evaluates agent behaviour across three dimensions (task success rate, policy compliance rate, response latency), computes a composite performance score $P_i(t)$ and a temporally smoothed trust score $T_i(t)$ using Exponential Moving Average, and transitions agents among four discrete trust states based on configurable thresholds.

**Objective 4: Adaptive Trust-State-Aware Authorisation.** Implement a policy enforcement module that gates agent operations based on live trust state — blocking high-privilege operations from SUSPICIOUS agents, blocking all operations from QUARANTINED and REVOKED agents, and maintaining a complete audit trail of authorisation decisions.

**Objective 5: Trust-Weighted Agent Discovery and Matching.** Build an agent registry and discovery engine that filters candidate agents by required capability and trust state eligibility, and ranks qualified agents by a composite match score incorporating trust score, reputation score, task success rate, and response latency.

**Objective 6: Sequential Multi-Agent Workflow Orchestration.** Implement a workflow orchestration engine that coordinates sequential pipelines of capability-specific agent tasks, passes output data between pipeline steps, enforces per-step trust verification, and records complete workflow and node-level execution state.

## 1.4 Scope and Boundaries

**In Scope:**

- All six objectives listed in Section 1.3
- Local Verifiable Data Registry implemented as a SQLite database file (`vdr.db`) with Write-Ahead Logging
- A structured local execution engine (LocalAgentConnector) that simulates agent task responses for development and testing purposes based on declared capability
- JWT-based authentication with Argon2id password hashing, refresh token rotation, and account lockout
- Role-Based Access Control with three roles: ADMIN, OPERATOR, VIEWER
- A React 19 / Vite 8 dashboard providing a comprehensive UI for all platform features
- A complete automated test suite covering all objectives

**Out of Scope:**

- Distributed or blockchain-based Verifiable Data Registry (future scope; see Section 6.4.1)
- Live LLM inference for agent task execution (future scope; see Section 6.4.2)
- PARALLEL workflow execution (schema-supported but not fully tested; future scope; see Section 6.4.3)
- Cross-organisational federated trust (future scope; see Section 6.4.4)
- W3C VC revocation list / StatusList2021 (future scope; see Section 6.4.6)
- Zero-Knowledge Proof credential presentation (future scope; see Section 6.4.7)

## 1.5 Proposed Solution Overview

TrustChain-AI is organised into five architectural layers (detailed in Chapter 3):

**Layer 1 — Presentation Layer:** A React 19 single-page application providing seventeen interactive components for agent management, trust analytics, workflow orchestration, collaboration management, identity and credential operations, audit trail inspection, and system health monitoring. A global dark/light theme toggle provides operator ergonomics.

**Layer 2 — API Gateway Layer:** A FastAPI ASGI application exposing 38 REST endpoints across three modules (Authentication, Agent Registry, Verifiable Data Registry) plus a system health endpoint. Pydantic v2 validates all request and response payloads. JWT Bearer tokens protect all protected endpoints. OpenTelemetry API/SDK instruments request handling.

**Layer 3 — Trust Intelligence Layer:** The TrustEngine class implements the EMA trust scoring algorithm and state machine. The AdaptivePolicyEnforcer evaluates every agent operation request against live trust state. The LocalAgentConnector executes capability-specific tasks as a structured local execution engine.

**Layer 4 — Identity and Credential Layer:** The DIDKey class generates Ed25519 keypairs, encodes public keys with multicodec prefix 0xED01, and constructs conformant DID:key URIs and DID Documents. The VerifiableCredential class issues W3C Verifiable Credentials with Ed25519Signature2020 proofs using JSON-LD canonicalisation via PyLD.

**Layer 5 — Persistence Layer:** A local SQLite database in WAL mode serves as the Verifiable Data Registry, accessed through SQLAlchemy 2.0 ORM. Fourteen tables record agent identities, trust scores, telemetry events, audit trails, Verifiable Credentials, collaboration sessions, workflow state, user accounts, refresh tokens, and security events.

## 1.6 Key Contributions

This project makes three principal contributions to the state of practice for multi-agent AI systems:

**Contribution 1: Integrated DID/VC + Behavioural Trust Framework.** TrustChain-AI is the first demonstration of a system that integrates W3C DID and VC standards with a formal behavioural EMA trust scoring engine in a single, testable platform. Prior works either address identity (DID/VC) without behavioural trust, or address trust scoring without cryptographic identity foundations.

**Contribution 2: Adaptive Policy Enforcement for AI Agents.** The AdaptivePolicyEnforcer operationalises zero trust principles specifically for AI agent operations by combining RBAC with trust-state gating. This provides a principled mechanism for restricting agent capabilities in response to detected behavioural anomalies without requiring human intervention.

**Contribution 3: Trust-Aware Multi-Agent Discovery.** The agent matching algorithm incorporates four factors — cryptographic trust score, peer reputation, historical success rate, and response latency — into a single composite match score that enables trust-aware agent selection for capability-specific workflow roles.

## 1.7 Report Organisation

The remainder of this report is organised as follows:

**Chapter 2 — Literature Review** surveys relevant prior work across five thematic areas: trust and reputation management in distributed systems, trust in IoT and cyber-physical systems, decentralised identity and self-sovereign identity, adaptive authorisation and zero trust, and multi-agent systems coordination. A research gap analysis identifies the specific gaps that TrustChain-AI addresses.

**Chapter 3 — System Design and Implementation** presents the complete technical design and implementation of TrustChain-AI. It covers the five-layer architecture, identity management, trust intelligence engine, adaptive authorisation, agent registry and discovery, collaboration, workflow orchestration, security architecture, database design, REST API design, and frontend architecture.

**Chapter 4 — Results and Verification** reports the results of the complete automated test suite (77/77 tests passing), presents verified system health data, demonstrates the trust mathematics through worked examples, and provides an objectives achievement matrix confirming the status of all six project objectives.

**Chapter 5 — Advantages, Limitations, and Applications** discusses the strengths and acknowledged limitations of the implementation, and identifies potential application domains for TrustChain-AI.

**Chapter 6 — Conclusion and Future Scope** summarises the project's achievements and contributions, and identifies seven directions for future work.

**References** lists all fifteen cited works. **Appendices A–D** provide the complete API endpoint reference, database schema, test results, and trust mathematics reference.

## 1.8 Chapter Summary

This chapter established the motivation for trust management in multi-agent AI systems, drawing on the convergence of trust and reputation research, self-sovereign identity standards, and zero trust architecture. It identified five specific gaps in existing multi-agent platforms and defined six concrete project objectives to address those gaps. The scope, solution overview, and key contributions of TrustChain-AI were presented, and the structure of the remaining report was described.

---

---

# CHAPTER 2: LITERATURE REVIEW

## 2.1 Introduction to the Literature Review

Trust in distributed computational systems has been studied for over two decades, motivated initially by the challenges of peer-to-peer file sharing, grid computing, and e-commerce reputation systems. As AI agent systems have grown in complexity and autonomy, the trust problem has acquired new dimensions: agents are not merely passive service providers but active participants that initiate requests, delegate subtasks, consume resources, and modify shared state. This chapter surveys the most relevant prior work across five thematic areas: (1) trust and reputation in distributed systems, (2) trust in IoT and cyber-physical systems, (3) decentralised identity and self-sovereign identity, (4) adaptive authorisation and zero trust, and (5) multi-agent systems coordination. For each area, the key contributions of cited works are summarised and their limitations in the context of AI agent trust management are identified. The chapter concludes with a gap analysis table that maps prior limitations to TrustChain-AI contributions.

## 2.2 Trust and Reputation in Distributed Systems

The study of computational trust in distributed systems was codified by Jøsang, Ismail, and Boyd in a widely-cited survey published in the *Decision Support Systems* journal [3]. The survey provides a comprehensive taxonomy of trust and reputation systems, distinguishing between reliability trust (expectation that an agent will perform correctly), competence trust (belief in an agent's capability to complete a task), and honesty trust (confidence that an agent will not deceive). The survey classifies systems by their aggregation method (centralised vs. distributed reputation), evidence type (direct experience vs. referrals), and trust model (probabilistic, fuzzy, flow-based, or game-theoretic). This taxonomy remains the most widely referenced framework for evaluating new trust systems and is used in this review to contextualise TrustChain-AI's design.

A landmark contribution to distributed reputation management is the EigenTrust algorithm by Kamvar, Schlosser, and Garcia-Molina [4], designed for peer-to-peer file sharing networks. EigenTrust computes a normalised global trust value for each peer by iteratively propagating trust scores from a set of pre-trusted peers. A peer's trust value converges to a principal eigenvector of the trust matrix, providing a provably consistent and attack-resistant global reputation. The algorithm is effective for large, relatively homogeneous peer networks where the trust relationship is transitive and the network graph is relatively stable. However, EigenTrust has two significant limitations in the AI agent context. First, it assumes a static graph where peer relationships are established and persist; AI agent environments are highly dynamic, with agents joining, leaving, and changing capability profiles frequently. Second, EigenTrust provides a single scalar trust value per peer, without distinguishing between trust dimensions (reliability vs. competence vs. honesty) or incorporating objective behavioural metrics such as response latency or policy compliance.

Mui, Mohtashemi, and Halberstadt [5] proposed a probabilistic computational model of trust and reputation grounded in Bayesian inference. In their model, trust is represented as a probability distribution over the likelihood of an agent behaving cooperatively in a future interaction, estimated from a Beta distribution parameterised by counts of cooperative and non-cooperative past interactions. Reputation is modelled as a propagated trust estimate derived from third-party referrals, discounted by the trustworthiness of the referring agent. This model is mathematically rigorous and handles uncertainty well. However, it treats trust as a single binary dimension (cooperated vs. did not cooperate), which is insufficient for AI agent systems where behavioural quality has multiple continuous dimensions: a task may be completed but late, compliant but incorrect, or successful on simple tasks but unreliable on complex ones.

Azzedin and Maheswaran [7] studied trust evolution in grid computing systems, where distributed compute nodes collaborate to execute large-scale scientific workloads. They proposed a trust management framework that is context-sensitive (trust assessments are task-type specific), dynamic (trust values evolve over time as new evidence accumulates), and hierarchical (trust can be delegated across administrative domains). Their framework introduced the important concept of trust dynamism: a node that was trusted for data-intensive tasks may not be trusted for compute-intensive tasks, and a node's trust in one context does not transfer to another. This context-sensitivity principle influenced TrustChain-AI's capability-specific trust evaluation and the match score formula, which weights trust relative to the task type required.

**Summary and Gap:** The distributed trust literature establishes the theoretical foundation for trust quantification from interaction history. However, it addresses peer networks of relatively homogeneous computational nodes, not AI agents with diverse capability profiles, verifiable cryptographic identity, and the ability to present credentials. None of these works integrates identity verification with trust scoring. A misbehaving peer in EigenTrust or Mui's model can only be identified retrospectively through degraded reputation; it cannot be pre-emptively identified as an impersonator through credential verification. TrustChain-AI addresses this gap by combining formal identity verification (DID:key + VC) with behavioural trust scoring.

## 2.3 Trust in IoT and Cyber-Physical Systems

Nitti, Girau, and Atzori [6] studied trust management in the Social Internet of Things (SIoT), a paradigm where IoT devices establish social-like relationships (ownership, co-location, co-work, etc.) with one another. Their model distinguishes between object trust (historical performance of a device in completing tasks), service trust (quality of specific services provided), and social relationship trust (trust derived from the social network of device relationships). Trust values are computed as weighted combinations of direct experience and referrals from socially proximate devices.

The SIoT trust model is notable for its multi-dimensional treatment of trust (object, service, social) and its recognition that trust is relationship-specific rather than global. These design choices parallel TrustChain-AI's multi-factor trust scoring, which separately measures task success ($S_i$), compliance ($C_i$), and latency ($L_i$) rather than collapsing to a single binary rating. The temporal aspect of TrustChain-AI's EMA formula — weighting recent behaviour more heavily — also parallels the temporal decay mechanisms used in SIoT models.

However, IoT devices differ fundamentally from AI agents in their identity model. IoT devices typically receive their identity from a manufacturer certificate or a gateway-assigned credential. They do not generate their own cryptographic identity, present verifiable credentials to relying parties, or have the ability to adapt their behaviour in response to detected trust challenges. An IoT device that is misbehaving is typically handled by physical replacement or gateway-level blacklisting, not by graduated trust-state transitions that allow recovery if behaviour improves. TrustChain-AI's four-state trust machine (TRUSTED → SUSPICIOUS → QUARANTINED → REVOKED) with recovery paths from SUSPICIOUS and QUARANTINED states better models the graduated response needed for AI agents, which may exhibit temporary performance degradation due to transient conditions rather than permanent compromise.

The multi-factor trust approach in SIoT also differs from TrustChain-AI in an important respect: SIoT metrics are largely self-reported or network-inferred. In TrustChain-AI, trust metrics are derived from structured telemetry events submitted by agents and independently recorded in the VDR — an auditable evidence chain that SIoT models lack.

**Summary and Gap:** IoT trust research confirms the value of multi-dimensional, temporal trust scoring and introduces important concepts of social trust propagation. However, IoT trust models do not address cryptographic agent identity, verifiable credential presentation, or graduated authorisation enforcement. The ability of IoT devices to self-manage trust transitions and recover from degraded states is also limited.

## 2.4 Decentralised Identity and Self-Sovereign Identity (SSI)

The W3C Decentralised Identifiers (DIDs) v1.0 Recommendation [1] defines a URI scheme for identifiers that are globally unique, resolvable, cryptographically verifiable, and decentralised — meaning their creation and control does not depend on any central authority. A DID URI (e.g., `did:key:z6Mk...`) resolves to a **DID Document** — a JSON-LD document containing the subject's public keys, authentication methods, and service endpoints. The DID Core specification defines the abstract data model and resolution process; specific implementations are governed by DID methods (did:key, did:web, did:ion, etc.), each registered in the W3C DID Method Registry.

TrustChain-AI implements the **did:key method**, which generates a DID from a public key in a self-contained, infrastructureless manner: the public key is encoded with a multicodec prefix, base58-encoded with a multibase prefix, and embedded directly in the DID URI. This approach requires no external registry, no blockchain, and no DNS lookup for DID resolution. The `did:key` method is appropriate for development and local deployment scenarios where infrastructure independence is valued; in production, methods such as `did:ion` or `did:web` may be preferred for their additional capabilities (key rotation, service endpoints, etc.).

The W3C Verifiable Credentials Data Model v1.1 [2] defines a standard format for expressing digitally-signed credentials in a manner that is cryptographically verifiable by any party with access to the issuer's public key. A Verifiable Credential contains a `credentialSubject` block (the claims), an `issuer` field, a `proof` block (the digital signature and signing method), and JSON-LD context declarations. TrustChain-AI implements the **Ed25519Signature2020** proof suite — an Ed25519 digital signature over the URDNA2015 JSON-LD canonical form of the credential document. This proof suite provides strong cryptographic security (128-bit security level) with compact key and signature sizes (32-byte public key, 64-byte signature), making it highly efficient for agent credential presentation.

Fromknecht, Velicanu, and Yakoubov [9] proposed CertCoin, a decentralised public key infrastructure that uses a public blockchain to record identity-to-key bindings, addressing the certificate authority single-point-of-trust problem. While TrustChain-AI does not implement blockchain-based key registration, the conceptual motivation is similar: identity records should be verifiable without trusting a central authority. TrustChain-AI achieves this through the `did:key` self-certifying identifier, where the DID itself encodes the public key and no external lookup is required for verification.

The Trust over IP Foundation [14] has proposed a four-layer model for decentralised digital trust: (Layer 1) decentralised identifier utilities (blockchain/DID infrastructure), (Layer 2) DID communication protocols, (Layer 3) exchange protocols for credentials and proofs, and (Layer 4) application ecosystems. TrustChain-AI addresses layers 2, 3, and 4 of this model: it implements DID communication through the VDR REST API, credential exchange through the VC issuance and verification endpoints, and an application ecosystem through the React dashboard. Layer 1 (blockchain infrastructure) is explicitly out of scope for the local VDR implementation.

RFC 8037 [8] defines the use of Edwards curves (Ed25519/X25519) in the JSON Object Signing and Encryption (JOSE) framework, specifying the `Ed25519` algorithm identifier and key representation format. TrustChain-AI's Ed25519 implementation is consistent with RFC 8037's key representation principles, though the VC proof suite uses the W3C `Ed25519Signature2020` format rather than JWS, to align with the VC Data Model's proof block convention.

**Summary and Gap:** W3C DID and VC standards provide the cryptographic identity foundation that distributed trust models lack. However, the SSI literature focuses on human identity management — credential issuance for people, presentation to service verifiers — not on the specific requirements of AI agent identity: automated credential rotation, trust-state-triggered credential revocation, capability attestation, and integration with behavioural trust scoring. TrustChain-AI bridges this gap by embedding VC-based identity in an AI agent registry where credential validity is coupled to behavioural trust state.

## 2.5 Adaptive Authorization and Zero Trust

The National Institute of Standards and Technology (NIST) Special Publication 800-207 [15] defines the Zero Trust Architecture (ZTA) model, which rejects the traditional perimeter-based security model in favour of continuous verification of identity and posture for every resource access. The seven tenets of ZTA include: all data sources and computing services are considered resources; all communication is secured regardless of network location; access to resources is granted on a per-session basis; access to resources is determined by dynamic policy; the enterprise monitors and measures the integrity and security posture of all owned and associated assets; all resource authentication and authorisation is dynamic and strictly enforced before access is allowed; and the enterprise collects as much information as possible about the current state of assets, network infrastructure, and communications to improve its security posture.

TrustChain-AI operationalises ZTA tenets 4, 6, and 7 specifically for AI agent operations. Tenet 4 (dynamic policy) is implemented through the trust-state-dependent operation classification: whether a given operation is permitted depends not only on the agent's role (RBAC) but on its current trust state. Tenet 6 (dynamic authorisation) is implemented through the AdaptivePolicyEnforcer, which evaluates each operation request against the agent's current trust state retrieved from the VDR. Tenet 7 (continuous monitoring) is implemented through the telemetry submission system and trust audit trail.

Bernabe et al. [10] survey privacy-preserving solutions for blockchain-based access control, noting the tension between transparency (needed for auditability) and privacy (needed for user protection). While TrustChain-AI does not use blockchain, the auditability vs. privacy tension is relevant: the trust audit trail records all state transitions and the evidence basis for each, providing strong auditability, but in a production system, this data would need appropriate access control to prevent inference attacks on agent behaviour.

Zhang et al. [11] proposed a decentralised trust management and access control system for smart data environments, where data objects carry embedded access control policies that are enforced by a distributed trust computation network. Their system evaluates access requests by computing a requestor trust score from interaction history and matching it against the data object's required trust threshold. This concept is directly analogous to TrustChain-AI's operation classification (PRIVILEGED vs. STANDARD) and trust-state gating, though applied at the data object level rather than the operation type level.

**Summary and Gap:** Zero trust architecture and adaptive authorisation research provides the policy framework that justifies TrustChain-AI's trust-state-dependent operation gating. However, these works address human users and service accounts, not autonomous AI agents whose behavioural trust can change rapidly within a single session. The specific mapping from AI agent trust states to operation type permissions — and the precise characterisation of which operations are high-privilege in the AI agent context — is a novel contribution of TrustChain-AI.

## 2.6 Multi-Agent Systems and Agent Coordination

The Foundation for Intelligent Physical Agents (FIPA) [12] published a suite of standards for agent management and communication, including the FIPA Agent Management Specification that defines the Agent Management System (AMS) — a mandatory component of every FIPA-compliant agent platform that serves as a white pages service (identity registry) and lifecycle manager. The FIPA AMS maintains records of agent identifiers (AID), state (active, suspended, waiting, etc.), and transport addresses. Agents must register with the AMS before communicating, and the AMS can suspend or kill agents on administrative command.

TrustChain-AI's agent registry (Section 3.6) is conceptually analogous to the FIPA AMS: it maintains agent identities (DID-based AIDs), lifecycle state (active/inactive), and operational metrics. However, TrustChain-AI extends the FIPA model significantly by integrating trust state management (TRUSTED/SUSPICIOUS/QUARANTINED/REVOKED) into the registry, providing a capability-based yellow pages equivalent through the discovery and matching engine, and connecting registry state to dynamic authorisation enforcement — none of which are part of the FIPA AMS specification.

The FIPA Agent Communication Language (ACL) defines performatives (INFORM, REQUEST, QUERY-IF, etc.) for structured agent communication. TrustChain-AI's collaboration event model (message types: `task_request`, `response`, `update`) draws conceptual inspiration from ACL performatives while using a simpler REST-based JSON format appropriate for web-native deployment.

Shoker [13] proposed a self-stabilising autonomous distributed ledger designed for Byzantine fault tolerance in distributed systems. The work is relevant as a theoretical reference for the distributed VDR future scope (Section 6.4.1): a self-stabilising ledger provides automatic recovery from Byzantine participants, which aligns with TrustChain-AI's goal of maintaining registry integrity even when some registered agents are behaving incorrectly.

**Summary and Gap:** FIPA standards provide an established conceptual model for agent identity management and lifecycle control that TrustChain-AI extends with trust-state management and adaptive authorisation. FIPA protocols were designed for intranet agent platforms of the early 2000s; they do not address cryptographic identity (DID:key), verifiable credentials, or the internet-scale REST API patterns appropriate for modern AI agent deployment. TrustChain-AI modernises the FIPA registry model for the web-native, cryptographically-secured AI agent ecosystem.

## 2.7 Research Gap Analysis

**Table R1: Research Gap Analysis**

| Prior Work | Focus Area | Key Limitation | TrustChain-AI Contribution |
|-----------|-----------|---------------|---------------------------|
| Jøsang et al. [3] — Trust survey | Distributed reputation taxonomy | No cryptographic identity; single-dimension trust | Multi-factor EMA trust (S, C, L) + DID/VC identity |
| Kamvar et al. [4] — EigenTrust | P2P reputation propagation | Static graph; scalar trust; no identity verification | Dynamic agent registry; trust-state machine; VC-based identity |
| Mui et al. [5] — Bayesian trust | Probabilistic trust modelling | Binary cooperation metric; no capability dimension | Three-factor performance score; capability-specific discovery |
| Nitti et al. [6] — SIoT trust | IoT multi-dimensional trust | No cryptographic identity; no graduated auth enforcement | DID:key identity; adaptive policy enforcement |
| Azzedin & Maheswaran [7] — Grid trust | Context-sensitive trust | No standardised identity; no VC-based credentials | W3C DID/VC + context-sensitive match scoring |
| W3C DID [1] + VC [2] | Decentralised identity standards | Human identity focus; no behavioural trust integration | AI agent identity + behavioural EMA trust coupling |
| NIST ZTA [15] | Zero trust security model | Organisational policy framework; not agent-specific | Trust-state-gated operation classification for AI agents |
| FIPA AMS [12] | Agent lifecycle management | No cryptographic identity; no trust scoring; no adaptive auth | DID registry + trust scoring + adaptive authorisation |
| Zhang et al. [11] | Decentralised access control | Object-level control; no agent identity | Operation-level trust-state gating + RBAC |

## 2.8 Chapter Summary

This chapter surveyed fifteen works across five thematic areas relevant to TrustChain-AI. The distributed trust literature (Jøsang, EigenTrust, Mui, Azzedin) provides the theoretical basis for quantifying trust from interaction history. The IoT trust literature (Nitti) confirms the value of multi-dimensional trust metrics and temporal scoring. The SSI literature (W3C DID/VC, RFC 8037, ToIP, Fromknecht) provides the cryptographic identity foundation. The zero trust and adaptive authorisation literature (NIST, Zhang, Bernabe) provides the policy enforcement model. The multi-agent systems literature (FIPA, Shoker) provides the agent coordination context.

The gap analysis (Table R1) identifies that no prior work integrates all five dimensions: cryptographic verifiable identity, multi-factor behavioural trust scoring, trust-state-aware adaptive authorisation, capability-based trust-weighted discovery, and auditable evidence recording. TrustChain-AI addresses all five dimensions in a single, testable implementation. The following chapters describe the design, implementation, and verification of this framework.

---

*End of Part 1 — Continue in TrustChain_AI_Blackbook_Part2.md*
