import re
import urllib.request

base = 'http://hq.sinajs.cn/list='
bios = 'sh600660'

def GetTotalData(inputstr):
    '''
    input a number serial, ex:600660
    '''
    pattern_id = '\d{6}'
    reobj = re.compile(pattern_id)
    id = reobj.findall(inputstr)
    id = "".join(id)
    page = ''
    if id != '':
        flag = int(id)
        if flag >= 600000:
            bios = 'sh' + id
        else:
            bios = 'sz' + id
        inputstr = base + bios
#        print(inputstr)
        page = urllib.request.urlopen(inputstr).read()
#        print(page)
        if len(page) < 30:
            print('error, invalid id')
            return 0
        s = page[30:]
        s = str(s)
        
        pattern_data = '\d+\.*\d*(?=,)'
        reobj = re.compile(pattern_data)
        data = reobj.findall(s)
        data.pop()
        data.pop()
        
        pattern_data = '\d\d\d\d-\d\d-\d\d'
        reobj = re.compile(pattern_data)
        date = reobj.findall(s)
        data.append(date)
        
        pattern_data = '\d\d:\d\d:\d\d'
        reobj = re.compile(pattern_data)
        time = reobj.findall(s)
        data.append(time)
        data.append(id)
        return data
    else:
        print('invalid id')
        return 0
