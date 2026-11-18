Secure SDLC: an interactive reference, version 3.1 (November 2026)

- Rebuilt the compliance table. It used to tick every cell. Each cell now names the clause, requirement or practice it rests on (52 of 64 cells), empty cells stay empty, and every reference is written out by stage underneath.
- Corrected the framework references: ISO/IEC 27001 now uses 2022 numbering (A.14 was the 2013 edition), PCI DSS is cited as v4.0.1, incident response and breach notification point to the clauses that actually cover them, and NIST SSDF and SP 800-218 are shown as one document.
- Added India: the CERT-In Directions (6-hour incident reporting, 180-day logs) and the DPDP Act and Rules, with the note that their security and breach duties start in May 2027.
- Replaced tools that are archived or no longer developed: SeaSponge (now Threagile), Terrascan (Conftest), TheHive (DFIR-IRIS), tfsec (Trivy's own IaC scanner), kube-hunter (Kubescape), OWASP SKF (OWASP Cornucopia), Archery (DefectDojo) and YARA (YARA-X). Updated the OWASP Dependency-Check link to its new home.
- Tool descriptions are now plain text beside each tool. They used to appear only on mouse hover, so they did not exist on a phone or for keyboard users.
- Added a short worked example to each of the eight stages. They are illustrative, not accounts of real incidents.
- Stopped calling every tool "open source": commercial, proprietary and source-available tools now carry a label, and "HackTheBox CE", which does not exist, is plain Hack The Box.
- Renamed "OWASP ZAP" to ZAP (it left OWASP in 2023), SonarQube CE to SonarQube Community Build, and dropped DREAD from the threat-modelling step, with the source for why.
- Removed the unsourced "catches 80%" claim, corrected the tool count (67, not "75+"), and marked the KPI figures as example targets, not industry benchmarks.
- Renamed the page from "The Definitive Reference Guide" to "Secure SDLC: an interactive reference" and set one version and date everywhere (it said v2.0 and v3.0 in different places).
- Each stage header is now a real button, the page reads in full without JavaScript, section titles are proper headings, and the wide tables scroll inside their own box on a phone.
- Added links to the DevOps and DevSecOps roadmap, the cybersecurity career roadmap and the AI security guide, plus the site's shared header, footer and licence (CC BY-NC-SA 4.0).
