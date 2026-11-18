DevOps and DevSecOps Roadmap, version 3.0 (November 2026)

- Corrected the AWS Free Tier text. Accounts created from 15 July 2025 get up to USD 200 in credits and a six-month free plan, not 12 months of free use. Checked on aws.amazon.com on 18 November 2026.
- Added a "How not to get billed" box: which plan you are on, budget alerts, deleting resources the same day, never committing keys, and staying local where you can.
- Added a cost line to each of the 20 projects. The five that use billed AWS services (8, 10, 16, 17 and 19) now say so plainly and give a free or local way to practise the same skill.
- Removed Play with Docker and Play with Kubernetes, which Docker withdrew from 1 March 2026. The free labs listed now are Killercoda and iximiuz Labs, with kind and minikube for a cluster on your own machine.
- Replaced Promtail with Grafana Alloy for shipping logs to Loki. Promtail reached end of life on 2 March 2026.
- Replaced DynamoDB state locking with the Terraform S3 backend's own lock file (use_lockfile), generally available since Terraform 1.11.
- Added Gateway API beside Ingress throughout. The ingress-nginx controller was retired in March 2026 and the Ingress API is frozen.
- Corrected licences and names: HashiCorp Vault is under the Business Source License and is no longer listed as open source (OpenBao is the open-source fork); "OWASP ZAP" is now "ZAP by Checkmarx".
- Moved secrets scanning (Gitleaks) to the commit stage of the pipeline, corrected the note on Kubernetes Secrets (stored unencrypted by default), and added advice to pin GitHub Actions to a commit SHA after the March 2026 Trivy compromise.
- Removed figures that had no source (GitHub star counts, community member counts, "2x faster") and fixed or removed three broken or misleading community links.
- Updated certifications: the Docker Certified Associate is sold by Mirantis; added the two exam fees confirmed on the providers' pages and a note to check the current fee before paying.
- Added the version and review date, links to the Secure SDLC, Cybersecurity Roadmap and Network Concepts guides, a labelled and keyboard-operable menu, and British spelling throughout.
