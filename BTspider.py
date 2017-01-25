import requests
from bs4 import BeautifulSoup
import os
import win32con
import win32clipboard as w
import time

def getText():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d

def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def spider(num,key,href):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    url = 'https://www.torrentkitty.tv/search/' + key+ '/'+str(num)
    res = requests.get(url, headers=headers)
    res.encoding = 'uft-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.select('#archiveResult')[0]
    count = 1
    for tr in table.find_all('tr'):
        name = tr.select('.name')[0].text
        if 'Torrent' in name:
            continue
        try:
            print(str(count) + '.' + name)
            print('')
        except:
            continue
        href.append(tr.find_all('a')[1]['href'])
        count += 1


def menu2(num,key,href):
    while (True):
        n = input("请选择要下载的内容序号(换一批按0，结束选择按e,一次输入一个序号): ")
        if n == '0':
            os.system('cls')
            num += 1
            href = []
            try:
                spider(num, key, href)
            except IndexError:
                print("这已是全部资源了!")
            except Exception as e:
                print(e)
            menu2(num,key,href)
        elif n == 'e':
            torrent=''
            f = open('torrent.txt', 'r')
            lines = f.readlines()
            for line in lines:
                torrent=torrent+line+'\n'
            f = open('torrent.txt', 'w')
            f.close()
            setText(torrent)
            print("现在请打开迅雷或qq旋风，若无反应按新建下载")
            print('5秒后自动退出')
            time.sleep(5)
            os._exit(1)
        else:
            f = open('torrent.txt', 'a')
            f.write(href[int(n) - 1] + '\n')
            f.close()

while(True):
    key = input("请输入搜索内容: ")
    href = []
    num = 1
    try:
        spider(num, key, href)
    except IndexError:
        print("未找到有关资源")
    except:
        print("网络异常或未知错误!")
        time.sleep(3)
        os._exit(1)
    else:
        break
menu2(num, key, href)

