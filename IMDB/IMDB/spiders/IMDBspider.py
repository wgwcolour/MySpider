# -*- coding: utf-8 -*-
import scrapy
import re
import json
from ..items import ImdbItem,ImdbItemActor,Awards
from lxml import etree

def getRule(rule):
    return re.compile(rule, re.S)
#链接对应名字
NameDict = {}
#Id
getIdRule = getRule("/tt(.*?)/")# 获取id
#stars
getStarsRule1 = getRule("<h4 class=\"inline\">Stars:</h4>(.*?)<span")
getStarsRule2 = getRule("<a.*?>(.*?)</a>")
# director
getDirector1 = getRule("<h4 class=\"inline\">Director:</h4>(.*?)</div>")
getDirector2 = getRule("<a.*?>(.*?)</a>")
# Img
getImg1 = getRule("class=\"poster\">(.*?)</div>")
getImg2 = getRule("<img.*?src=\"(.*?)\"")
#
getTime = getRule("datetime=\"PT([0-9]+)M")
# Intro_type
div = getRule("<div class=\"title_wrapper\">(.*?)</div>")
getIntro_type = getRule("<a href=\"/search/title\?genres=.*?>(.*?)</a>")
#Intro_Era
getIntro_Era = getRule("\"See more release dates\" >(.*?)</a>")
# Intro_brief_des
getIntro_brief_des = getRule("<div class=\"summary_text\">(.*?)</div>")
#
getScore = getRule("<span itemprop=\"ratingValue\">(.*?)</span")
#Metascore
getMetascore1 = getRule("class=\"metacriticScore score_favorable titleReviewBarSubItem\">(.*?)</div>")
getMetascore2 = getRule("<span>(.*?)</span>")
#RevUser
getRevUser = getRule("itemprop=\"reviewCount\">(.*?)user</s")
#RevCritic
getRevCritic = getRule("reviewCount.*?itemprop=\"reviewCount\">(.*?)critic</s")
#Popularity
getPopularity1 = getRule("class=\"titleOverviewSprite popularityTrendUp\"></div>(.*?)</span>")
getPopularity2 = getRule("<span class=\"subText\">.*?([0-9]+)")
#
getVotes = getRule("itemprop=\"ratingCount\">(.*?)</span>")
#
getActor = getRule("<table class=\"cast_list\">(.*?)</table>")
getTr = getRule("<tr class=\"(.*?)</tr>")
getActor_id = getRule("<a href=\"/name/nm([0-9]+)/?")
#
getActor_name = getRule("<td>.*?<a href=\"/name/nm.*?>(.*?)</a>")
#Role_name
getRole_name = getRule("<td class=\"character\">.*?<a.*?>(.*?)</a>")
getRole_name2 = getRule("<td class=\"character\">(.*?)</td>")

getActorUrl = getRule("id=\"titleCast\">(.*?)See full cast")
getseeMore = getRule("<a href=\"(fullcredits.*?)\"")
getActor_avatar = getRule("loadlate=\"(.*?)\"")
#
getActorHome = getRule("<a href=\"(/name/nm.*?)\"")
#Actor_career
getActor_career = getRule("\"jobTitle\": (.*?)\"description\"")
#PProduce
getPProduce = getRule("Produced by(.*?)</table>")
getPProduce2 = getRule("<td class=\"name\">.*?>(.*?)</a>")
#
getMusic = getRule("Music by(.*?)</table>")
getPCine= getRule("Cinematography by(.*?)</table>")
#
getActor_Influence = getRule("id=\"meterRank\" >(.*?)</a>")
#
getplotsummary = getRule("<h2>Storyline</h2>.*?<span class=\"see-more inline\">(.*?)</span>")
getsumary2 = getRule("<a href=\"(.*?)\"")
#
getSum1 = getRule("id=\"summaries\"(.*?)</ul>")
getSum2 = getRule("<li(.*?)</li>")
getP = getRule("<p>(.*?)</p>")
getN = getRule("<a.*?>(.*?)</a>")
#
getSy = getRule("id=\"synopsis\"(.*?)</ul>")
getSy1 = getRule("<li.*?>(.*?)</li>")
subTag = getRule("<a.*?>|<br/>")
#
getsee = getRule("See also(.*?)</p>")
getKeyWords = getRule("Synopsis.*?(/title/.*?/keywords?.*?)\"")
getK = getRule("<td class=\"soda sodavote\".*?data-item-keyword=\"(.*?)\">")
#
getTaglinesURL = getRule("See also.*?<a href=\"(.*?taglines?.*?)\"")
getTag = getRule("<div class=\"soda odd\">(.*?)</div>")
#
getGenres1 = getRule("<h4 class=\"inline\">Genres:</h4>(.*?)</div>")
getGenres2 = getRule(">(.*?)</a>")
#
getDetail = getRule("<h2>Details</h2(.*?)<hr />")
getOfficial = getRule("Official Sites:</h4(.*?)</div>")
#
getCountry = getRule(">Country:</h4>(.*?)</div>")
#
getLanguage = getRule(">Language:</h4>(.*?)</div>")
#
getRelease = getRule("Release Date:</h4>(.*?)<span")
#
uuname = getRule("(.*?)\,https.*?")
uurl = getRule("(https://.*?)")
def getName(title):
    rule = title + "(.*?)</table>"
    return getRule(rule)



class metas(dict):
    def __init__(self,dic=None):
        super().__init__()
        if dic is not None:
            self.update(dic)

    def __setattr__(self, key, value):
        if value is None: value = ''
        if key is not None:
            if isinstance(value,str):
                self[key] = value.strip().strip("\n")
            else:
                self[key] = value




class ImdbspiderSpider(scrapy.Spider):
    name = 'IMDBspider'
    allowed_domains = ['www.imdb.com']
    start_urls = []
    # start_urls = ['https://www.imdb.com/title/tt0111161/?ref_=adv_li_tt',"https://www.imdb.com/title/tt0147800/?ref_=fn_tt_tt_1"]
    global NameDict
    with open("imdb.csv","r",encoding="utf-8") as f:
        content = f.readlines()
        for d,i in enumerate(content):
            if d != 0:

                # row = i.split(",")
                n = re.findall(uuname,i)
                if len(n) == 0:
                    with open('error.txt','a+',encoding='utf-8') as e:
                        e.write(i)
                        e.write('\n')
                    continue
                u = i.replace(n[0],'')
                start_urls.append(u.replace("\n",'').replace(',',''))
                NameDict[u.replace("\n",'').replace(',','')] = n[0].replace("\n",'')
    print("加载完成")

    def parse(self, response):
        meta = metas()
        meta.ID = self.getId(response.url)#Id
        meta.Title = NameDict.get(response.url,'')#Title
        meta.Role_info = self.getStars(response)#Role_info
        meta.Director = self.exeRe(response.text,getDirector1,getDirector2)
        meta.URL = response.url
        meta.Img = self.exeRe(response.text,getImg1,getImg2)
        meta.Viedo_rb =self.exeRe(response.text,getTime,tp='')[0]#!!!
        meta.Intro_type =self.exeRe(response.text,div,getIntro_type)#!!!
        years_erae = self.exeRe(response.text,getIntro_Era).split('(')
        meta.Intro_Era = ','.join(years_erae).replace(')','')
        meta.Intro_brief_des = self.exeRe(response.text,getIntro_brief_des)
        meta.PVNum = self.exeRe(response.text,getVotes).replace(",",'')
        meta.Score = self.exeRe(response.text,getScore)
        meta.Metascore = self.exeRe(response.text,getMetascore1,getMetascore2)
        meta.RevUser = self.exeRe(response.text,getRevUser)
        meta.RevCritic = self.exeRe(response.text,getRevCritic)#!!!
        meta.Popularity = self.exeRe(response.text,getPopularity1,getPopularity2)
        meta.Genres = self.exeRe(response.text, getGenres1, getGenres2, tp='')
        ofs = self.exeRe(response.text,getDetail,getOfficial)
        meta.Off_sites = self.exeRe(ofs,getRule("<a.*?>(.*?)</a>"),tp='')
        coun = self.exeRe(response.text,getDetail,getCountry)
        meta.Country = self.exeRe(coun,getRule("<a.*?>(.*?)</a>"),tp='')
        Lang = self.exeRe(response.text,getDetail,getLanguage)
        meta.Language = self.exeRe(Lang,getRule("<a.*?>(.*?)</a>"),tp='')
        # rele = self.exeRe(response.text, getDetail, getRelease)
        meta.Release_date = self.exeRe(response.text, getDetail, getRelease)
        meta.Budget = self.exeRe(response.text,getRule("<h4 class=\"inline\">Budget:</h4>(.*?)<"))
        meta.Open_weekend = self.exeRe(response.text,getRule("Opening Weekend USA:</h4>(.*?)<span"))
        meta.Gross = self.exeRe(response.text,getRule("Gross USA:</h4>(.*?)</"))
        meta.W_Gross = self.exeRe(response.text,getRule("Cumulative Worldwide Gross:</h4>(.*?)</"))
        meta.Runtime = self.exeRe(response.text,getRule("Runtime:</h4>.*?>(.*?)</time>"))
        meta.SoundMix = self.exeRe(response.text,getRule("Sound Mix:</h4>(.*?)</div>"),getRule("<a.*?>(.*?)</a>"),tp='')
        meta.Color = self.exeRe(response.text,getRule("<h4 class=\"inline\">Color:</h4>(.*?)</div>"),getRule("<a.*?>(.*?)</a>"),tp='')
        meta.Aspect_ratio = self.exeRe(response.text,getRule(">Aspect Ratio:</h4>(.*?)</div>"))
        plotURL = "https://www.imdb.com" + self.exeRe(response.text, getplotsummary,getsumary2)
        meta.nextURL = plotURL

        ActorUrl = response.url.split('?')[0] + self.exeRe(response.text,getActorUrl,getseeMore)
        yield scrapy.Request(url=ActorUrl, callback=self.parse_Actor, meta=meta)


    def parse_Actor(self,response):
        meta = metas(response.meta)
        meta.Pproduce = self.exeRe(response.text,getPProduce,getPProduce2,tp='')
        meta.PMusic = self.exeRe(response.text,getMusic,getPProduce2,tp='')
        meta.PCine = self.exeRe(response.text,getPCine,getPProduce2,tp='')
        meta.PEditing = self.exeRe(response.text,getName("Film Editing by"),getPProduce2,tp='')
        meta.PCasting = self.exeRe(response.text,getName("Casting By"),getPProduce2,tp='')
        meta.PPDesign = self.exeRe(response.text,getName("Production Design by"),getPProduce2,tp='')
        meta.PArtDir = self.exeRe(response.text,getName("Art Direction by"),getPProduce2,tp='')
        meta.PDecoration = self.exeRe(response.text,getName("Set Decoration by"),getPProduce2,tp='')
        meta.PCDesign = self.exeRe(response.text,getName("Costume Design by"),getPProduce2,tp='')
        meta.PMakeup = self.exeRe(response.text,getName("Makeup Department"),getPProduce2,tp='')
        meta.ProductionManagement = self.exeRe(response.text,getName("Production Management"),getPProduce2,tp='')
        meta.PSDirector = self.exeRe(response.text,getName("Second Unit Director or Assistant Director"),getPProduce2,tp='')
        meta.PArtDep = self.exeRe(response.text,getName("Art Department"),getPProduce2,tp='')
        meta.PSoundDep = self.exeRe(response.text,getName("Sound Department"),getPProduce2,tp='')
        meta.PSpecialEff = self.exeRe(response.text,getName("Special Effects by"),getPProduce2,tp='')
        meta.PVisualEff = self.exeRe(response.text,getName("Visual Effects by"),getPProduce2,tp='')
        meta.PStunts  = self.exeRe(response.text,getName("<h4 class=\"dataHeaderWithBorder\">Stunts"),getPProduce2,tp='')
        meta.PCameraDep = self.exeRe(response.text,getName("Camera and Electrical Department"),getPProduce2,tp='')
        meta.PCastingDep = self.exeRe(response.text,getName("Casting Department"),getPProduce2,tp='')
        meta.PCostumeDep  = self.exeRe(response.text,getName("Costume and Wardrobe Department"),getPProduce2,tp='')
        meta.PEditorialDep = self.exeRe(response.text,getName("Editorial Department"),getPProduce2,tp='')
        meta.PLocationMan = self.exeRe(response.text,getName("Location Management"),getPProduce2,tp='')
        meta.PMusicDep = self.exeRe(response.text,getName("Music Department"),getPProduce2,tp='')
        meta.PTransportationDep = self.exeRe(response.text,getName("Transportation Department"),getPProduce2,tp='')
        meta.POther = self.exeRe(response.text,getName("Other crew"),getPProduce2,tp='')
        meta.PThanks  = self.exeRe(response.text,getName("<h4 class=\"dataHeaderWithBorder\">Thanks"),getPProduce2,tp='')


        # 演员
        tr = self.exeRe(response.text, getActor, getTr, tp='')
        for index,i in enumerate(tr):
            Actor = metas()
            Actor.Sub_id = response.meta.get('ID')
            Actor.Actor_id = self.exeRe(i, getActor_id,tp='')[0]
            Actor.Actor_name = self.exeRe(i, getActor_name)
            rn = self.exeRe(i, getRole_name)
            if rn:
                Actor.Role_name =rn
            else:
                Actor.Role_name = self.exeRe(i, getRole_name2)
            # Actor.Actor_Influence = index+1 # 演员排名/影响力 TODO 是否应该用顺序表示？？？？
            Actor.Actor_avatar = self.exeRe(i,getActor_avatar)
            ActorHomeUrl = "https://www.imdb.com" + self.exeRe(i,getActorHome)
            yield scrapy.Request(url=ActorHomeUrl, callback=self.ActorHome, meta=Actor)
        # 剧情

        yield scrapy.Request(url=meta.get('nextURL'), callback=self.plotPage, meta=meta)
        # 奖项
        awards_url = meta.get('nextURL').replace('plotsummary?ref_=tt_stry_pl','awards?ref_=tt_awd')
        yield scrapy.Request(url=awards_url,callback=self.awards)

    def awards(self,response):
        subId = self.getId(response.url)
        txt = response.text
        html = etree.HTML(txt)
        div = html.xpath("//div[@class='article listo']")
        ddv = div[0] if len(div) else None
        if ddv:
            content = etree.tostring(ddv).decode('utf-8')
            rl1 = getRule("(<h3>.*?</table><br)")# 片段
            rlname = getRule("<h3>(.*?)<a")# 奖项
            rlyears = getRule("event_year.*?>(.*?)</")
            table = self.exeRe(content,rl1,tp='')
            rlTr = getRule("(<tr>.*?</tr>)")
            rlb = getRule("<b>(.*?)</b><br")
            rla = getRule("award_description\">(.*?)<br")
            rltd = getRule("(<td class=\"award_description\">.*?</td>)")
            rluser = getRule("<a.*?nm([0-9]+).*?>(.*?)</a>")
            rlc = getRule("award_category.*?>(.*?)<")

            li = []
            for i in table:
                awards = {}
                title_award_outcome = ''
                c = ''
                name = self.exeRe(i,rlname)
                years = self.exeRe(i,rlyears)
                awards['name'] = name
                awards['years'] = years
                # 先找tr
                tr = self.exeRe(i,rlTr,tp = '')
                awards['list'] = []
                for t in tr:
                    ali = {}
                    if "title_award_outcome" in t:# 更新标题：获奖还是提名
                        title_award_outcome = self.exeRe(t,rlb)
                        c = self.exeRe(t,rlc)
                    ali['name'] = title_award_outcome
                    ali['award_category'] = c
                    td = self.exeRe(t,rltd)
                    a =self.exeRe(td,rla)# 奖项名称
                    b = re.findall(rluser,td)
                    ali['award_description'] = a
                    ali['Actor'] = [{'name':i[1],'id':i[0]} for i in b]
                    awards['list'].append(ali)
                li.append(awards)

            meta = metas()
            meta.Sub_id = subId
            meta.awards = li
            item = Awards()
            item._values = meta
            yield item
            # meta.AwardsName=name
            # meta.years = years


    def ActorHome(self,response):
        meta = metas(response.meta)
        rank = self.exeRe(response.text,getActor_Influence)
        if rank.find("SEE RANK") != -1:
            rank = "NA"
        meta.Actor_Influence = rank#TODO 这个排名到底在哪
        meta.Actor_career = self.exeRe(response.text,getActor_career)
        #
        # if careerList:
        #     acJson = json.loads(careerList)
        #     meta.Actor_career = ','.join(acJson.get('jobTitle',''))
        # else:
        #     acJson = {}
        #     meta.Actor_career = ''
        meta.Actor_birthday = self.exeRe(response.text,getRule("\"birthDate\": \"(.*?)\""))
        meta.Actor_infor = self.exeRe(response.text,getRule("\"description\": \"(.*?)\""))
        item = ImdbItemActor()
        item._values = meta
        yield item

    def plotPage(self,response):
        meta = metas(response.meta)
        sum = self.exeRe(response.text,getSum1,getSum2,tp = '')
        Summaries = []
        for i in sum:
            P = self.exeRe(i,getP)
            N = self.exeRe(i,getN)
            Summaries.append(P + "----" + N)
        meta.Summaries = Summaries
        synopsis = self.exeRe(response.text,getSy,getSy1)
        meta.Synopsis = re.sub(subTag,'',synopsis)
        KeywordsURL = self.exeRe(response.text,getsee,getKeyWords)
        yield scrapy.Request(url="https://www.imdb.com" + KeywordsURL, callback=self.parseKeyWords, meta=meta)

    def parseKeyWords(self,response):
        meta = metas(response.meta)
        meta.PlotKeywords = self.exeRe(response.text,getK,tp='')
        tagURL = "https://www.imdb.com" + self.exeRe(response.text,getTaglinesURL)
        yield scrapy.Request(url=tagURL, callback=self.parseTAG, meta=meta)

    def parseTAG(self,response):
        meta = metas(response.meta)
        meta.Taglines = self.exeRe(response.text,getTag)
        item = ImdbItem()
        item._values = meta
        yield item



    def exeRe(self,strs, re1, re2=None,tp = 'str'):
        if re2 is not None:
            result = re.findall(re1, strs)
            cont = result[0] if len(result) > 0 else ''
            return ','.join(re.findall(re2, cont)) if tp == "str" else re.findall(re2, cont)
        else:
            return ','.join(re.findall(re1, strs)) if tp == "str" else re.findall(re1, strs)

    def getId(self,url):
        return self.exeRe(url,getIdRule)

    def getStars(self,response):
        return self.exeRe(response.text,getStarsRule1,getStarsRule2)

