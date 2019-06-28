import requests,json,re,random,time
from pymongo import MongoClient
from bson import binary
from urllib import parse

def sleeps(a, b):
    t = random.randrange(a, b)
    time.sleep(t)

def save_data(data):
    conn = MongoClient(MONGO_HOST, MONGO_PORT)
    db = conn[MONGO_DB]
    my_set = db[MONGO_COLL]
    a = my_set.insert_one(data)
    print(a)
    conn.close()


def login_web():
    headers1 = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Host': "m.mmfintec.com",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    }
    headers = {
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        # "Connection":"keep-alive",
        "Host":"loan.mmfintec.com",
        "Referer":"http://loan.mmfintec.com/admin/login/?next=/credit/creditor_package_iframe",
        "Upgrade-Insecure-Requests":'1',
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    loginUrl = 'http://loan.mmfintec.com/admin/login/'
    s = requests.session()
    r = s.get("http://loan.mmfintec.com/admin/login/",headers=headers)
    rule = re.compile("csrfmiddlewaretoken\" value=\"(.*?)\"")
    # print(r.text)
    csrf = re.findall(rule,r.text)[0]
    user = {
        "csrfmiddlewaretoken":csrf,
        "username":"liuqiuxia",
        "password":'xinghe!@#',
        "this_is_the_login_form":'1',
        "next":"/admin/"
    }
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Origin'] = 'http://loan.mmfintec.com'
    a = s.post(loginUrl,data = user,headers=headers,cookies=r.cookies.get_dict(),allow_redirects=False)
    # headers['Cookie'] = a.cookies.get_dict()
    # s, response, header = login(loginUrl, 'http://loan.mmfintec.com/credit/query_package_info_by_fund_type', headers, user, s)
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Accept'] = "*/*"
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Referer'] = 'http://loan.mmfintec.com/credit/creditor_package_iframe'
    # headers['Content-Length'] = "20"
    try:
        resp = requests.post("http://loan.mmfintec.com/credit/query_package_info_by_fund_type",
                             data={"fundType": "liuwenliang"}, headers=headers, cookies=a.cookies.get_dict(),
                             allow_redirects=False)
    except:
        sleeps(20,50)
        resp = requests.post("http://loan.mmfintec.com/credit/query_package_info_by_fund_type",
                             data={"fundType": "liuwenliang"}, headers=headers, cookies=a.cookies.get_dict(),
                             allow_redirects=False)
    dic = json.loads(resp.text)
    package_list = dic.get('package_list',None)
    # 获取日期列表
    for idx,i in enumerate(package_list):
        key = i.get('package_start_date')
        # if int(key.replace("-",''))>20190108:
        # if int(key.replace("-", '')) > 20190104:
        #     continue
        # if idx == 0: continue
        sleeps(2, 5)

        print(key)
        package_id = i.get('package_id',None)
        fundType = i.get('fund_type',None)
        loan_day = i.get('loan_day')
        headers['Referer'] = 'http://loan.mmfintec.com/credit/creditor_package'
        # headers['Content-Length'] = '63'
        # 获取用户列表
        try:
            aa = requests.post("http://loan.mmfintec.com/credit/query_package_detail_by_package_id",
                               data={"fundType": fundType, "packageId": package_id}, headers=headers,
                               cookies=a.cookies.get_dict(), allow_redirects=False)
        except:
            sleeps(20,50)
            aa = requests.post("http://loan.mmfintec.com/credit/query_package_detail_by_package_id",
                               data={"fundType": fundType, "packageId": package_id}, headers=headers,
                               cookies=a.cookies.get_dict(), allow_redirects=False)
        userlist = json.loads(aa.text)
        if len(userlist)==0:
            continue
        ul = []
        for u in userlist:
            user_id = u.get('user_id')
            contractNO = u.get('contractNO')
            applyUserName = u.get('id_card_name')
            print(applyUserName)
            refundAmount = u.get('due_principal')
            loanPeriod = str(loan_day)
            loan_date = u.get('loan_date')
            repayment_date = u.get('due_date')
            due_amount = u.get('due_amount')
            idCardNo = u.get('id_card_number')
            accountName = u.get('accountName')
            accountBank = u.get('accountBank')
            accountNo = u.get('accountNo')
            # data = parse.quote("contractNO")
            # 身份证信息
            sleeps(1,3)
            try:
                headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
                headers['Upgrade-Insecure-Requests'] = '1'
                sf = requests.get("http://loan.mmfintec.com/credit/detail/{0}/".format(user_id), headers=headers,
                                  cookies=a.cookies.get_dict())
            except:
                sleeps(10,12)
                print("http://loan.mmfintec.com/credit/detail/{0}/".format(user_id))
                sf = requests.get("http://loan.mmfintec.com/credit/detail/{0}/".format(user_id), headers=headers,
                                  cookies=a.cookies.get_dict())
            sleeps(5,8)
            # 协议信息
            di = dict(
                contractNO=contractNO,applyUserName=applyUserName,refundAmount=refundAmount,
                loanPeriod=loanPeriod,loan_date=loan_date,repayment_date=repayment_date,due_amount=due_amount,
                idCardNo=idCardNo,accountName=accountName,accountBank=accountBank,accountNo=accountNo
            )

            # del headers['Content-Type']
            # data = json.dumps({parse.quote(k):parse.quote(v) for k,v in di.items()})
            # data = json.dumps({parse.quote('"' + k + '"'):parse.quote('"' + v + '"') for k,v in di.items()}).replace(' ','')
            data = parse.quote(json.dumps(di).replace(' ','')).replace("%3A",':').replace('%7B','{').replace('%7D','}')
            uul = "http://m.mmfintec.com/agreement/instant/loan_agreement_remain.html?data={0}".format(data)
            try:
                xieyi = requests.get(uul, headers=headers1)
            except:
                sleeps(20,50)
                xieyi = requests.get(uul, headers=headers1)
            u['xieyi'] = xieyi.content.decode("utf8")
            u['homepage'] = sf.text
            rule1 = re.compile("img src=(.*?)/>",re.S)
            ps = re.findall(rule1,sf.text)
            ps = [p.replace(' ','').replace('amp;','') for p in ps]
            card = []
            for idxx,pp in enumerate(ps):
                try:
                    rs = requests.get(pp)
                except:
                    sleeps(20,50)
                    rs = requests.get(pp)
                data = binary.Binary(rs.content)
                card.append(data)
                # with open('C:\\Users\\HP\\Desktop\\身份证\\{0}{1}.jpg'.format(applyUserName,idxx), 'ab') as f:
                #     f.write(rs.content)
            u['img'] = ps
            u['cards'] = card
            ul.append(u)

        i['userList'] = ul
        save_data(i)



if __name__ == '__main__':
    # MongoDB设置
    MONGO_HOST = "127.0.0.1"  # 主机IP
    MONGO_PORT = 27017  # 端口号
    MONGO_DB = "MONGO_DB"  # 库名
    MONGO_COLL = "mmfintec2"  # collection名
    login_web()