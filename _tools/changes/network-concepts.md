Network Concepts Guide, version 2.1 (November 2026)

- Replaced two diagrams that taught wrong things. The attack lifecycle drawing had mislabelled stages, and the packet flow drawing put ARP after the TCP and TLS handshakes and called ports a Layer 3 idea. Both are redrawn, each with a text version underneath.
- Corrected the ISO/IEC 27001:2022 references: A.8.21 is Security of network services (web filtering is A.8.23), CCTV belongs to A.7.4 Physical security monitoring and cable shielding to A.7.12 Cabling security. Every control now carries its published title.
- Corrected the MITRE ATT&CK table against version 20.1: SQL injection sits under Initial Access (Exploit Public-Facing Application, T1190), ARP poisoning is a sub-technique of Adversary-in-the-Middle under Credential Access and Collection, and the entries with no matching technique were removed.
- Replaced "Threat + Vulnerability = Risk" with the NIST SP 800-30 definition: risk depends on the likelihood that a threat exploits a vulnerability and on the impact if it does.
- Corrected the CIS Controls entry to version 8.1 (18 Controls, 153 Safeguards) and the NIST CSF 2.0 mapping (physical access is PR.AA-06; firewalls and segmentation are PR.IR-01).
- Rebuilt the port table with a TCP or UDP column and added the ports it lacked: 20, 88 (Kerberos), 135, 179 (BGP), 445 (SMB), 587, 1812 and 1813 (RADIUS), 6514, and UDP 443 for HTTP/3.
- Added what was missing from the flow and the protocol notes: NAT, QUIC and HTTP/3, TLS 1.3, and DNS over TCP.
- Merged the separate glossary into this page as a searchable section: all 105 terms kept and put in true alphabetical order, errors fixed (PPTP, DNS transport, the risk formula), and 16 terms added, including RPKI, HSTS, RADIUS, Kerberos, SMB, DNSSEC and NGFW.
- Corrected protocol statements: IPsec is not mandatory in IPv6, SCTP uses a four-way handshake, TCP is reliable but cannot guarantee delivery, and routers do change a packet in transit (TTL and the IPv4 checksum), as do NAT devices and proxies.
- Corrected two attributions: a BGP hijack succeeds because route origins are not validated, not because the session lacks authentication; and "verify explicitly, least privilege, assume breach" is Microsoft's summary of Zero Trust, not text from NIST SP 800-207.
- Added a caution beside the defence in depth image, links to the sources used, and links to the Cybersecurity Career Roadmap, Operating Systems Unit 1 and Secure SDLC guides.
- Made the page easier to use from the keyboard and on a phone: the tabs keep working with the arrow keys, the glossary search works without a mouse, and the page now states its licence (CC BY-NC-SA 4.0).
