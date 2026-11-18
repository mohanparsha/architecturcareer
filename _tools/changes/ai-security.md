# Version 4.0, November 2026

- Rewritten from the start. The earlier "AI Security Stack" was six cards of headings; this is a reference with seven layers, and for each one an attack walked through step by step, the control, what the control does not stop, and how you would prove the control works.
- Corrected the central claim. The earlier page listed "prompt injection detection and prevention". Prompt injection cannot be reliably prevented, only made less likely and contained, and the page now starts from that fact and cites the UK NCSC, OpenAI and Anthropic saying so.
- Added the two layers the earlier page lacked: agents, tools and actions (identity, policy at the tool boundary, human approval, revocation), and governance and evidence.
- Added indirect prompt injection, output handling and retrieval permissions, none of which the earlier page mentioned.
- Mapped every layer to the OWASP Top 10 for LLM Applications 2026, the OWASP Top 10 for Agentic Applications 2026 and MITRE ATLAS 2026.10, with a warning that the OWASP numbering changed between the 2025 and 2026 editions.
- Added eleven documented incidents from 2024 to 2026, each linked to the vendor advisory, CVE record or original research, with the control that would have contained it.
- Added the Indian regulatory reading: the DPDP Act and Rules (with the fact that the security and breach duties commence in mid-May 2027), the CERT-In Directions and AI guidance, RBI, SEBI, the India AI Governance Guidelines, ISO/IEC 42001 and 27090, and the amended EU AI Act dates.
- Removed errors from the earlier page: NIST SSDF and SP 800-218 listed as two documents (they are one), and PCI DSS cited as the standard for AI API security.
- Added a ten-point starting baseline and free places to practise.
