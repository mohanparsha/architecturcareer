"""Write a small redirect page at every old address, so links already shared keep working.

Run from the repository root:  python _tools/make_stubs.py
Each stub carries a canonical link, an instant redirect that keeps any #fragment, and a plain link
for readers without JavaScript. GitHub Pages cannot send a real 301, so this is the nearest thing.
"""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mohanparsha.github.io/architecturcareer/"

# old file name -> (new address relative to the site root, guide name)
MOVED = {
    "cybersecurity-roadmap.html": ("cybersecurity-roadmap/", "Cybersecurity Career Roadmap"),
    "devops-roadmap-colorful-v2.6.html": ("devops-devsecops-roadmap/", "DevOps and DevSecOps Roadmap"),
    "Secure_SDLC_Interactive_visual_v3.0.html": ("secure-sdlc/", "Secure SDLC"),
    "network_concepts_guide.html": ("network-concepts/", "Network Concepts Guide"),
    "network_glossary.html": ("network-concepts/#glossary", "Network Concepts Guide (the glossary is now part of it)"),
    "OS_Unit1_Reference_Guide.html": ("os-unit-1/", "Operating Systems Unit 1"),
    "agentic-ai-runtime-architecture_3.0.html": ("agentic-ai-runtime/", "Agentic AI Runtime Architecture"),
    "ai_security_stack_v3.0.html": ("ai-security/", "Securing AI Systems and Agents"),
    "ai-knowledge-map_v2.5.html": ("ai-knowledge-map/", "The AI Knowledge Map"),
    "data-intelligence-layer-guide.html": ("data-intelligence-layer/", "Data Intelligence Layer"),
    "ThinkingSkillsRoadmap_3.0.html": ("thinking-skills/", "Thinking Skills"),
    "top-10-soft-skills-V2.5.html": ("thinking-skills/#soft-skills", "Thinking Skills (the ten soft skills are now part of it)"),
    "iks_life_skills_curriculum.html": ("iks-life-skills/", "IKS Life Skills Curriculum"),
    "jeevan_kaushal_curriculum.html": ("iks-life-skills/#ugc-jeevan-kaushal", "IKS Life Skills Curriculum (this page is now a section of it)"),
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved: {name} | Architect U'r Career</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{site}{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>
(function () {{
  var target = "{target}";
  var hash = target.indexOf("#") === -1 ? location.hash : "";
  location.replace(target + hash);
}})();
</script>
<style>body{{font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem;color:#0b1220}}a{{color:#047857}}</style>
</head>
<body>
<p>This page has moved. Go to <a href="{target}">{name}</a>, or to the <a href="./">Architect U'r Career home page</a>.</p>
</body>
</html>
"""

if __name__ == "__main__":
    for old, (target, name) in sorted(MOVED.items()):
        path = os.path.join(ROOT, old)
        io.open(path, "w", encoding="utf-8", newline="\n").write(TEMPLATE.format(site=SITE, target=target, name=name))
        print("stub", old, "->", target)
