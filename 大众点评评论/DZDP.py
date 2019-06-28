import requests
from pymongo import MongoClient
import time
import json
import random
import re
from hanzi import get_xy

# -------------------------修改这部分就可以解决大众点评反爬问题-----------------------------#
# li里的内容，是svg文件中，每一行文字的内容和此行的高度值
li = [["美量务饭足姐般费子理好楼比热意上度试微当于又豆", 36],
      ["牛进要不菜也算配其烤合东直方拍起位吧欢路分店前感之家们元作底排对包第粉刚桌成里", 58],
      ["且棒动开境食烧单格汤装做重因跟场外同火评几自行海新可性提业置", 89],
      ["哈看那生常心挺能最板打午间态他十特得鱼老么和色什级干虾选料清", 117],
      ["会定份你每年甜餐错找鸡串实次高种回适友地一队师车等然更让接", 139],
      ["是所走无五来口带下就啊个说体买真非风喜情酸", 177],
      ["快茶肉这多着手三环晚赞边在了强辣品全很出门超红大天鲜中别入果才号日", 207],
      ["像朋酒服去区候米调放后近小整以有员嫩气太经觉蛋爱如给主式少人想价味二皮较尝面", 242],
      ["而内还喝啦满水点修为头时我两己锅酱花些便但客块正发奶周推", 277],
      ["过荐笑儿加用西差的糕只完值本现总话片吃牌油香再都到样没知", 309]]
# ------------------------------------------------------------------------------------#
def get_css():
    with open("hehe", "r", encoding="utf-8") as f:
        css = f.read()
    return css

csfile = get_css()
rulecss = re.compile("px -([0-9]+).0",re.S)

# index是css文件中，取出所有的y值里最小的一个
indexs = re.findall(rulecss,csfile)
index = sorted([int(i) for i in indexs])[0]


rule = re.compile("roundlv([0-9]+)\.")
rule2 = re.compile("feedScoreList\":(\[.*?\]),")
rule3 = re.compile("<span class=\"([a-zA-Z0-9]+)\"></span>", re.S)
redic = get_xy(li, inde=index)





def sleeps(a, b):
    t = random.randrange(a, b)
    time.sleep(t)


def save_data(data):
    conn = MongoClient(MONGO_HOST, MONGO_PORT)
    db = conn.MONGO_DB
    my_set = db.MONGO_COLL
    my_set.insert_one(data)
    conn.close()


def get_review(url):
    sleeps(1, 2)
    response = requests.get(url=url, headers=headers2, allow_redirects=False)
    # print(response.text)
    li = re.findall(rule2, response.text)
    return li if len(li) != 0 else ''


def get_hanzi(xy):
    # {background:-518.0px -109.0px
    rule1 = re.compile(":-([0-9]+)\.0")
    rule2 = re.compile("px -([0-9]+)\.0")
    x = re.findall(rule1, xy)[0]
    y = re.findall(rule2, xy)[0]
    zi = redic[int(y)][int(x)]
    print("解析成功")
    return zi


def parser_data(data):
    """
    破解
    :param data:
    :return:
    """
    result = re.findall(rule3, data)
    for i in result:
        s = "\.{0}(.*?);".format(i)  # {background:-[0-9]+.0px -[0-9]+.0px;}
        # s = "\.{0}(.*?);".format('waxaiu')
        rule = re.compile(s, re.S)
        css = get_css()
        xy = re.findall(rule, css)[0]
        zi = get_hanzi(xy)
        strOle = "<span class=\"{0}\"></span>".format(i)
        data = data.replace(strOle, zi)
    return data


def get_reviewList(l):
    for i in l:
        reviewId = i.get("reviewId")
        userNickName = i.get("userNickName")  # 昵称
        userLevelImg = i.get("userLevelImg")  # 等级图片
        le = re.findall(rule, userLevelImg)
        level = le[0] if len(le) != 0 else ''
        vipLevel = i.get("vipLevel")
        star = i.get('star')  # 用户评价星数【浮点数】
        scoreInfo = get_review("https://m.dianping.com/review/{0}".format(reviewId))  # 打分信息
        reviewBody = i.get("reviewBody")
        if reviewBody.find("<span class=\"") >= 0:
            reviewBody = parser_data(reviewBody)
        flowerTotal = i.get('flowerTotal')
        followNoteNo = i.get('followNoteNo')
        reviewPicNum = i.get("reviewPicNum", 0)
        reviewPics = i.get('reviewPics', [])
        picUrl = []
        for pic in reviewPics:
            picUrl.append(pic.get("bigurl"))
        times = i.get("lastTimeStr")
        addTime = i.get("addTime")
        yield dict(userNickName=userNickName,
                   level=level,
                   vipLevel=vipLevel,
                   star=star,
                   scoreInfo=scoreInfo,
                   reviewBody=reviewBody,
                   flowerTotal=flowerTotal,
                   followNoteNo=followNoteNo,
                   reviewPicNum=reviewPicNum,
                   picUrl=picUrl,
                   time=times,
                   addTime=addTime, content=i
                   )


def pages(shopId):
    payload = {
        "moduleInfoList": [{
            "moduleName": "reviewlist",
            "query": {
                "shopId": shopId,
                "offset": 0,
                "limit": 10,
                "type": 1,
                "pageDomain": "m.dianping.com"
            }
        }],
        "pageEnName": "shopreviewlist"
    }
    while True:
        print("准备采集第", payload['moduleInfoList'][0]["query"]["offset"] / 10, "页")
        result = request(payload)
        if result is True:
            payload['moduleInfoList'][0]["query"]["offset"] += 10
            # break
        else:
            print("采集结束……")
            break


def request(payload):
    url = "https://m.dianping.com/isoapi/module"
    sleeps(1, 5)
    response = requests.get(url=url, data=json.dumps(payload), headers=headers)
    # print(response.text)
    js = json.loads(response.text)
    msg = js.get('msg', None)
    if msg is not None and msg == 'success':
        data = js.get("data")
        shopId = data.get("shopId")  # shopId
        moduleInfoList = data.get('moduleInfoList')
        if len(moduleInfoList) != 0:
            moduleData = moduleInfoList[0].get('moduleData')
            nmsg = moduleData.get('msg', None)
            if nmsg is not None and nmsg == 'success':
                dataNew = moduleData.get("data")
                reviewList = dataNew.get("reviewList", None)
                hasNextPage = dataNew.get("hasNextPage")
                totalCount = dataNew.get("totalCount")
                print("共", totalCount, "条评论")
                if reviewList is not None and len(reviewList) != 0:
                    for i in get_reviewList(reviewList):
                        # save_data(i)  # 保存
                        print(i)
                    return hasNextPage
                else:
                    print("评论列表为空……")
                    pass  # 空的评论列表
            else:
                print(nmsg)
                print("访问出错")
    else:
        print(msg)
        print("访问出错")


def get_headers(shopId):
    # 外层headers
    headers = {
        'Host': 'm.dianping.com',
        "Content-Type": "application/json",
        'Connection': 'keep-alive',
        "Origin": "https://m.dianping.com",
        'Accept': '*/*',
        "Referer": "https://m.dianping.com/shop/{0}/review_all".format(shopId),
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
        "Cookie": '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=1696109459ec8-0825a29e12f0bb-38395f03-144000-1696109459fc8; _lxsdk=1696109459ec8-0825a29e12f0bb-38395f03-144000-1696109459fc8; _hc.v=7523e441-f374-1c86-3ed8-f92569ad4c72.1552111192; s_ViewType=10; cy=2; cye=beijing; cityid=10; msource=default; default_ab=shop%3AA%3A1%7Cshopreviewlist%3AA%3A1; logan_custom_report=; thirdtoken=c356ef6d-4906-42ac-b201-89793f979457; dper=b794b566d9c95219abb3b3a09864964f7ff32266f5d78836c97d2e75b6caae023c9a8a1c081176ddc585e83fa8a4ef0ec3b1d6db94e2279362c0dfbea13d30fefac77eb458a13e1dd0ea36ca4522b08896658391524b2d275cf34191ad48c17c; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_4057558397; ctu=90932168949cd4657531c5f87c835a83d90d1eb24bc09999ca256d896aaf43e4; logan_session_token=l27jlyt6r361w3o71epj; _lxsdk_s=169619829db-e29-591-add%7C0%7C6; dp_pwa_v_=4918b24041ad5907d9fbe068bd4425432fb2c8c9'
    }
    # 详情headers
    headers2 = {
        'Host': 'm.dianping.com',
        "Content-Type": "application/json",
        "Upgrade-Insecure-Requests": "1",
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        "Referer": "https://m.dianping.com/shop/{0}/review_all".format(shopId),
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
        "Cookie": '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=1696109459ec8-0825a29e12f0bb-38395f03-144000-1696109459fc8; _lxsdk=1696109459ec8-0825a29e12f0bb-38395f03-144000-1696109459fc8; _hc.v=7523e441-f374-1c86-3ed8-f92569ad4c72.1552111192; s_ViewType=10; cy=2; cye=beijing; cityid=10; msource=default; default_ab=shop%3AA%3A1%7Cshopreviewlist%3AA%3A1; logan_custom_report=; thirdtoken=c356ef6d-4906-42ac-b201-89793f979457; dper=b794b566d9c95219abb3b3a09864964f7ff32266f5d78836c97d2e75b6caae023c9a8a1c081176ddc585e83fa8a4ef0ec3b1d6db94e2279362c0dfbea13d30fefac77eb458a13e1dd0ea36ca4522b08896658391524b2d275cf34191ad48c17c; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_4057558397; ctu=90932168949cd4657531c5f87c835a83d90d1eb24bc09999ca256d896aaf43e4; logan_session_token=l27jlyt6r361w3o71epj; _lxsdk_s=169619829db-e29-591-add%7C0%7C6; dp_pwa_v_=4918b24041ad5907d9fbe068bd4425432fb2c8c9'
    }
    return headers, headers2


if __name__ == '__main__':

    # MongoDB设置
    MONGO_HOST = "127.0.0.1"  # 主机IP
    MONGO_PORT = 27017  # 端口号
    MONGO_DB = "DZdianpingNew"  # 库名
    MONGO_COLL = "shopReviewNew"  # collection名
    with open("shopId.txt", "r", encoding="utf-8") as f:
        result = f.readlines()
        for shopId in result:
            headers, headers2 = get_headers(shopId.replace("\n", '').replace(" ", ''))
            print("开始采集", shopId)
            pages(shopId)
