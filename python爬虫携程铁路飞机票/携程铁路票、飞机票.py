import requests,json,sys,time,datetime,random,re
from lxml import etree
from urllib import request
from xpinyin import Pinyin
from prettytable import PrettyTable
from urllib.request import quote as qu
from getPrice import price
#铁路直达方案
def oneWay(DepartureDate,DepartureDateReturn):
    global n1,n2,origin,destination,q1,q2
    while 1:
        n1 = input('请输入始发城市：')
        n2 = input('请输入抵达城市：')
        p = Pinyin()
        origin = p.get_pinyin(n1, '')
        destination = p.get_pinyin(n2, '')
        q1 = request.quote(n1, encoding='gb2312')
        q2 = request.quote(n2, encoding='gb2312')
        trainData=[]
        falseBook=[]
        url='https://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList'
        headers={
            'Referer':'https://trains.ctrip.com/TrainBooking/Search.aspx?from={}&to={}&day=1&fromCn={}&toCn={}'.format(origin,destination,q1,q2),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        aa={"IsBus":'false',"Filter":"0","Catalog":"","IsGaoTie":'false',"IsDongChe":'false',"CatalogName":"","DepartureCity":origin,"ArrivalCity":destination,"HubCity":"","DepartureCityName":n1,"ArrivalCityName":n2,"DepartureDate":DepartureDate,"DepartureDateReturn":DepartureDateReturn,"ArrivalDate":"","TrainNumber":""}
        data={
            'value':json.dumps(aa)
        }
        try:
            respones=requests.post(url=url,headers=headers,data=data).content.decode('gb2312')
            trainDataDict = json.loads(respones, encoding='gb2312')['TrainItemsList']
            break
        except json.decoder.JSONDecodeError:
            print('地点输入有误，请重新输入\n')
        except Exception:
            print('网络错误，请检查网络连接后重试，3秒后将退出程序')
            time.sleep(3)
            sys.exit(-1)
    print('=' * 300 + '\n', n1, '--->', n2, '|', DepartureDate, '\n' + '=' * 300)
    for train in trainDataDict:
        if train['SaleReminder']!='':
            falseBook.append([train['TrainName'],train['SaleReminder']])
        else:
            if len(train['SeatBookingItem'])==3:
                trainData.append({train['TrainName']:[train['StartStationName'],train['EndStationName'],train['StratTime'],train['EndTime'],train['TakeTime'],train['TakeDays'],'余{}张'.format(str(train['SeatBookingItem'][0]['Inventory']))+'--¥'+train['SeatBookingItem'][0]['Price'],'余{}张'.format(str(train['SeatBookingItem'][1]['Inventory']))+'--¥'+train['SeatBookingItem'][1]['Price'],'余{}张'.format(str(train['SeatBookingItem'][2]['Inventory']))+'--¥'+train['SeatBookingItem'][2]['Price']]})
            elif len(train['SeatBookingItem'])==1:
                trainData.append({train['TrainName']: [train['StartStationName'], train['EndStationName'],
                                                       train['StratTime'], train['EndTime'], train['TakeTime'],
                                                       train['TakeDays'], '余{}张'.format(
                        str(train['SeatBookingItem'][0]['Inventory'])) + '--¥' + train['SeatBookingItem'][0]['Price'],
                                                      '余0张','余0张']})
            elif len(train['SeatBookingItem'])==2:
                trainData.append({train['TrainName']: [train['StartStationName'], train['EndStationName'],
                                                       train['StratTime'], train['EndTime'], train['TakeTime'],
                                                       train['TakeDays'], '余{}张'.format(
                        str(train['SeatBookingItem'][0]['Inventory'])) + '--¥' + train['SeatBookingItem'][0]['Price'],
                                                       '余{}张'.format(
                                                           str(train['SeatBookingItem'][1]['Inventory'])) + '--¥' +
                                                       train['SeatBookingItem'][1]['Price'], '余0张']})

            else:
                if train['SeatBookingItem'][0]['Inventory']==0:
                    trainData.append({train['TrainName']: [train['StartStationName'], train['EndStationName'],
                                                           train['StratTime'], train['EndTime'], train['TakeTime'],
                                                           train['TakeDays'], '余{}张'.format(
                            str(train['SeatBookingItem'][3]['Inventory'])) + '（无座）--¥' + train['SeatBookingItem'][3]['Price'],
                                                           '余{}张'.format(
                                                               str(train['SeatBookingItem'][1]['Inventory'])) + '--¥' +
                                                           train['SeatBookingItem'][1]['Price'], '余{}张'.format(
                            str(train['SeatBookingItem'][2]['Inventory'])) + '--¥' + train['SeatBookingItem'][2]['Price']]})
                else:
                    trainData.append({train['TrainName']: [train['StartStationName'], train['EndStationName'],
                                                           train['StratTime'], train['EndTime'], train['TakeTime'],
                                                           train['TakeDays'], '余{}张'.format(
                            str(train['SeatBookingItem'][0]['Inventory'])) + '--¥' + train['SeatBookingItem'][0][
                                                               'Price'],
                                                           '余{}张'.format(
                                                               str(train['SeatBookingItem'][1]['Inventory'])) + '--¥' +
                                                           train['SeatBookingItem'][1]['Price'], '余{}张'.format(
                            str(train['SeatBookingItem'][2]['Inventory'])) + '--¥' + train['SeatBookingItem'][2]['Price']]})
    # print(trainData)
    for i in trainData:
        for key in i:
            if i[key][-3][0:3]!='余0张':
                if i[key][-2][0:3] == '余0张':
                    i[key][-2]='-'*13
                if i[key][-1][0:3] == '余0张':
                    i[key][-1]='-'*13
                i[key].append('¥'+i[key][-3].split('¥')[1])
            elif i[key][-2][0:3]!='余0张':
                i[key][-3] = '-' * 13
                if i[key][-1][0:3] == '余0张':
                    i[key][-1]='-'*13
                i[key].append('¥'+i[key][-2].split('¥')[1])
            elif i[key][-1][0:3]!='余0张':
                i[key][-3] = '-' * 13
                i[key][-2] = '-' * 13
                i[key].append('¥'+i[key][-1].split('¥')[1])
            else:
                i[key][-3] = '-' * 13
                i[key][-2] = '-' * 13
                i[key][-1] = '-' * 13
                i[key].append('-'*13)
    # print(trainData)
    """
        如果只看有票
        """
    if trainData!=[]:
        print('=' * 300 + '\n——铁路直达方案：')
        table0 = PrettyTable(['车次', '始发站', '终点站', '发车时间', '停靠时间', '行程总时长', '天数', '二等座（硬座）', '一等座（硬卧）', '商务座（软卧）','最低价格'])
        for i in trainData:
            for key in i:
                i[key].insert(0, key)
                table0.add_row(i[key])
        print(table0)
        #筛选算法
        # trainData = oneWay_priceOrder(trainData)
        # table = PrettyTable(['车次', '始发站', '终点站', '发车时间', '停靠时间', '行程总时长', '天数', '二等座（硬座）', '一等座（硬卧）', '商务座（软卧）', '最低价格'])
        # for i in trainData:
        #     for key in i:
        #         table.add_row(i[key])
        # print(table)
    if falseBook!=[]:
        print('\n' + '=' * 300 + '\n——预售车次：')
        tablebook = PrettyTable(['车次', '开售时间'])
        for i in falseBook:
            tablebook.add_row(i)
        print(tablebook)
#铁路换乘方案
def Multiple(DepartureDate,DepartureDateReturn):
    global n1,n2,origin,destination,q1,q2
    agent = [
        # win7操作系统
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        # win10操作系统
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5680.400 QQBrowser/10.2.1852.400',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Core/1.63.5680.400 QQBrowser/10.2.1852.400; rv:11.0) like Gecko'
    ]
    trainData = []
    trainUrl=[]
    url='https://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getTransferList'
    headers={
        'Referer': 'https://trains.ctrip.com/TrainBooking/Search.aspx?from={}&to={}&day={}&fromCn={}&toCn={}'.format(origin,destination,DepartureDate,q1,q2),
        'User-Agent': '{}'.format(random.choice(agent))
    }
    aa={"departure":"","arrive":"","date":""}
    aa['departure']=n1
    aa['arrive']=n2
    aa['date']=DepartureDate
    data={
        'value':json.dumps(aa)
    }
    response=requests.post(url=url,headers=headers,data=data).content.decode('gb2312')
    trainDataList=json.loads(response, encoding='gb2312')
    for train in trainDataList:
        # if len(train['TrainTransferInfos']) == 2:
        d1=datetime.datetime(int(train['TrainTransferInfos'][0]['DepartDate'].split('-')[0]),int(train['TrainTransferInfos'][0]['DepartDate'].split('-')[1]),int(train['TrainTransferInfos'][0]['DepartDate'].split('-')[2]))
        d2=datetime.datetime(int(train['TrainTransferInfos'][1]['ArriveDate'].split('-')[0]),int(train['TrainTransferInfos'][1]['ArriveDate'].split('-')[1]),int(train['TrainTransferInfos'][1]['ArriveDate'].split('-')[2]))
        d12=d2-d1
        trainData.append([train['DepartStation']+'--->'+train['ArriveStation'],train['TransferStation'],
                          train['TrainTransferInfos'][0]['TrainNumber']+'（'+train['TrainTransferInfos'][0]['DepartTime']+'-'+train['TrainTransferInfos'][0]['ArriveTime']+'|+'+str(train['TrainTransferInfos'][0]['TakeDays'])+'）'+'--->'+
                          train['TrainTransferInfos'][1]['TrainNumber'] + '（' + train['TrainTransferInfos'][1]['DepartTime'] + '-' + train['TrainTransferInfos'][1]['ArriveTime']+'|+'+str(train['TrainTransferInfos'][1]['TakeDays']) + '）',
                          train['TotalRuntime'],str(d12.days)
                          ])
        trainUrl.append([train['TrainTransferInfos'][0]['TrainNumber'],train['TrainTransferInfos'][0]['DepartStation'],train['TrainTransferInfos'][0]['ArriveStation'],train['TrainTransferInfos'][0]['DepartDate'],
                         train['TrainTransferInfos'][1]['TrainNumber'],train['TrainTransferInfos'][1]['DepartStation'],train['TrainTransferInfos'][1]['ArriveStation'],train['TrainTransferInfos'][1]['DepartDate']
                         ])
    Data=price(origin, destination, DepartureDate, q1, q2,trainUrl, trainData)
    if Data!=[]:
        print('\n' + '=' * 300 + '\n——铁路换乘方案：')
        table=PrettyTable(['车次换乘情况','中转站','换乘详明','总时长','跨天数','前·二等座（硬座）','前·一等座（硬卧）','前·商务座（软卧）','后·二等座（硬座）','后·一等座（硬卧）','后·商务座（软卧）'])
        for i in Data:
            table.add_row(i)
        print(table)
#飞机直达+换乘方案
def air(DepartureDate):
    global n1,n2
    url = 'https://flights.ctrip.com/itinerary/api/12808/products'
    dCity =n1
    aCity =n2
    date=DepartureDate
    citydata = {'code': [], 'cityid': []}
    for i in [qu(g) for g in [dCity, aCity]]:
        Url = 'https://flights.ctrip.com/itinerary/api/13076/getpoicontent?key={}'.format(i)
        Data = json.loads(requests.get(url=Url).content.decode('utf-8'))['data']['Data'][0]
        citydata['code'].append(Data['Code'])
        citydata['cityid'].append(Data['CityId'])
    url = 'https://flights.ctrip.com/itinerary/api/12808/products'
    headers = {
        'Referer': 'https://flights.ctrip.com/itinerary/oneway/{}-{}?date={}'.format(citydata['code'][0],
                                                                                     citydata['code'][1], date),
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    data = {"flightWay": "Oneway", "classType": "ALL", "hasChild": 'false', "hasBaby": 'false',
            "searchIndex": 1, "airportParams": [
            {"dcity": citydata['code'][0], "acity": citydata['code'][1], "dcityname": dCity, "acityname": aCity,
             "date": date, "dcityid": citydata['cityid'][0], "acityid": citydata['cityid'][1]}]}
    response = requests.post(url=url, headers=headers, data=json.dumps(data)).content.decode('utf-8')
    response = json.loads(response)['data']['routeList']
    Route_f, Route_tf, Route_ft, Route_ff = [], [], [], 0
    if type(response)==list:
        for route in response:
            if route['routeType'] == 'Flight':
                end = route['legs'][0]['flight']['arrivalDate'].split()[0].split('-')
                End = route['legs'][0]['flight']['arrivalDate'].split()[-1].split(':')
                start = route['legs'][0]['flight']['departureDate'].split()[0].split('-')
                Start = route['legs'][0]['flight']['departureDate'].split()[-1].split(':')
                a = datetime.datetime(int(end[0]), int(end[1]), int(end[2]), int(End[0]), int(End[1]))
                b = datetime.datetime(int(start[0]), int(start[1]), int(start[2]), int(Start[0]), int(Start[1]))
                if type(route['legs'][0]['flight']['craftTypeName'])==str:
                    Route_f.append([route['legs'][0]['flight']['airlineName'], route['legs'][0]['flight']['flightNumber'],
                                    route['legs'][0]['flight']['craftTypeName'] + '·' + route['legs'][0]['flight']['craftTypeKindDisplayName'],
                                    route['legs'][0]['flight']['departureDate'].split()[-1] + '（' +
                                    route['legs'][0]['flight']['departureAirportInfo']['airportName'] +
                                    route['legs'][0]['flight']['departureAirportInfo']['terminal']['name'] + '）' +
                                    '--->' + route['legs'][0]['flight']['arrivalDate'].split()[-1] + '（' +
                                    route['legs'][0]['flight']['arrivalAirportInfo']['airportName'] +
                                    route['legs'][0]['flight']['arrivalAirportInfo']['terminal']['name'] + '）' +
                                    '·+{}'.format((a - b).days),
                                    '{}时{}分钟'.format(int(int((a - b).seconds) / 60 // 60), int(int((a - b).seconds) / 60 % 60)),
                                    route['legs'][0]['characteristic']['lowestPrice']])
                else:
                    Route_f.append(
                        [route['legs'][0]['flight']['airlineName'], route['legs'][0]['flight']['flightNumber'],
                         '-'*20,
                         route['legs'][0]['flight']['departureDate'].split()[-1] + '（' +
                         route['legs'][0]['flight']['departureAirportInfo']['airportName'] +
                         route['legs'][0]['flight']['departureAirportInfo']['terminal']['name'] + '）' +
                         '--->' + route['legs'][0]['flight']['arrivalDate'].split()[-1] + '（' +
                         route['legs'][0]['flight']['arrivalAirportInfo']['airportName'] +
                         route['legs'][0]['flight']['arrivalAirportInfo']['terminal']['name'] + '）' +
                         '·+{}'.format((a - b).days),
                         '{}时{}分钟'.format(int(int((a - b).seconds) / 60 // 60), int(int((a - b).seconds) / 60 % 60)),
                         route['legs'][0]['characteristic']['lowestPrice']])
            elif route['routeType'] == 'Transit':
                Route_ff+=1
            elif route['routeType'] == 'FlightTrain':
                if route['legs'][0]['legType'] == 'Train':
                    end3 = route['legs'][1]['flight']['arrivalDate'].split()[0].split('-')
                    End1 = route['legs'][1]['flight']['arrivalDate'].split()[-1].split(':')
                    start3 = route['legs'][1]['flight']['departureDate'].split()[0].split('-')
                    End3 = route['legs'][1]['flight']['departureDate'].split()[-1].split(':')
                    end4 = route['legs'][0]['toTime'].split()[0].split('-')
                    Start3 = route['legs'][0]['toTime'].split()[-1].split(':')
                    start4 = route['legs'][0]['fromTime'].split()[0].split('-')
                    Start1 = route['legs'][0]['fromTime'].split()[-1].split(':')
                    a3 = datetime.datetime(int(end3[0]), int(end3[1]), int(end3[2]), int(End1[0]), int(End1[1]))
                    b3 = datetime.datetime(int(start3[0]), int(start3[1]), int(start3[2]), int(End3[0]), int(End3[1]))
                    a4 = datetime.datetime(int(end4[0]), int(end4[1]), int(end4[2]), int(Start3[0]), int(Start3[1]))
                    b4 = datetime.datetime(int(start4[0]), int(start4[1]), int(start4[2]), int(Start1[0]), int(Start1[1]))
                    Route_tf.append([route['legs'][0]['trainNumber'] + '-->' + route['legs'][1]['flight'][
                        'flightNumber'] + '（{}）'.format(route['legs'][1]['flight']['airlineName']),
                                     route['legs'][0]['fromTime'].split()[-1] + '（{}）'.format(
                                         route['legs'][0]['fromStation']['name']) + '-->' +
                                     route['legs'][0]['toTime'].split()[-1] + '（{}）'.format(
                                         route['legs'][0]['toStation']['name']) + '·+{}'.format((a4 - b4).days),
                                     '{}时{}分钟'.format(int(int((b3 - a4).seconds) / 60 // 60),
                                                      int(int((b3 - a4).seconds) / 60 % 60)),
                                     '<{}>'.format(route['legs'][1]['flight']['departureDate'].split()[0].split('-')[-1]) +
                                     route['legs'][1]['flight']['departureDate'].split()[-1] + '（{}）'.format(
                                         route['legs'][1]['flight']['departureAirportInfo']['airportName'] +
                                         route['legs'][1]['flight']['departureAirportInfo']['terminal']['name']) + '-->' +
                                     route['legs'][1]['flight']['arrivalDate'].split()[-1] + '（{}）'.format(
                                         route['legs'][1]['flight']['arrivalAirportInfo']['airportName'] +
                                         route['legs'][1]['flight']['arrivalAirportInfo']['terminal'][
                                             'name']) + '·+{}'.format((a3 - b3).days),
                                     '{}时{}分钟'.format(int(int((a3 - b4).seconds) / 60 // 60),
                                                      int(int((a3 - b4).seconds) / 60 % 60)), route['transitPrice']
                                     ])
                elif route['legs'][0]['legType'] == 'Flight':
                    end1 = route['legs'][1]['toTime'].split()[0].split('-')
                    End2 = route['legs'][1]['toTime'].split()[-1].split(':')
                    start1 = route['legs'][1]['fromTime'].split()[0].split('-')
                    End4 = route['legs'][1]['fromTime'].split()[-1].split(':')
                    end2 = route['legs'][0]['flight']['arrivalDate'].split()[0].split('-')
                    Start4 = route['legs'][0]['flight']['arrivalDate'].split()[-1].split(':')
                    start2 = route['legs'][0]['flight']['departureDate'].split()[0].split('-')
                    Start2 = route['legs'][0]['flight']['departureDate'].split()[-1].split(':')
                    a1 = datetime.datetime(int(end1[0]), int(end1[1]), int(end1[2]), int(End2[0]), int(End2[1]))
                    b1 = datetime.datetime(int(start1[0]), int(start1[1]), int(start1[2]), int(End4[0]), int(End4[1]))
                    a2 = datetime.datetime(int(end2[0]), int(end2[1]), int(end2[2]), int(Start4[0]), int(Start4[1]))
                    b2 = datetime.datetime(int(start2[0]), int(start2[1]), int(start2[2]), int(Start2[0]), int(Start2[1]))
                    Route_ft.append([route['legs'][0]['flight']['flightNumber'] + '（{}）'.format(
                        route['legs'][0]['flight']['airlineName']) + '-->' + route['legs'][1]['trainNumber'],
                                     route['legs'][0]['flight']['departureDate'].split()[-1] + '（{}）'.format(
                                         route['legs'][0]['flight']['departureAirportInfo']['airportName'] +
                                         route['legs'][0]['flight']['departureAirportInfo']['terminal']['name']) + '-->' +
                                     route['legs'][0]['flight']['arrivalDate'].split()[-1] + '（{}）'.format(
                                         route['legs'][0]['flight']['arrivalAirportInfo']['airportName'] +
                                         route['legs'][0]['flight']['arrivalAirportInfo']['terminal'][
                                             'name']) + '·+{}'.format((a2 - b2).days),
                                     '{}时{}分钟'.format(int(int((b1 - a2).seconds) / 60 // 60),
                                                      int(int((b1 - a2).seconds) / 60 % 60)),
                                     '<{}> '.format(route['legs'][1]['fromTime'].split()[0].split('-')[-1]) +
                                     route['legs'][1]['fromTime'].split()[-1] + '（{}）'.format(
                                         route['legs'][1]['fromStation']['name']) + '-->' +
                                     route['legs'][1]['toTime'].split()[
                                         -1] + '（{}）'.format(route['legs'][1]['toStation']['name']) + '·+{}'.format(
                                         (a1 - b1).days),
                                     '{}时{}分钟'.format(int(int((a1 - b2).seconds) / 60 // 60),
                                                      int(int((a1 - b2).seconds) / 60 % 60)), route['transitPrice']
                                     ])
    if Route_f != []:
        print('\n' + '=' * 300 + '\n——航空直达方案：')
        table1 = PrettyTable(['航空公司', '航班班次', '客机机型', '发车时间地点-->停靠时间地点', '行程总时长', '最低价格'])
        for i in Route_f:
            table1.add_row(i)
        print(table1)
    if Route_tf != []:
        print('\n' + '=' * 300 + '\n——铁空换乘方案：')
        table2 = PrettyTable(['车次航班', '前半程（铁路）', '间隔时长', '后半程（航空）', '行程总时长', '最低总价格'])
        for j in Route_tf:
            table2.add_row(j)
        print(table2)
    if Route_ft != []:
        print('\n' + '=' * 300 + '\n——空铁换乘方案：')
        table3 = PrettyTable(['车次航班', '前半程（航空）', '间隔时长', '后半程（铁路）', '行程总时长', '最低总价格'])
        for k in Route_ft:
            table3.add_row(k)
        print(table3)
    if Route_ff!=0:
        print('共有%d种飞飞方案未列出'%Route_ff)


def start():
    while 1:
        try:
            DepartureDate = input('请输入出行日期：')
            DepartureDate = '-'.join((DepartureDate[0:4], DepartureDate[4:6], DepartureDate[6:8]))
            DepartureDateReturn = str(datetime.date(*map(int, DepartureDate.split('-'))) + datetime.timedelta(2))
            break
        except Exception:
            print('请输入正确的日期\n\n'+'='*300)
    oneWay(DepartureDate, DepartureDateReturn)
    Multiple(DepartureDate, DepartureDateReturn)
    air(DepartureDate)
    print('\n'+'='*300+'\n'+'='*300+'\n所有车次和航班已示出！\n'+'='*300)
if __name__ == '__main__':
    start()