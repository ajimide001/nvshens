#-*- coding:utf-8 -*-
import requests
import time
import re
from bs4 import BeautifulSoup
class NvShen(object):
    def __init__(self):
        self.s = requests.session()
        self.base_url = 'https://www.nvshens.com'
    def get_nv_url(self): #获取女神首页url链接
        nv_url = 'https://www.nvshens.com/ajax/girl_query_total.ashx'
        nv_data = {
            'country': '中国',
            'professional': '主播',
            'curpage': '2',
            'pagesize': '20',
        }
        res = self.s.post(url=nv_url,data=nv_data)
        html = BeautifulSoup(res.text,'lxml')
        a = html.find_all('a')
        # print(a)
        last_num = int(a[-1].text[3:])
        print('总页数:{}'.format(last_num))
        all_url = []
        for i in range(1,last_num+1):
            nv_data['curpage'] = i
            res = self.s.post(url=nv_url, data=nv_data)
            html = BeautifulSoup(res.text, 'lxml')
            a = html.find_all('a',href=re.compile('girl'),text=re.compile('\w'))
            all_url.extend(a)
        return all_url



    def get_nv_url_response(self,nv_url): #通过女神首页url链接 获取response内容
        url = self.base_url + nv_url
        try:
            res = self.s.get(url=url)
            res.encoding = 'utf-8'
            return res
        except Exception as e:
            print('{}获取超时{}'.format(url,e))


    def pipe_data(self,res): #清洗数据
        html = BeautifulSoup(res.text,'lxml')
        shenfen = html.find_all('table')[0].text
        xinxi = html.find_all(class_='infocontent')[0].text
        # img_url = html.select('a[class="igalleryli_link"] img' )
        img_url = html.find_all('a',class_= 'igalleryli_link' )
        # print(shenfen)
        # print(xinxi)
        all_url = []
        for i in img_url:
            all_url.append((i['href'],i.img['title'],i.img['data-original'][:-11]))
        return [shenfen,xinxi,all_url]
    def get_img_num(self,img_url):
        url = self.base_url + img_url
        res = self.s.get(url)
        html = BeautifulSoup(res.text,'lxml')
        num = html.find_all('div',id='dinfo')
        num = num[0].span.text[:-3]
        return num


    def main(self):
        datas = []
        for i in self.get_nv_url():
            datas.append(i.text)
            tuple_url = self.pipe_data(self.get_nv_url_response(i['href']))
            # for k in tuple_url[2]:
            #     num = self.get_img_num(k[2])
            #     k.append(num)
            print(tuple_url)

            # break

if __name__ == '__main__':
    n = NvShen()
    n.main()
    print('结束')