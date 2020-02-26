# coding=utf-8
import requests, re, os
from urllib.request import quote
from lxml import etree
from multiprocessing import Pool
from ffmpy3 import FFmpeg
from prettytable import PrettyTable

order, infors = 1, []
table = PrettyTable(['序号', 'up主', '标题', '视频时长', '投稿日期', '播放量', '试看链接'])
path = 'D:\哔哩哔哩视频'
path_ = 'D:\哔哩哔哩视频\m4s文件集'


def _checkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def _existFile(filePath):
    return os.path.exists(filePath)

def _getData(content, page):
    global order, infors
    url = 'https://search.bilibili.com/all?keyword=%s&from_source=banner_search&page=%d' % (quote(content), page)
    headers = {
        'Referer': 'https://www.bilibili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    if page == 1:
        responses = etree.HTML(requests.get(url, headers=headers).content.decode('utf-8')) \
            .xpath('//*[@id="all-list"]/div[1]/div[2]/ul[2]/li')
        if responses == []:
            responses = etree.HTML(requests.get(url, headers=headers).content.decode('utf-8')) \
                .xpath('//*[@id="all-list"]/div[1]/div[2]/ul/li')
    else:
        responses = etree.HTML(requests.get(url, headers=headers).content.decode('utf-8')) \
            .xpath('//*[@id="all-list"]/div[1]/ul/li')
    for response in responses:
        infors.append([str(order),  # 序号
                       response.xpath('./div/div[3]/span[4]/a/text()')[0],  # up主
                       response.xpath('./div/div[1]/a/@title')[0],  # 标题
                       response.xpath('./a/div/span[1]/text()')[0],  # 视频时长
                       response.xpath('./div/div[3]/span[3]/text()')[0]  # 投稿日期
                      .replace('\n', '').replace(' ', ''),
                       response.xpath('./div/div[3]/span[1]/text()')[0]  # 播放量
                      .replace('\n', '')
                      .replace(' ', ''),
                       'https:' + response.xpath('./div/div[1]/a/@href')[0]  # 试看链接
                      .split('?')[0]])
        order += 1  # 序号增加


def _getUrlsForPages(content, pages=1):
    global table, infors
    for page in range(1, pages + 1):
        _getData(content, page)
    for info in infors:
        table.add_row(info)
    print(table)
    number = input('输入要下载的视频序号：').split('.')
    return [infors[int(i) - 1][-1] for i in number]


def download(url, savePath, childPath, fileName):
    global path
    print(url)
    headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Range': 'bytes=0-'
    }
    hv = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    response: str = requests.get(url, headers=hv).content.decode('utf-8')
    urls1 = re.findall('"baseUrl":"(.+?)"', response)  # 获取m3p视频url
    urls2 = re.findall('"url":"(.+?)"', response)  # 获取flv视频url
    # 下载m3p视频
    if urls1 != []:
        print(fileName + '开始下载!')
        print(urls1[0], "-----", urls1[-1])
        with open(childPath + '\%s.mp4' % (fileName), 'wb')as f:
            f.write(requests.get(urls1[0], headers=headers).content)
        with open(childPath + '\%s.mp3' % (fileName), 'wb')as f:
            f.write(requests.get(urls1[-1], headers=headers).content)
        try:
            ff: FFmpeg = FFmpeg(
                executable="D:\Python\\ffmpeg\\ffmpeg-20200224-bc9b635-win64-static\\bin\\ffmpeg.exe",
                inputs={childPath + '\%s.mp4' % (fileName): None, childPath + '\%s.mp3' % (fileName): None},
                outputs={savePath + '\%s.mp4' % (fileName): '-c:v copy -c:a aac -strict experimental'}) # '-c:v h264 -c:a ac3'
            print(ff, "-------------------------------------")
            ff.run()
        except:
            print(fileName + "音视频合成失败！！失败日志已被屏蔽！！")
        print(fileName + '下载完成!')
    # 下载flv视频
    else:
        print(fileName + '开始下载!')
        with open(savePath + '\%s.flv' % (fileName), 'wb')as f:
            f.write(requests.get(urls2[0], headers=headers).content)
        print(fileName + '下载完成!')

def downloadsAll(url):
    minPage = 1
    maxPage = 1
    _checkPath(path)
    _checkPath(path_)
    hv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    pageTile = etree.HTML(requests.get(url, headers=hv).content.decode('utf-8'))\
        .xpath('//*[@id="viewbox_report"]/h1/@title')[0]
    print("pageTile:", pageTile)
    # 创建子目录
    childPath = path_ + "\\" + pageTile
    savePath = path + "\\" + pageTile
    _checkPath(childPath)
    _checkPath(savePath)
    multiPage = etree.HTML(requests.get(url, headers=hv).content.decode('utf-8'))\
        .xpath('//*[@id="multi_page"]/div[2]/ul/li')
    # multiPage不为空则说明此链接下有视频选集（即多个子视频）
    if multiPage != []:
        maxPage = len(multiPage)
    print("maxPage:", maxPage)
    for p in range(minPage, maxPage + 1):
        _url = url + '?p=%d' %(p)
        # 如果是单视频则文件名就是父目录名
        if (maxPage == 1):
            fileName = pageTile
        # 否则是多视频，文件名为子目录名
        else:
            print(etree.tostring(multiPage[p - 1]))
            # 这里居然获取不到子视频集的名字，可能是js动态加载出来的，所以这里获取不到（网页源码是有的）
            # fileName = multiPage[p].xpath('./a/@title')[0]
            fileName = str(p)
        # 如果文件存在，则跳过本次下载
        if _existFile(savePath + '\%s.mp4' % (fileName)):
            continue
        if _existFile(childPath + '\%s.mp4' % (fileName)):
            continue
        download(_url, savePath, childPath, fileName)

def start(content,pages):
    urls = _getUrlsForPages(content, pages=pages)  # 获取待下载URL集
    pool = Pool(processes=4)  # 设置处理器个数
    pool.map(downloadsAll, urls)
    pool.close()

if __name__ == '__main__':
    content = input('输入内容：')  # 爬取关键字
    pages = 3  # 爬取总页数
    start(content,pages)

    # 测试下载程序OK
    # downloadsAll("https://www.bilibili.com/video/av75859780")
