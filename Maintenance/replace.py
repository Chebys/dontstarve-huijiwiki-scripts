import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import *

replacements = [
    (r'辣椒面', r'辣椒碎'),
]
category = '联机版'
template = None

if len(replacements) == 1:
    pages = [site.pages[item['title']] for item in site.search('辣椒面')]
else:
    pages = get_pages(category=category, template=template)
for page in tqdm(pages):
    text = page.text()
    newtext = text
    for old, new in replacements:
        newtext = newtext.replace(old, new)
    if newtext != text:
        page.save(newtext, summary='批量替换文本')