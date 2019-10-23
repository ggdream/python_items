#!/uesr/bin/python3.7.4
#coding=utf-8
#Author:清梦XXC
"""
1、获取citycode的接口：https://flights.ctrip.com/international/search/api/poi/search?key=
2、获取表单数据的接口：https://flights.ctrip.com/international/search/oneway-%s-%s?depdate=%s&cabin=y_s&adult=1&child=0&infant=0
3、获取机票数据的api：https://flights.ctrip.com/international/search/api/search/batchSearch?v=
注意：国外机票和国内机票使用的不是同一个api接口

JS源码里参数sign的加密过程：
{
            key: "genAntiCrawlerHeader",
            value: function(e) {
                var t = "";
                return e.get("flightSegments").valueSeq().forEach(function(e) {
                    var n = e.get("departureCityCode"),
                    r = e.get("arrivalCityCode"),
                    i = e.get("departureDate");
                    t += n + r + i
                }),
                {
                    sign: (new b.a).update(e.get("transactionID") + t).digest("hex")
                }
            }
        }
"""
import requests,json,re,time,hashlib
from urllib.request import quote
from prettytable import PrettyTable

F={'1':[],'2':[],'3':[],'4':[],'5':[]}
citydata={'Code':[],'CityId':[],'CountryId':[],'ProvinceId':[],'CityName':[],'CountryName':[],'TimeZone':[]}

def link_data(date,dcity,acity):
    date = '-'.join((date[0:4], date[4:6], date[6:8]))
    for i in [dcity,acity]:
        response=json.loads(requests.get('https://flights.ctrip.com/international/search/api/poi/search?key=%s'%quote(i)).content.decode('utf-8'))['Data'][0]
        citydata['Code'].append(response['Code'])
    url='https://flights.ctrip.com/international/search/oneway-%s-%s?depdate=%s&cabin=y_s&adult=1&child=0&infant=0'%(citydata['Code'][0],citydata['Code'][1],date)
    headers={
        'Referer':'https://flights.ctrip.com/international/search/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }
    datas=json.loads(re.findall('[GlobalSearchCriteria =](.*)[;]',requests.get(url,headers=headers).content.decode('utf-8'))[2].split('=')[-1])
    citydata['CityId']=[datas['flightSegments'][0]['departureCityId'],datas['flightSegments'][0]['arrivalCityId']]
    citydata['CountryId']=[datas['flightSegments'][0]['departureCountryId'],datas['flightSegments'][0]['arrivalCountryId']]
    citydata['ProvinceId']=[datas['flightSegments'][0]['departureProvinceId'],datas['flightSegments'][0]['arrivalProvinceId']]
    citydata['CityName']=[datas['flightSegments'][0]['departureCityName'],datas['flightSegments'][0]['arrivalCityName']]
    citydata['CountryName']=[datas['flightSegments'][0]['departureCountryName'],datas['flightSegments'][0]['arrivalCountryName']]
    citydata['TimeZone']=[datas['flightSegments'][0]['departureCityTimeZone'],datas['flightSegments'][0]['arrivalCityTimeZone']]
    citydata['timeZone']=datas['flightSegments'][0]['timeZone']
    citydata['transactionID']=datas['transactionID']
#以下是请求包含航班信息的部分
    url0='https://flights.ctrip.com/international/search/api/search/batchSearch?v='
    headers={
        'Referer':'https://flights.ctrip.com/international/search/oneway-%s-%s?depdate=%s&cabin=y_s&adult=1&child=0&infant=0&directflight='%(citydata['Code'][0],citydata['Code'][1],date),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Content-Type':'application/json;charset=utf-8',
        'sign':hashlib.md5(bytes(citydata['transactionID']+citydata['Code'][0]+citydata['Code'][1]+date,encoding='utf-8')).hexdigest(),
        'transactionid':citydata['transactionID']
    }
    data={"flightWayEnum":"OW","arrivalProvinceId":citydata['ProvinceId'][1],
          "extGlobalSwitches":{"useAllRecommendSwitch":'false'},"arrivalCountryName":citydata['CountryName'][1],
          "infantCount":0,"cabin":"Y_S","cabinEnum":"Y_S","departCountryName":citydata['CountryName'][0],
          "flightSegments":[{"departureDate":date,"arrivalProvinceId":citydata['ProvinceId'][1],
                             "arrivalCountryName":citydata['CountryName'][1],"departureCityName":citydata['CityName'][0],
                             "departureCityCode":citydata['Code'][0],"departureCountryName":citydata['CountryName'][0],
                             "arrivalCityName":citydata['CityName'][1],"arrivalCityCode":citydata['Code'][1],
                             "departureCityTimeZone":citydata['TimeZone'][0],"arrivalCountryId":citydata['CountryId'][1],
                             "timeZone":citydata['timeZone'],"departureCityId":citydata['CityId'][0],"departureCountryId":citydata['CountryId'][0],
                             "arrivalCityTimeZone":citydata['TimeZone'][1],"departureProvinceId":citydata['ProvinceId'][0],"arrivalCityId":citydata['CityId'][1]}],
          "childCount":0,"segmentNo":1,"adultCount":1,"extensionAttributes":{"isFlightIntlNewUser":'false'},"transactionID":citydata['transactionID'],
          "directFlight":'false',"departureCityId":citydata['CityId'][0],"isMultiplePassengerType":0,"flightWay":"S","arrivalCityId":citydata['CityId'][1],"departProvinceId":citydata['ProvinceId'][0]}
    return json.loads(requests.post(url0,data=json.dumps(data),headers=headers).content.decode('utf-8'))['data']['flightItineraryList']
def fdata(flight):
    f=flight['flightSegments'][0]['flightList']
    day=flight['flightSegments'][0]['crossDays']
    t=divmod(flight['flightSegments'][0]['duration'],60)
    if len(f)==1:
        f=f[0]
        if 'departureTerminal' not in f:
            f['departureTerminal'] = ''
        if 'arrivalTerminal' not in f:
            f['arrivalTerminal'] = ''
        F['1'].append([f['flightNo'],f['marketAirlineName'],f['departureDateTime'].split()[-1]+'（'+f['departureAirportName']+f['departureTerminal']+
                       '|'+f['departureCountryName']+'·'+f['departureCityName']+'）'+'--->'+f['arrivalDateTime'].split()[-1]+'（'+f['arrivalAirportName']+f['arrivalTerminal']+
                       '|'+f['arrivalCountryName']+'·'+f['arrivalCityName']+'）'+'·%d'%day,'%d时%d分'%(t),'￥%d'%(flight['priceList'][0]['adultPrice']+flight['priceList'][0]['adultTax'])])

    elif len(f)==2:
        for i in range(2):
            if 'departureTerminal' not in f[i]:
                f[i]['departureTerminal'] = ''
            if 'arrivalTerminal' not in f[i]:
                f[i]['arrivalTerminal'] = ''
        F['2'].append([f[0]['flightNo']+'（'+f[0]['marketAirlineName']+'）'+'-->'+f[1]['flightNo']+'（'+f[1]['marketAirlineName']+'）',
                       f[0]['departureDateTime'].split()[-1] + '（' + f[0]['departureAirportName'] + f[0]['departureTerminal'] +'|' + f[0]['departureCountryName'] + '·' + f[0]['departureCityName'] + '）' + '--->' +
                       f[0]['arrivalDateTime'].split()[-1] + '（' + f[0]['arrivalAirportName'] + f[0]['arrivalTerminal'] +'|' + f[0]['arrivalCountryName'] + '·' + f[0]['arrivalCityName'] + '）',
                       '%d时%d分'%(divmod(f[0]['transferDuration'],60)),
                       f[1]['departureDateTime'].split()[-1] + '（' + f[1]['departureAirportName'] + f[1]['departureTerminal'] + '|' + f[1]['departureCountryName'] + '·' + f[1]['departureCityName'] + '）' + '--->' +
                       f[1]['arrivalDateTime'].split()[-1] + '（' + f[1]['arrivalAirportName'] + f[1]['arrivalTerminal'] + '|' + f[1]['arrivalCountryName'] + '·' + f[1]['arrivalCityName'] + '）',
                       '%d时%d分'%(t)+'|%d'%day,'￥%d'%(flight['priceList'][0]['adultPrice']+flight['priceList'][0]['adultTax'])])
    elif len(f)==3:
        for i in range(3):
            if 'departureTerminal' not in f[i]:
                f[i]['departureTerminal'] = ''
            if 'arrivalTerminal' not in f[i]:
                f[i]['arrivalTerminal'] = ''
        F['3'].append([f[0]['flightNo']+'（'+f[0]['marketAirlineName']+'）'+'-->'+f[1]['flightNo']+'（'+f[1]['marketAirlineName']+'）'+'-->'+f[2]['flightNo']+'（'+f[2]['marketAirlineName']+'）',
                       f[0]['departureDateTime'].split()[-1] + '（' + f[0]['departureAirportName'] + f[0]['departureTerminal'] + '|' + f[0]['departureCountryName'] + '·' + f[0]['departureCityName'] + '）' + '--->' +
                       f[0]['arrivalDateTime'].split()[-1] + '（' + f[0]['arrivalAirportName'] + f[0]['arrivalTerminal'] + '|' + f[0]['arrivalCountryName'] + '·' + f[0]['arrivalCityName'] + '）',
                       '%d时%d分' % (divmod(f[0]['transferDuration'], 60)),
                       f[1]['departureDateTime'].split()[-1] + '（' + f[1]['departureAirportName'] + f[1]['departureTerminal'] + '|' + f[1]['departureCountryName'] + '·' + f[1]['departureCityName'] + '）' + '--->' +
                       f[1]['arrivalDateTime'].split()[-1] + '（' + f[1]['arrivalAirportName'] + f[1]['arrivalTerminal'] + '|' + f[1]['arrivalCountryName'] + '·' + f[1]['arrivalCityName'] + '）',
                       '%d时%d分' % (divmod(f[1]['transferDuration'], 60)),
                       f[2]['departureDateTime'].split()[-1] + '（' + f[2]['departureAirportName'] + f[2]['departureTerminal'] + '|' + f[2]['departureCountryName'] + '·' + f[2]['departureCityName'] + '）' + '--->' +
                       f[2]['arrivalDateTime'].split()[-1] + '（' + f[2]['arrivalAirportName'] + f[2]['arrivalTerminal'] + '|' + f[2]['arrivalCountryName'] + '·' + f[2]['arrivalCityName'] + '）',
                       '%d时%d分' % (t) + '|%d' % day,'￥%d'%(flight['priceList'][0]['adultPrice']+flight['priceList'][0]['adultTax'])])
    elif len(f)==4:
        for i in range(4):
            if 'departureTerminal' not in f[i]:
                f[i]['departureTerminal'] = ''
            if 'arrivalTerminal' not in f[i]:
                f[i]['arrivalTerminal'] = ''
        F['4'].append([f[0]['flightNo']+'（'+f[0]['marketAirlineName']+'）'+'-->'+f[1]['flightNo']+'（'+f[1]['marketAirlineName']+'）'+'-->'+f[2]['flightNo']+'（'+f[2]['marketAirlineName']+'）'+'-->'+f[3]['flightNo']+'（'+f[3]['marketAirlineName']+'）',
                       f[0]['departureDateTime'].split()[-1] + '（' + f[0]['departureAirportName'] + f[0]['departureTerminal'] + '|' + f[0]['departureCountryName'] + '·' + f[0]['departureCityName'] + '）' + '--->' +
                       f[0]['arrivalDateTime'].split()[-1] + '（' + f[0]['arrivalAirportName'] + f[0]['arrivalTerminal'] + '|' + f[0]['arrivalCountryName'] + '·' + f[0]['arrivalCityName'] + '）',
                       '%d时%d分' % (divmod(f[0]['transferDuration'], 60)),
                       f[1]['departureDateTime'].split()[-1] + '（' + f[1]['departureAirportName'] + f[1]['departureTerminal'] + '|' + f[1]['departureCountryName'] + '·' + f[1]['departureCityName'] + '）' + '--->' +
                       f[1]['arrivalDateTime'].split()[-1] + '（' + f[1]['arrivalAirportName'] + f[1]['arrivalTerminal'] + '|' + f[1]['arrivalCountryName'] + '·' + f[1]['arrivalCityName'] + '）',
                       '%d时%d分' % (divmod(f[1]['transferDuration'], 60)),
                       f[2]['departureDateTime'].split()[-1] + '（' + f[2]['departureAirportName'] + f[2]['departureTerminal'] + '|' + f[2]['departureCountryName'] + '·' + f[2]['departureCityName'] + '）' + '--->' +
                       f[2]['arrivalDateTime'].split()[-1] + '（' + f[2]['arrivalAirportName'] + f[2]['arrivalTerminal'] + '|' + f[2]['arrivalCountryName'] + '·' + f[2]['arrivalCityName'] + '）',
                       '%d时%d分' % (divmod(f[2]['transferDuration'], 60)),
                       f[3]['departureDateTime'].split()[-1] + '（' + f[3]['departureAirportName'] + f[3]['departureTerminal'] + '|' + f[3]['departureCountryName'] + '·' + f[3]['departureCityName'] + '）' + '--->' +
                       f[3]['arrivalDateTime'].split()[-1] + '（' + f[3]['arrivalAirportName'] + f[3]['arrivalTerminal'] + '|' + f[3]['arrivalCountryName'] + '·' + f[3]['arrivalCityName'] + '）',
                       '%d时%d分' % (t) + '|%d' % day,'￥%d' % (flight['priceList'][0]['adultPrice'] + flight['priceList'][0]['adultTax'])])
    else:
        F['5'].append(['%d'%len(f),flight['itineraryId'],'%d时%d分' % (t) + '|%d' % day,'￥%d'%(flight['priceList'][0]['adultPrice']+flight['priceList'][0]['adultTax'])])
def start(date,dcity,acity):
    # for i in map(fdata,link_data(date,dcity,acity)):
    #     pass
    for flight in link_data(date,dcity,acity):
        fdata(flight)
    print('='*250+'\n'+'='*250+'\n'+dcity+'--->'+acity+'|'+date+'\n'+'='*250)
    table1=PrettyTable(['航空公司','航班号','航程详明','总用时','最低价格'])
    table2=PrettyTable(['航班信息','航班详明-1','间隔时长','航班详明-2','总用时','最低总价格'])
    table3=PrettyTable(['航班信息','航班详明-1','间隔时长Ⅰ','航班详明-2','间隔时长Ⅱ','航班详明-3','总用时','最低总价格'])
    table4=PrettyTable(['航班信息','航班详明-1','间隔时长Ⅰ','航班详明-2','间隔时长Ⅱ','航班详明-3','间隔时长Ⅲ','航班详明-4','总用时','最低总价格'])
    table5=PrettyTable(['乘坐次数','航班信息','总用时','总价格'])
    for i,j in zip(range(1,6),[table1,table2,table3,table4,table5]):
        if F[str(i)]!=[]:
            print('='*250)
            print('———换乘次数：%d'%(i-1))
            for k in F[str(i)]:
                j.add_row(k)
            print(j)
    print('='*250+'\n'+'————全部航班已示出！！！')

if __name__ == '__main__':
    ddate = input('输入时间：')
    dcity = input('输入起点：')
    acity = input('输入终点：')
    start(ddate,dcity,acity)



