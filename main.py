from mwclient import *
from mwparserfromhell import parse
from tqdm import tqdm
import json
from pathlib import Path
from zipfile import ZipFile
import pandas as pd
from bs4 import BeautifulSoup
import polib
import shutil
from pypinyin import lazy_pinyin
import re
from hashlib import md5

with open('config.json','r', encoding='utf-8') as f:
    config = json.load(f)

site = Site('dontstarve.huijiwiki.com', custom_headers={
            'X-authkey': config["huijiwiki"]["X-authkey"]})
site.login(
    username = config["huijiwiki"]["username"],
    password = config["huijiwiki"]["password"],
)

dst_path = Path(config["dontstarve"]["dst_path"])
ds_path = Path(config["dontstarve"]["ds_path"])

steam_username = config["steam"]["username"]
steam_password = config["steam"]["password"]

def touch_all():
    for item in tqdm(list(site.search('创建缩略图出错'))):
        site.pages[item['title']].touch()

def get_pages(template=None, category=None):
    if template and category:
        pages_using_template = {
            p.name for p in site.pages['Template:' + template].embeddedin()}
        res = list(p for p in site.categories[category] if p.name in pages_using_template)
        return res
    elif template:
        return list(site.pages['Template:' + template].embeddedin())
    elif category:
        return list(site.categories[category])
    return list(site.allpages())

def get_param(template, index, default=''):
    try:
        return str(template.get(index).value).strip()
    except ValueError:
        return default

if __name__ == '__main__':
    print('不要直接运行这个文件，要更新哪些数据就去运行对应的脚本。')