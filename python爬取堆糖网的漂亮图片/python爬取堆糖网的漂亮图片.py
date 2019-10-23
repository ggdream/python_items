#!/uesr/bin/python3.7.4
#coding=utf-8
#Auther:清梦XXC
#@Time:2019/10/23 21:14
import PC
import time,requests
from urllib.request import urlretrieve
def link(start):
    url='https://www.duitang.com/napi/blog/list/by_filter_id/?include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum%2Creply_count&filter_id=%E6%91%84%E5%BD%B1_%E4%BA%BA%E5%83%8F&start={}&_={}'.format(start*24,int(time.time()*1000))
    headers={
        'Referer':'https://www.duitang.com/category/?cat=photography&sub=%E6%91%84%E5%BD%B1_%E4%BA%BA%E5%83%8F',
        'User-Agent':PC.random()
    }
    # proxies={
    #     'https':'220.173.106.168:63000',
    #     'https':'218.2.226.42:80',
    #     'htpps':'221.178.232.130:8080'
    # }
    response=requests.get(url,headers=headers).json()['data']['object_list']
    print('开始下载第%d批'%(start+1))
    for i,j in zip(response,range(24*start+1,24*(start+1)+1)):
        urlretrieve(i['photo']['path'],'./image/%d.jpg'%j)

if __name__ == '__main__':
    for i in range(2):
        link(i)