#!/uesr/bin/python3.7.4
#coding=utf-8
#Auther:清梦XXC
#@Time:2019/12/13 19:33
import requests
import execjs
from lxml import etree
from useragentxxc import PersonComputer as PC
from urllib.parse import quote
from multiprocessing import Pool


def get():
    key = input("输入查询内容：")
    url = f'https://www.meipai.com/search/all?q={quote(key)}'
    headers = {
        "Referer": "https://www.meipai.com/",
        "User-Agent": PC.random()
    }
    res = requests.get(url, headers=headers).content.decode("utf-8")
    codes = etree.HTML(res).xpath('//*[@class="content-l-video content-l-media-wrap pr cp"]/@data-video')
    return codes


def decrypt(code):
    with open("meipai.js")as f:
        JS = f.read()
    result = execjs.compile(JS).call("decode", code)
    if result[-1] == "@":
        result = result[:-1]
    print(result)


if __name__ == '__main__':
    p = Pool(processes=4)
    p.map(decrypt, get())

