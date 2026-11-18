"""The single source of facts about each guide: address, search title, description, version,
path, and the one-page summary. seo.py, build_sitemap.py and build_onepagers.py all read it.

To move the site to its own domain, change SITE here and run the three builders again.
When a guide is reviewed, change its version and REVIEWED below, then rebuild.
"""

SITE = "https://mohanparsha.github.io/architecturcareer/"
SITE_NAME = "Architect U'r Career"
AUTHOR = "Krishna Mohan Parsha"
LICENCE_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
REVIEWED = "2026-11-18"          # ISO date of the last review, used in structured data and the sitemap
REVIEWED_TEXT = "November 2026"  # the same date as readers see it
ONEPAGER_CAMPAIGN = "onepager"   # GoatCounter campaign name carried by the QR codes

PATHS = {
    1: "Start a security career",
    2: "Secure and govern AI",
    3: "Teach it",
}

# Order within each path follows the home page.
GUIDES = [
    {
        "slug": "network-concepts", "name": "Network Concepts Guide", "path": 1, "step": 1, "version": "2.1",
        "seo_title": "Network Concepts for Security: OSI, TCP/IP, Ports and Controls",
        "description": "OSI and TCP/IP explained layer by layer for security work: protocols, ports, attacks, controls, framework mappings and a searchable glossary.",
        "type": "Reference guide", "level": "Beginner", "audience": "student",
        "what": "OSI and TCP/IP explained layer by layer, for security work.",
        "who": "Final-year students and career switchers starting out in security.",
        "learn": [
            "What each OSI and TCP/IP layer does, and how the two models compare.",
            "How data is wrapped and unwrapped through the stack, and what really happens between typing a URL and seeing the page.",
            "The core protocols and their ports, TCP against UDP, IPv4 against IPv6, and subnetting.",
            "The attacks seen at each layer, and the controls that answer them.",
            "How those controls map to NIST CSF 2.0, ISO/IEC 27001:2022, CIS Controls v8.1 and MITRE ATT&CK, with a searchable glossary of 121 terms.",
        ],
    },
    {
        "slug": "cybersecurity-roadmap", "name": "Cybersecurity Career Roadmap", "path": 1, "step": 2, "version": "4.1",
        "seo_title": "Cybersecurity Career Roadmap for India, with Costs in Rupees",
        "description": "A free cybersecurity career roadmap for students in India: eight domains, an 18-month plan, exam costs in rupees, a fit quiz and free resources.",
        "type": "Career roadmap", "level": "Beginner to intermediate", "audience": "student",
        "what": "A career roadmap for security in India: the domains, an 18-month plan, and what it costs.",
        "who": "Students and career switchers in India choosing a first security role.",
        "learn": [
            "Eight security domains, what each job involves, and a short self-assessment to find your fit.",
            "An 18-month plan from foundations to job-ready, phase by phase.",
            "What a first certification route costs in rupees, with every price linked to the official page.",
            "Free practice platforms, and what to do in your first seven days for nothing.",
            "The entry-level market in India as it is, including why job-ready is not the same as job-landed.",
        ],
    },
    {
        "slug": "devops-devsecops-roadmap", "name": "DevOps and DevSecOps Roadmap", "path": 1, "step": 3, "version": "3.0",
        "seo_title": "DevOps and DevSecOps Roadmap for Students: 12 Months, 20 Projects",
        "description": "A 12-month DevOps and DevSecOps roadmap for students: monthly plan, 20 projects with cloud cost warnings, free labs, tools, certifications and a glossary.",
        "type": "Learning roadmap", "level": "Beginner to intermediate", "audience": "student",
        "what": "A twelve-month DevOps and DevSecOps plan, built around projects.",
        "who": "Computer science students and early-career engineers.",
        "learn": [
            "What DevOps and DevSecOps are, and the pipeline and tool chain that join them.",
            "A six-phase plan, month by month, for twelve months.",
            "Twenty graded projects, each marked free or paid, with a free or local alternative where the cloud costs money.",
            "How not to get billed while you learn on a cloud account.",
            "The security tools for each stage, certifications, career paths and interview preparation.",
        ],
    },
    {
        "slug": "secure-sdlc", "name": "Secure SDLC", "path": 1, "step": 4, "version": "3.1",
        "seo_title": "Secure SDLC: Stages, Tools, Worked Examples and Compliance Mapping",
        "description": "Eight stages of a secure software development lifecycle: activities, tools, worked examples, RACI, example KPIs and a clause-level compliance map.",
        "type": "Reference guide", "level": "Intermediate", "audience": "student",
        "what": "Security at every stage of software delivery, with the clause behind each requirement.",
        "who": "Developers, testers and security engineers, and students preparing for those roles.",
        "learn": [
            "The eight stages, from training and requirements to incident response and decommissioning.",
            "The activities and tools for each stage, marked essential, recommended or advanced.",
            "One worked example per stage of what a team actually does.",
            "Where security gates sit in a CI/CD pipeline, who is responsible for what, and what to measure.",
            "A compliance map that names the clause behind every tick: NIST SSDF, OWASP SAMM, ISO/IEC 27001, PCI DSS, SOC 2, GDPR, HIPAA, and India's DPDP and CERT-In rules.",
        ],
    },
    {
        "slug": "ai-knowledge-map", "name": "The AI Knowledge Map", "path": 2, "step": 1, "version": "3.0",
        "seo_title": "The AI Knowledge Map: Eleven Core AI Ideas and How They Connect",
        "description": "Eleven core AI terms, from machine learning to MCP and agentic AI, as an interactive map with a reading order, labelled relationships and a plain list view.",
        "type": "Concept map", "level": "Beginner", "audience": "student",
        "what": "Eleven core ideas of modern AI, in the order to learn them.",
        "who": "Engineers, students and managers new to AI.",
        "learn": [
            "What AI, machine learning, deep learning and natural language processing are, and how each sits inside the last.",
            "What generative AI and large language models are.",
            "How retrieval-augmented generation (RAG) gives a model the facts it needs.",
            "What makes an AI agent, and the two protocols agents use: MCP for tools and A2A for other agents.",
            "A reading order, a map of how the ideas relate, and questions to check yourself.",
        ],
    },
    {
        "slug": "agentic-ai-runtime", "name": "Agentic AI Runtime Architecture", "path": 2, "step": 2, "version": "3.1",
        "seo_title": "Agentic AI Runtime Architecture: Agent Loop, Layers and Controls",
        "description": "An interactive diagram of an AI agent runtime: the execution loop, seven layers, security controls and orchestration patterns, each with a code sample.",
        "type": "Architecture reference", "level": "Intermediate to advanced", "audience": "professional",
        "what": "How an AI agent runtime is built, and what keeps it within bounds.",
        "who": "Engineers and architects who build or review AI agents.",
        "learn": [
            "The agent loop: perceive, plan, act, observe, adapt.",
            "A seven-layer runtime stack, from the API gateway down to models and vector storage, component by component.",
            "Memory, tools, and the agent protocols MCP and A2A as they stood in November 2026.",
            "The controls that bound an agent (its own identity, policy at the tool boundary, human approval, budgets) and what each does not stop.",
            "Five orchestration patterns, with code samples, some of them runnable as written.",
        ],
    },
    {
        "slug": "ai-security", "name": "Securing AI Systems and Agents", "path": 2, "step": 3, "version": "4.0",
        "seo_title": "Securing AI Systems and Agents: A Practitioner's Reference",
        "description": "A practitioner's reference to securing AI systems and agents: seven layers, one attack walked through at each, the control, what it does not stop, and how to prove it.",
        "type": "Practitioner reference", "level": "Intermediate to advanced", "audience": "professional",
        "what": "Securing AI systems and agents layer by layer: the attack, the control, and what the control does not stop.",
        "who": "Working engineers and security staff responsible for AI systems.",
        "learn": [
            "Why prompt injection cannot be prevented, only contained, and what that changes about design.",
            "Seven layers, from supply chain to governance, each with an attack walked through, the control, what it does not stop, and how to prove it works.",
            "How it all maps to the 2026 OWASP Top 10 lists for LLM and agentic applications, and to MITRE ATLAS.",
            "Eleven real incidents from 2024 to 2026, and the control that would have contained each.",
            "What Indian law and regulators expect, and ten things to do first.",
        ],
    },
    {
        "slug": "data-intelligence-layer", "name": "Data Intelligence Layer", "path": 2, "step": 4, "version": "1.1",
        "seo_title": "Data Intelligence Layer: Catalogue, Lineage, Quality and Governance",
        "description": "How data catalogue, quality, lineage and governance form a control plane over enterprise data, with data mesh, data fabric, the lakehouse and example tools.",
        "type": "Architecture guide", "level": "Intermediate", "audience": "professional",
        "what": "How catalogue, lineage, quality and governance work together as a control plane over enterprise data.",
        "who": "Data, analytics and governance engineers, and students heading that way.",
        "learn": [
            "A five-layer view of enterprise data, from sources to consumption.",
            "Batch and streaming processing, and the warehouse, the lake and the lakehouse.",
            "The intelligence layer itself: catalogue, lineage, quality, governance, access and privacy.",
            "Data mesh and data fabric, as architecture approaches rather than products.",
            "Example tools in each category, with a disclosure of the author's interests, and a maturity model.",
        ],
    },
    {
        "slug": "iks-life-skills", "name": "IKS Life Skills Curriculum", "path": 3, "step": 1, "version": "1.1",
        "seo_title": "IKS Life Skills Curriculum for Classes 9 to 12",
        "description": "A 12-week life skills curriculum for Classes 9 to 12 drawing on Indian Knowledge Systems, with session plans, simulations, rubrics and cited sources.",
        "type": "Curriculum", "level": "Secondary school, Classes 9 to 12", "audience": "teacher",
        "what": "A twelve-week life skills curriculum drawing on Indian Knowledge Systems, ready to teach.",
        "who": "Teachers of Classes 9 to 12, and school heads.",
        "learn": [
            "Twelve weekly modules at three tiers, with session plans, simulations and rubrics.",
            "Stories from many traditions, each cited by text, book and verse, and open to discussion.",
            "Safeguarding notes for facilitators: role-plays are announced, volunteers can opt out, nothing is staged.",
            "Printable scenario cards and a facilitator note for every week.",
            "How it relates to UGC Jeevan Kaushal 2.0. It is an independent work, not endorsed by UGC, NCERT, CBSE or any government body.",
        ],
    },
    {
        "slug": "thinking-skills", "name": "Thinking Skills", "path": 3, "step": 3, "version": "3.1",
        "seo_title": "Thinking Skills: Critical, Analytical and Design Thinking, with Labs",
        "description": "Critical, analytical and design thinking for students: 10 foundations, 19 frameworks, 36 self-contained labs, Nyaya reasoning and ten workplace skills.",
        "type": "Study guide", "level": "Undergraduate and early career", "audience": "student",
        "what": "Critical, analytical and design thinking, practised through labs.",
        "who": "Students and early-career professionals, and the teachers who run the labs.",
        "learn": [
            "Ten foundations to learn before any framework.",
            "Nineteen frameworks for critical, analytical and design thinking.",
            "Thirty-six labs, each with its own materials, worksheet and facilitator note, ready to print.",
            "The Nyaya tradition of reasoning, and purva paksha: stating the other side fairly before answering it.",
            "Ten skills employers ask about, with verified courses, and three study plans to choose from.",
        ],
    },
    {
        "slug": "os-unit-1", "name": "Operating Systems Unit 1", "path": 3, "step": 4, "version": "3.3",
        "seo_title": "Operating Systems Unit 1: Processes, System Calls and CPU Scheduling",
        "description": "Interactive revision reference for a first operating systems unit: OS structure, system calls, processes and CPU scheduling, with worked calculations.",
        "type": "Revision reference", "level": "Undergraduate", "audience": "student",
        "what": "A revision reference for a first unit in operating systems, following Silberschatz, Galvin and Gagne, 10th edition.",
        "who": "Undergraduates in a first operating systems course, and their teachers.",
        "learn": [
            "What an operating system is, how a computer system is organised, and dual-mode operation.",
            "Operating-system services, interfaces and structures, and how a system call works.",
            "Processes, the process control block, and fork and exec.",
            "CPU scheduling, with five worked calculations checked step by step.",
            "A two-minute revision strip, common exam traps, a glossary and self-test questions.",
        ],
    },
]

# Pages that are not guides but belong in the sitemap.
OTHER_PAGES = [
    {"path": "", "changefreq": "monthly"},
    {"path": "iks-life-skills/cards/", "changefreq": "yearly"},
    {"path": "print/", "changefreq": "yearly"},
    {"path": "about/", "changefreq": "monthly"},
]


def by_slug(slug):
    return next(g for g in GUIDES if g["slug"] == slug)


def next_on_path(guide):
    """The guide that follows this one on its path, or None. The card pack is step 2 of path 3 and has no one-pager."""
    later = sorted((g for g in GUIDES if g["path"] == guide["path"] and g["step"] > guide["step"]), key=lambda g: g["step"])
    return later[0] if later else None


def url(slug):
    return SITE + slug + "/"
