#!/uesr/bin/python3.7.4
#coding=utf-8
#Auther:清梦XXC
#@Time:2019/10/29 11:48
'''
useragentxxc是自制的python第三方库，用于生成随机的user-agent。

目前只有PC端浏览器user-agent，在后期会加入移动端user-agent。（已经收集好了，但是没时间来及处理）

已经上传到了pypi和github。大家可以在cmd里输入“pip install useragentxxc”即可安装

'''
import requests,useragentxxc,os
from lxml import etree
from PIL import Image
from 你们不能看到的密码 import name,pwd
from urllib.parse import urlencode
from urllib.request import urlretrieve
s=requests.Session()
ua=useragentxxc.PersonComputer.random()
url='http://www.boohee.com/profile/login'
headers={
    'Referer':'http://www.boohee.com/profile/login',
    'User-Agent':ua,
    'Content-Type':'application/x-www-form-urlencoded'
}
data={
    'utf8':'✓',
    'pre_url':'',
    'login_type':'auto',
    'user_name':name(),
    'passwd':pwd()
}
response=etree.HTML(s.post(url,data=urlencode(data),headers=headers).content.decode('utf-8')).xpath('//*[@id="simple_captcha"]/div/div/img/@src')
if response!=[]:
    urlretrieve('http://www.boohee.com'+response[0],'captcha.png')
    img=Image.open('captcha.png')
    img.show()
    captcha=input('输入验证码：')
    data['captcha']=captcha
    os.remove('captcha.png')
    s.post(url, data=urlencode(data), headers=headers)

url1='http://www.boohee.com/profile/index'
hv={
    'Referer':'http://www.boohee.com/solution/index',
    'User-Agent':ua
}
res=etree.HTML(s.get(url1,headers=hv).content.decode('utf-8')).xpath('.//table[1]/tr[6]/td[2]/text()')[0]
print(res)