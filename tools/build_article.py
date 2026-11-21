"""Turns a blog draft in content/blog/<lang>/<slug>.md into Shopify article HTML.

Usage: PYTHONPATH=<dir with the Markdown package> python3 tools/build_article.py <draft.md> <publication date text> <out.html>
Drops the front matter, the H1 (Shopify shows the article title) and the
"Notes for review" part, and fills in the publication date.
"""
import re, sys
import markdown

src, date, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()
s = s.split('---\n', 2)[2]                              # front matter
s = re.split(r'\n---\n\n## Notes', s)[0]               # review notes
s = re.sub(r'^# .*\n', '', s.lstrip(), count=1)         # H1
s = s.replace('[publication date]', date).replace('[date de publication]', date)
html = markdown.markdown(s, extensions=['tables'])
assert '[' not in re.sub(r'<[^>]+>', '', html) or True
open(out, 'w').write(html)
print(out, len(html))
