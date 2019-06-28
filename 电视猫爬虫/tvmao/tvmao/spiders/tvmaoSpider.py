# -*- coding: utf-8 -*-
import scrapy
import json
import requests

from .rules import *
import time
from ..items import TvmaoItem,ActorItem,subMainItem
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }


class metas(dict):
    def __init__(self,dic=None):
        super().__init__()
        if dic is not None:
            self.update(dic)

    def __setattr__(self, key, value):
        if value is None: value = ''
        if key is not None:
            self[key] = value

def get_data(li,rule,sign):
    for i in li:
        pTag = exeRe(i, rule, tp='')
        for p in pTag:
            if sign in p:
                return p.replace(sign, '')
    return ''

def get_actHome(url):
    try:
        response = requests.get(url,headers=headers)
        c = response.text
        u = exeRe(c,gaurl)
    except:
        time.sleep(10)
        response = requests.get(url)
        c = response.text
        u = exeRe(c, gaurl)
    if u:
        return "https://m.tvmao.com" + u,u
    else:
        return '',''
def sss(data):
    a = ''
    for k,v in data.items():
        a += k + '=' + v + '&'
    return a[:-1]
def get_review(data,result = None):
    data1 = {k:str(v) for k,v in data.items()}
    url = "https://www.tvmao.com/servlet/listcomments"
    if result is None:
        result = []
    url += "?" + sss(data1)
    response = requests.get(url,headers=headers)
    # response = requests.get('https://www.tvmao.com/servlet/listcomments?typeId=11&resId=100285&wapShow=true&start=0&ps=30',headers=headers)
    c = response.text

    rlist = json.loads(c)
    if len(rlist) > 0:
        html = rlist[1]
        li = html.split("material_comment")[1:]
        for i in li:
            redict = dict()
            redict['user'] = exeRe(i,getUser)
            redict['comment'] = exeRe(i,getcont)
            redict['putTime'] = exeRe(i,pTime)
            redict["reply"] = []
            relis = exeRe(i,relist,reli,tp='')
            for ii in relis:
                rd = dict()
                rd['user'] = exeRe(ii,reply)
                rd['reTime'] = exeRe(ii,reTime)
                rd['recontent'] = exeRe(ii,recont)
                redict["reply"].append(rd)
            result.append(redict)
    else: return result
    if len(rlist) == 3:# True
        data['start'] = data['start'] + 30
        result = get_review(data,result=result)
    else:
        return result

def parse_PC(response,meta):
    # PC端获取评论和语言
    meta = metas(meta)
    data = dict(typeId=exeRe(response.text, getA, TID).replace(' ', ''), resId=exeRe(response.text, getA, resID).replace(' ', ''),
                wapShow='true', start=0, ps=30)
    meta.review = get_review(data)
    meta.Language = exeRe(response.text,langu)
    return meta
titleDict = dict()
import xlrd
book = xlrd.open_workbook("drama.xlsx")
sheet1 = book.sheet_by_index(0)
rows = sheet1.nrows
for i in range(1,rows):
    row = sheet1.row_values(i)
    if row[4] == '':
        titleDict[row[2]] = row[1]





class TvmaospiderSpider(scrapy.Spider):
    name = 'tvmaoSpider'
    allowed_domains = ['m.tvmao.com',"www.tvmao.com"]
    start_urls = []
    for k,v in titleDict.items():

        start_urls.append(k)
    # global titleDict




    def parse(self, response):
        c = response.text
        meta = metas()
        meta.ID = response.url.split("drama/")[1]
        meta.Title = titleDict.get(response.url,'')
        zys = exeRe(c, zy, tp='')
        meta.Role_info = get_data(zys,zyp,"主演：")
        meta.Director = get_data(zys,zyp,"导演：")
        meta.URL = response.url
        # scr = exeRe(c,script)
        # sc = json.loads(scr) if scr else {}
        # Img = sc.get("images",'') if sc else ''
        # meta.Img = Img[0] if len(Img) > 0 else ''
        meta.Img = exeRe(c,poster,IMG)
        meta.Viedo_rb = get_data(zys,zyp,'集数：')
        meta.Screenwriter = get_data(zys,zyp,'编剧：')
        meta.Location = get_data(zys,zyp,'地区：')
        meta.Intro_type = exeRe(c,getTP,getTPa)
        meta.Intro_Era = get_data(zys,zyp,"年份：")
        meta.Language = ''# 语言 TODO 电视剧没有发现“语言”，电影待看
        summ =exeRe(c,summary,tp = '')
        meta.Intro_brief_des = summ[0].replace("</p>","").replace("<p>",'') if len(summ) > 0 else ''
        meta.PVNum = ''# 播放量 TODO 这个也没发现，电影待看
        meta.Score = exeRe(c,score)
        lw = exeRe(c,likewatch)
        meta.W_watch = lw.replace("人",'') if "人" in lw else lw
        meta.N_watch = ''# 在看人数 TODO 没找到，电影待看

        actURL= response.url + "/actors"
        submainURL= response.url + "/episode"
        playtimeURL = response.url + "/playingtime"

        yield scrapy.Request(url=playtimeURL, callback=self.parse_playTime, meta=meta)
        yield scrapy.Request(url=actURL, callback=self.parse_act, meta=meta)
        yield scrapy.Request(url=submainURL, callback=self.parse_subMain, meta=meta)


        ########################################################

    def parse_playTime(self,response):
        meta = metas(response.meta)
        c = response.text
        one = exeRe(c,plTIME,tp='')
        two = exeRe(c,getTV,tp = '')
        meta.Show_time = dict()
        meta['Show_time']['one'] = one
        li = []
        for i in two:
            dics = {}
            dics['TVname'] = exeRe(i,getTVname)
            dics['TVtime'] = exeRe(i,getTVmain)
            li.append(dics)
        meta['Show_time']['TV'] = li
        rwgx = response.url.replace("playingtime",'') + "renwuguanxitu"
        yield scrapy.Request(url=rwgx, callback=self.parse_RWGX, meta=meta)


    def parse_RWGX(self,response):
        c = response.text
        meta = metas(response.meta)
        p = ''
        ul = exeRe(c,RWGXT,tp = '')
        for i in ul:
            li = exeRe(i,getLI,tp = '')
            for l in li:
                p += exeRe(l,getP)
        meta.Relationship = p
        pcURL = "https://www.tvmao.com/drama/" + meta.get("ID")
        newre = requests.get(pcURL,headers=headers)
        meta = parse_PC(newre,meta)
        item = TvmaoItem()
        item._values = meta
        yield item
        # print(meta)
        # yield scrapy.Request(url=pcURL, callback=self.parse_PC, meta=meta)

    def parse_PC(self,response):
        # PC端获取评论和语言
        meta = metas(response.meta)
        data = dict(typeId=exeRe(response.text, getA, TID).replace(' ', ''),
                    resId=exeRe(response.text, getA, resID).replace(' ', ''),
                    wapShow='true', start=0, ps=30)
        meta.review = get_review(data)
        meta.Language = exeRe(response.text, langu)
        return meta
        # item = TvmaoItem()
        # item._values = meta
        # yield item



    def parse_subMain(self,response):
        # 剧集列表
        c = response.text
        u = response.url
        meta = metas()
        meta.Sub_main_id = response.meta['ID']
        p2 = exeRe(c,pages2,tp='')
        for i in p2:
        # for i in newURL:
            newURL = exeRe(i, pages)
            meta.Sub_id = newURL.split('/episode/')[1]
            meta.Sub_info_num = exeRe(i,getA2)
            yield scrapy.Request(url="https://m.tvmao.com" + i, callback=self.parse_subMain2, meta=meta)

    def parse_subMain2(self,response):
        # 剧集详情
        c = response.text
        meta = metas(response.meta)
        # meta.Sub_id = exeRe(c,appid)# TODO 是appid还是连接？
        # meta.Sub_info_num = meta.get('Sub_id').split('-')[1] if '-' in meta.get('Sub_id') else meta.get('Sub_id')
        meta.Sub_info_title =exeRe(c,pTitle).split("：")[1]
        meta.Sub_info_pic = json.loads(exeRe(c,mainimg) + ']')# 剧集图片 TODO 这个也没看到呀，是简介里的图片吗
        meta.Sub_info_detail_txt = exeRe(c,mainsumm,mainp)
        meta.Sub_publishTime =exeRe(c,pdate)
        meta.Sub_review = ''# 注意：不是API中的“playCount”字段，需要打开每个视频看到 TODO 这个在哪打开视频？
        # print(meta)
        item = subMainItem()
        item._values = meta
        yield item

    # 演员
    def parse_act(self,response):
        c = response.text
        u = response.url
        Sub_id = response.meta["ID"]
        li = exeRe(c,actList,tp='')
        for i in li:
            item = ActorItem()
            a = exeRe(i,act,tp = '')

            for aa in a:
                Aurl = exeRe(aa, aurl)
                meta = metas()
                sa = "https://m.tvmao.com" + Aurl
                meta.Actor_url,meta.Actor_id = get_actHome(sa)
                meta.Actor_name = exeRe(aa,actName).replace("演员 ",'')
                meta.Role_name = exeRe(aa,aName)
                meta.Sub_id = Sub_id
                meta.Role_intro = exeRe(aa,actSumm)
                meta.Actor_rating = exeRe(aa,actScore)
                # print(meta)
                item._values = meta
                yield item


