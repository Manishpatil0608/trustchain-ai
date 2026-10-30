# TrustChain-AI Blackbook — Report QA Checklist

Use this checklist to verify the final report before submission.

---

## 1. Preliminary Pages

- [ ] Title page: Project title, degree, department, university, student names + roll numbers, mentor, academic year
- [ ] Certificate: Signed by Internal Guide, HoD, External Examiner; seal placeholder present
- [ ] Acknowledgement: Mentor, department, university acknowledged
- [ ] Abstract: 250–300 words; problem, solution, methodology, results, contribution
- [ ] Table of Contents: All chapters, sections, references, appendices listed with page numbers
- [ ] List of Figures: All 12 figures listed with figure number and page number
- [ ] List of Tables: All 10 tables listed with table number and page number
- [ ] List of Abbreviations: All technical abbreviations expanded
- [ ] Symbols and Notations: P_i(t), T_i(t), S_i(t), C_i(t), L_i(t), w1, w2, w3, lambda, tau_trusted, tau_suspicious

---

## 2. Trust Model Accuracy (CRITICAL)

- [ ] P_i(t) = 0.6·S + 0.3·C + 0.1·(1-L) — EXACT weights
- [ ] T_i(t) = 0.7·P + 0.3·T_prev — EXACT lambda=0.7
- [ ] TRUSTED threshold: T >= 0.8
- [ ] SUSPICIOUS threshold: 0.5 <= T < 0.8
- [ ] QUARANTINED threshold: T < 0.5
- [ ] REVOKED: terminal, admin-only, not triggered by threshold
- [ ] Initial trust: 1.0 (TRUSTED)
- [ ] Window: last 10 telemetry events

---

## 3. Match Score Formula (CRITICAL)

- [ ] match_score = 0.4·T + 0.3·(r/5.0) + 0.2·σ + 0.1·(1-λ) — EXACT weights
- [ ] normalized_latency = min(latency_ms / 2000, 1.0)

---

## 4. Adaptive Authorization (CRITICAL)

- [ ] PRIVILEGED_OPERATIONS listed: workflow:execute, workflow:orchestrate, agent:delegate, credential:issue, admin:revoke, admin:manage, sensitive:execute
- [ ] STANDARD_OPERATIONS listed: read, query, map:generate, task:execute, collaboration:step, collaboration:participate
- [ ] SUSPICIOUS + PRIVILEGED → HTTP 403
- [ ] SUSPICIOUS + STANDARD → Permitted with audit record
- [ ] QUARANTINED → 403 all operations
- [ ] REVOKED → 403 all operations, permanent

---

## 5. Technology Stack Accuracy

- [ ] Python 3.12.3
- [ ] FastAPI 0.141.1
- [ ] SQLAlchemy 2.0.52
- [ ] Pydantic 2.13.5
- [ ] PyNaCl 1.6.2
- [ ] PyJWT 2.14.0
- [ ] argon2-cffi 25.1.0
- [ ] React 19.2.8
- [ ] Vite 8.2.2
- [ ] Tailwind CSS 4.3.3
- [ ] Recharts 3.10.1

---

## 6. Honest Limitation Statements (REQUIRED)

- [ ] VDR is local SQLite (`vdr.db`) — NOT distributed, NOT blockchain — stated clearly
- [ ] LocalAgentConnector is structured local execution engine — NOT live LLM inference — stated clearly
- [ ] PARALLEL workflow pattern: schema-supported only, not tested — labeled as future scope
- [ ] VC API key validation disabled in development mode
- [ ] Trust weights are static, not context-adaptive

---

## 7. Test Results

- [ ] 77 tests PASSED, 0 failed — stated in Chapter 4 and Appendix C
- [ ] No fabricated test results beyond what is verified
- [ ] Key test names cited correctly

---

## 8. References

- [ ] All 15 references are real, verifiable papers/standards
- [ ] All in-text citations [1]-[15] match the reference list
- [ ] No references cited that are NOT in the list
- [ ] IEEE formatting used consistently

---

## 9. Figures and Tables

- [ ] All 12 figures referenced in text as "Figure X"
- [ ] All 10 tables referenced in text as "Table X"
- [ ] Figures have captions
- [ ] Tables have titles

---

## 10. Chapter Completeness

- [ ] Chapter 1: Background, Problem Statement, 6 Objectives, Scope, Solution Overview, Contributions, Report Organization, Summary
- [ ] Chapter 2: 6 thematic sections, Research Gap Table, Summary
- [ ] Chapter 3: All 13 subsections (Architecture through Frontend), trust equations, match formula, auth matrix, DB schema, API inventory
- [ ] Chapter 4: Test results table, health verification, trust worked example, auth verification, objectives matrix
- [ ] Chapter 5: 6 advantages, 6 limitations, 5 applications
- [ ] Chapter 6: Conclusion, 3 contributions, 7 future scope items, Final Remarks
- [ ] References: All 15 listed
- [ ] Appendix A: API endpoint table
- [ ] Appendix B: DB schema summary
- [ ] Appendix C: Test results
- [ ] Appendix D: Trust math reference

---

## 11. Formatting

- [ ] Numbered sections (1.1, 1.2, 2.1, etc.)
- [ ] Equations use LaTeX math formatting
- [ ] Tables are formatted (not broken)
- [ ] Academic professional tone throughout
- [ ] No placeholder [TODO] markers remaining
- [ ] Student name/roll: [STUDENT NAME] / [ROLL NUMBER] placeholders — to be filled by student
- [ ] Mentor name: [MENTOR NAME] — to be filled by student
