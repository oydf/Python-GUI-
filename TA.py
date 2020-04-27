import wx
import urllib.request
import urllib.parse
import json
from urllib import request
from bs4 import BeautifulSoup
import sys
import chardet
from urllib.parse import quote
import  string

123456678912312121212120
12345667890qwehiuqwheuhwqiehiuwqheiu
def translater_somewords(src_word):
    data = {}
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
    data['i'] = src_word
    data['type'] = 'AUTO'
    data['from'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_ENTER'
    data['typoResult'] = 'true'
    data = urllib.parse.urlencode(data).encode('utf-8')
    resu = urllib.request.urlopen(url, data)
    html = resu.read().decode('utf-8')
    html = json.loads(html)
    return html['translateResult'][0][0]['tgt'] + '\n'

def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def translater_word_en(src_word):
    src_word = src_word.strip("\n")
    url = 'http://dict.youdao.com/w/%s/#keyfrom=dict2.top'%(src_word)
    url = quote(url, safe = string.printable)
    response = request.urlopen(url)
    html = response.read().decode("utf-8")
    bs=BeautifulSoup(html,'html.parser')
    
    if not is_contain_chinese(src_word):
        all_li = bs.find('div', class_='trans-container').find_all('li')
        reslut = ''
        for res in all_li:
            reslut += res.string+'\n'
        return reslut
    else:
        all_a = bs.find_all(class_='search-js')
        #print(all_a)
        reslut = ''
        for res in all_a:
            if not is_contain_chinese(res.string):
                reslut += res.string+'; '
            else:
                break
        reslut+='\n'
        return reslut

def getweathere(loc):
    LocHash = {'武侯':'101270119','金堂':'101270105','成都':'101270101','双流':'101270106'}
    url = 'http://www.weather.com.cn/weather/%s.shtml'%(LocHash[loc])
    response = request.urlopen(url)
    html = response.read().decode("utf-8")
    bs=BeautifulSoup(html,'html.parser')
    all_li = bs.find('li', class_='sky skyid lv3 on')
    if all_li.span.string == None:
        res = loc +' '+all_li.h1.string.replace('（今天）','')+' '+ all_li.p.string+' '+all_li.i.string
    else:
        res = loc +' '+all_li.h1.string.replace('（今天）','')+' '+ all_li.p.string+' '+all_li.i.string.replace('℃','') + '~' + all_li.span.string + '度'
    return res

def main():
    app=wx.App()
    win=wx.Frame(None,title="翻译助手",pos=(1500,500), size=(300,330))
    win.SetMaxSize(size=(300,330))
    win.SetMinSize(size=(300,330))
    ico = wx.Icon('dog.ico', wx.BITMAP_TYPE_ICO)
    win.SetIcon(ico)
    word=wx.TextCtrl(win,pos=(0,30),size=(300,100),style=wx.TE_MULTILINE | wx.TE_RICH2)
    weathere=wx.TextCtrl(win,pos=(0,0),size=(300,30),style=wx.TE_MULTILINE | wx.TE_RICH2 |wx.TE_READONLY)
    
    result=wx.TextCtrl(win,pos=(0,130),size=(300,150),style=wx.TE_MULTILINE|wx.TE_READONLY | wx.TE_RICH2)
    weathere.SetValue(getweathere('成都'))

    def wea_change(event):
        if not hasattr(wea_change, 'x'):
            wea_change.x = 0
        city_list = ['武侯','金堂','成都','双流']
        kcode = event.GetKeyCode()
        if kcode == 314 or kcode == 315:
            if wea_change.x < 3:
                wea_change.x += 1
            else:
                wea_change.x = 0
        else:
            if wea_change.x > 0:
                wea_change.x -= 1
            else:
                wea_change.x = 3
        weathere.SetValue(getweathere(city_list[wea_change.x]))

    def change_size(event):
        keywords = word.GetValue()
        if keywords == '' or keywords == '/n':
            result.SetValue('')
        else:
            try:
                res1 = translater_word_en(keywords)
                # print(res1)
                # print(res1 == '\n')
                if res1 !='\n':
                    res1 ='词典翻译:\n' + res1
                else:
                    res1 = ''
            except:
                res1 = ''
            try:
                res2 = '整句翻译:\n' + translater_somewords(keywords)
            except:
                res2 = '请重试...'
            result.SetValue( res1 + res2)

    def clear_res(event):
        if word.GetValue()== '':
            result.SetValue('')

    weathere.Bind(wx.EVT_KEY_UP,wea_change)
    word.Bind(wx.EVT_TEXT_ENTER,change_size)
    word.Bind(wx.EVT_KEY_UP,clear_res)
    win.SetTransparent(160)
    win.Show()
    app.MainLoop()


if __name__=='__main__':main()
