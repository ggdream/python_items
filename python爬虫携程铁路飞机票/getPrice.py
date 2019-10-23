import random,json,requests,re
"""
获取需要换乘车次的票价
"""
def price(origin, destination, DepartureDate, q1, q2,trainUrl, trainData):
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
    Url = 'https://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getQueryBooking'
    hv = {
        'Referer': 'https://trains.ctrip.com/TrainBooking/HubSingleTrip.aspx?from={}&to={}&day={}&number=&jumpflag=2&fromCn={}&toCn={}'.format(
            origin, destination, DepartureDate, q1, q2),
        'User-Agent': ''.format(random.choice(agent))
    }
    for rr, ss in zip(trainUrl, trainData):
        data1Dict, data2Dict = {}, {}
        data1Dict['trainNum'] = rr[0]
        data1Dict['departure'] = rr[1]
        data1Dict['arrive'] = rr[2]
        data1Dict['date'] = rr[3]
        data2Dict['trainNum'] = rr[4]
        data2Dict['departure'] = rr[5]
        data2Dict['arrive'] = rr[6]
        data2Dict['date'] = rr[7]
        data1 = {'value': json.dumps(data1Dict)}
        data2 = {'value': json.dumps(data2Dict)}
        response1 =json.loads(requests.post(url=Url, headers=hv, data=data1).content.decode('gb2312'), encoding='gb2312')['TicketResult']['TicketItems']
        response2 =json.loads(requests.post(url=Url, headers=hv, data=data2).content.decode('gb2312'), encoding='gb2312')['TicketResult']['TicketItems']
        if len(response1) == 1:
            if response1[0]['Inventory'] != 0:
                ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
            else:
                ss.append('-' * 13)
            ss.append('-' * 13)
            ss.append('-' * 13)
            if len(response2) == 1:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                else:
                    ss.append('-' * 13)
                ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 2:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 3:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
            else:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    if response2[3]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[3]['Inventory'])) + '--¥' + str(response2[3]['Price']))
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
        elif len(response1) == 2:
            if response1[0]['Inventory'] != 0:
                ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                if response1[1]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                else:
                    ss.append('-' * 13)
            else:
                ss.append('-' * 13)
                if response1[1]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                else:
                    ss.append('-' * 13)
            ss.append('-' * 13)
            if len(response2) == 1:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                else:
                    ss.append('-' * 13)
                ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 2:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 3:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
            else:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    if response2[3]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[3]['Inventory'])) + '--¥' + str(response2[3]['Price']))
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
        elif len(response1) == 3:
            if response1[0]['Inventory'] != 0:
                ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                if response1[1]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                    if response1[2]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response1[2]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                    else:
                        ss.append('-' * 13)
            else:
                ss.append('-' * 13)
                if response1[1]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                    if response1[2]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response1[2]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                    else:
                        ss.append('-' * 13)
            if len(response2) == 1:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                else:
                    ss.append('-' * 13)
                ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 2:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 3:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
            else:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    if response2[3]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[3]['Inventory'])) + '--¥' + str(response2[3]['Price']))
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
        else:
            if len(response1) == 1:
                if response1[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                else:
                    ss.append('-' * 13)
                ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response1) == 2:
                if response1[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                    if response1[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response1[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                    else:
                        ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response1) == 3:
                if response1[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                    if response1[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                        if response1[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response1[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response1[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                        if response1[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response1[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                        else:
                            ss.append('-' * 13)
            else:
                if response1[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response1[0]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                    if response1[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                        if response1[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response1[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    if response1[3]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response1[3]['Inventory'])) + '--¥' + str(response1[3]['Price']))
                        if response1[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                            if response1[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[0]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response1[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                            else:
                                ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response1[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response1[1]['Inventory'])) + '--¥' + str(response1[1]['Price']))
                            if response1[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response1[2]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response1[2]['Inventory'] != 0:
                                ss.append('余{}张'.format(str(response1[2]['Inventory'])) + '--¥' + str(response[2]['Price']))
                            else:
                                ss.append('-' * 13)
            if len(response2) == 1:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                else:
                    ss.append('-' * 13)
                ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 2:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                    else:
                        ss.append('-' * 13)
                ss.append('-' * 13)
            elif len(response2) == 3:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    ss.append('-' * 13)
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
            else:
                if response2[0]['Inventory'] != 0:
                    ss.append('余{}张'.format(str(response2[0]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                    if response2[1]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[2]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                        else:
                            ss.append('-' * 13)
                else:
                    if response2[3]['Inventory'] != 0:
                        ss.append('余{}张'.format(str(response2[3]['Inventory'])) + '--¥' + str(response2[3]['Price']))
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[0]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                    else:
                        ss.append('-' * 13)
                        if response2[1]['Inventory'] != 0:
                            ss.append('余{}张'.format(str(response2[1]['Inventory'])) + '--¥' + str(response2[1]['Price']))
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
                        else:
                            ss.append('-' * 13)
                            if response2[2]['Inventory'] != 0:
                                ss.append(
                                    '余{}张'.format(str(response2[2]['Inventory'])) + '--¥' + str(response2[2]['Price']))
                            else:
                                ss.append('-' * 13)
    return trainData