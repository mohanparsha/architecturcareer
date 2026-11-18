"""Make the shared footer's two outbound links open in a new tab, on every guide.

Run from the repository root:  python _tools/normalise_shell.py
Safe to run again: it changes nothing once every page is in the normal form.
"""
import glob, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
changed = 0
for path in sorted(glob.glob(os.path.join(ROOT, "*", "index.html")) + glob.glob(os.path.join(ROOT, "*", "*", "index.html"))):
    if os.sep + "_" in path:
        continue
    s = io.open(path, encoding="utf-8", newline="").read()
    m = re.search(r'<footer class="auc-foot">.*?</footer>', s, re.S)
    if not m:
        continue
    foot = m.group(0)
    new = foot.replace('<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">',
                       '<a rel="license noopener" target="_blank" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">')
    new = re.sub(r'<a href="(https://github\.com/mohanparsha/architecturcareer/issues/new[^"]*)">',
                 r'<a target="_blank" rel="noopener" href="\1">', new)
    if new != foot:
        io.open(path, "w", encoding="utf-8", newline="").write(s.replace(foot, new))
        changed += 1
        print("normalised", os.path.relpath(path, ROOT))
print("pages changed:", changed)
