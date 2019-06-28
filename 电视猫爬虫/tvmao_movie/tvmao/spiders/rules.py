import re

def Rule(rule):
    return re.compile(rule, re.S)


def exeRe(strs, re1, re2=None,tp = 'str'):
    if re2 is not None:
        result = re.findall(re1, strs)
        cont = result[0] if len(result) > 0 else ''
        return ','.join(re.findall(re2, cont)) if tp == "str" else re.findall(re2, cont)
    else:
        return ','.join(re.findall(re1, strs)) if tp == "str" else re.findall(re1, strs)
# 主页
zy = Rule("<div class=\"clear\">(.*?)</div>")
zy1 = Rule("<div class=\"d_s_info\">(.*?)</div>")
zyp = Rule("<p>(.*?)</p>")
script = Rule("application/ld+json\">(.*?)</script>")
getTP = Rule("<p class=\"d_cate over_hide\">(.*?)</p>")
getTPa = Rule("<a.*?>(.*?)</a>")
summary = Rule("<div class=\"lessmore\">(.*?)</div>")
score = Rule("<p class=\"play_text\">(.*?)<span>")
likewatch = Rule("<div class=\"like_btn_div\"><p class=\"top\">(.*?)</p>")
poster = Rule("<div class=\"m_s_i\">(.*?)</div>")
IMG = Rule("src=\"(.*?)\"")
scoreSPAN = Rule("<span class=\"score\">(.*?)<span class=\"fen\">")
scoreiunit = Rule("<span class=\"unit\">(.*?)</span>")
scoreidecimal = Rule("<span class=\"decimal\">(.*?)</span>")

getsee = Rule("<span class=\"gray block alignct mt5 seen\">(.*?)</span>")
getwant = Rule("<span class=\"gray block alignct mt5 want\">(.*?)</span>")

langu = Rule("<span itemprop=\"inLanguage\">(.*?)</span>")
getA = Rule("lovebtn click_like mr10 lt\"(.*?)>")
TID = Rule("typeid=\"(.*?)\"")
resID = Rule("resid=\"(.*?)\"")
RWGXT = Rule("<ul class=\"descl\">(.*?)</ul>")
getLI = Rule("<li>(.*?)</li>")
getP = Rule("<p>(.*?)</p>")
getA2 = Rule(">(.*?)</a>")

#播出时间
plTIME = Rule("<p class=\"font16\">(.*?)</p>")
getTV = Rule("<ul class=\"tv_program_list\">(.*?)</ul>")
getTVname = Rule("<a.*?>(.*?)</a>")
getTVmain = Rule("<li class=\"program\">(.*?)</li>")
#评论
# getLI = Rule("<li class=\"material_comment\">")
getUser = Rule("<p class=\"c_n lt\">(.*?)</p>")
getcont = Rule("div class=\"c_c clear\"><p>(.*?)</p>")
pTime = Rule("<span class=\"font12 c_t \">(.*?)</span>")
relist = Rule("class=\"material_rep_ul\">(.*?)</ul>")
reli = Rule("<li class=\"material_rep_li\"(.*?)/li>")
reply = Rule("<span class=\"r_n\">(.*?)<\/span>")
reTime = Rule("<span class=\"rt r_t\">(.*?)</span>")
recont = Rule("<p class=\"r_c\">(.*?)</p>")
# 演员
actList = Rule("<ul class=\"act_list\">(.*?)</ul>")
act = Rule("<li.*?>(.*?)</li>")
actName = Rule("<p class=\"act_star\">(.*?)</p>")
actScore = Rule("<span class=\"acting_text\">(.*?)</span>")
aName = Rule("<p class=\"font16\">(.*?)</p>")
actSumm = Rule("<p class=\"hidden clear pt5\">(.*?)</p>")
aurl = Rule("<a href=\"(.*?)\"")
gaurl = Rule("href=\"(/star/.*?)\"")
am = Rule("")
# 剧集
pages = Rule("/movie/[A-Za-z]+/episode/[0-9]+-[0-9]+\"|/movie/[A-Za-z]+/episode/dajieju\"")
pages2 = Rule("/movie/[A-Za-z]+/episode/[0-9]+-[0-9]+\" title=\".*?</a>|/movie/[A-Za-z]+/episode/dajieju\" title=\".*?</a>")
pages3 = Rule("ul class=\"epi_sel\">(.*?)</ul>")
page4 = Rule("/movie/Y15layNg/chapter/.*?\"")
getH2 = Rule("<h2 class=\"font18\" style=\"padding:0 17px;\">(.*?)</h2>")
pTitle = Rule("<p class=\"d_e_t\">(.*?)</p>")
mainsumm = Rule("<div class=\"episode\">(.*?)class=\"epi_agree_div clear\"")
mainsumm2 = Rule("<div class=\"e_a_t clear\">.*?</div>(.*?)</div>")
putime = Rule("<p class=\"rt\">(.*?)</p>")
mainp = Rule("<p>(.*?)</p>")
pdate = Rule("pubDate\":\"(.*?)\"")
mainimg = Rule("\"images\":(.*?)],")
appid = Rule("\"appid\":\"(.*?)\"")