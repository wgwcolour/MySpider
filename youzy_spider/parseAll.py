from lxml import etree
from pymongo import MongoClient

import sys
from subprocess import Popen, PIPE
from sqlalchemy import create_engine, text
import json, queue, copy, re
import threading, queue

# MongoDB设置
MONGO_HOST = "127.0.0.1"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "youzySpider"  # 库名


sqlserver = "mssql+pymssql://sa:wgwqqq@127.0.0.1/yzy?charset=utf8"
Engine = create_engine(sqlserver)


def getdata(q,table):
    while True:
        try:
            data = q.get_nowait()
            size = q.qsize()
            print("计数：{0} {1}".format(size,table))
            yield data
        except:
            break


def getHTML(lmt, s, conn, MONGO_DB, MONGO_COLL, par=None):
    par = {} if par is None else par

    db = conn[MONGO_DB]
    tb = db[MONGO_COLL]
    datas = tb.find(par).limit(lmt).skip(s)
    for i in datas:
        yield i


def dataQueue(lmt, s, conn, MONGO_DB, MONGO_COLL, par=None):
    q = queue.Queue()
    for i in getHTML(lmt, s, conn, MONGO_DB, MONGO_COLL, par):
        q.put(i)
    return q


def exethread(func, *args, threadNum=1):
    threads = []
    for i in range(0, threadNum):
        t = threading.Thread(target=func, args=args)  # get_r是多线程要操作的函数，args里是get_r需要的参数
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        # 多线程多join的情况下，依次执行各线程的join方法, 这样可以确保主线程最后退出， 且各个线程间没有阻塞
        t.join()


# 执行sql语句
def exsql(engine, sql, select=True, pars=None, echo=True):
    """
    exsql 执行sql语句，返回结果
    :param sql:sql语句或者sql语句列表
    :param pars:对应的sql语句需要的参数
    :return:
    """
    pars = {} if pars is None else pars
    connect = engine.connect()
    T = True
    if select:
        result = connect.execute(text(sql), pars)
        r = result.fetchall()
        connect.close()
        return r, T
    else:
        r = True
        trans = connect.begin()
        try:
            if isinstance(sql, list) is True:
                for idx, s in enumerate(sql):
                    connect.execute(text(s), pars[idx])
            else:
                connect.execute(text(sql), pars)
            trans.commit()
            if echo is True:
                print("执行成功")
        except Exception as e:
            print(e, sql)
            r = False
            trans.rollback()
        finally:
            connect.close()
        return '', r


rule2 = re.compile("&#x(.*?);")
# cn_5字体
code = ['B0CF', 'B27A', 'B305', 'B36E', 'B370', 'B3A2', 'B3CA', 'B425', 'B47D', 'B538', 'B6F2', 'B70D', 'B73A', 'B883',
        'B8B0', 'B8C1', 'B8DE', 'B8DF', 'B907', 'B90D', 'BA7A', 'BB66', 'BBBE', 'BC34', 'BC45', 'BCB9', 'BD0B', 'BD4B',
        'BEBD', 'BEDF', 'BEF6', 'BF6F', 'BF7B', 'BF8E', 'C620', 'C621', 'C622', 'C623', 'C624', 'C625', 'C626', 'C627',
        'C628', 'C629', 'C62A', 'C62B', 'C62C', 'C62D', 'C62E', 'C62F', 'C630', 'C631', 'C632', 'C633', 'C634', 'C635',
        'C636', 'C637', 'C638', 'C639', 'C63A', 'C63B', 'C63C', 'C63D', 'C63E', 'C63F', 'C640', 'C641', 'C642', 'C643',
        'C644', 'C645', 'C646', 'C647', 'C648', 'C649', 'C64A', 'C64B', 'C64C', 'C64D', 'C64E', 'C64F', 'C650', 'C651',
        'C652', 'C653', 'C654', 'C655', 'C656', 'C657', 'C658', 'C659', 'C65A', 'C65B', 'C65C', 'C65D', 'C65E', 'C65F',
        'C660', 'C661', 'C662', 'C663', 'C664', 'C665', 'C666', 'C667', 'C668', 'C669', 'C66A', 'C66B', 'C66C', 'C66D',
        'C66E', 'C66F', 'C670', 'C671', 'C672', 'C673', 'C674', 'C675', 'C676', 'C677', 'C678', 'C679', 'C67A', 'C67B',
        'C67C', 'C67D', 'C67E', 'C67F', 'C680', 'C681', 'C682', 'C683', 'C684', 'C685', 'C686', 'C687', 'C688', 'C689',
        'C68A', 'C68B', 'C68C', 'C68D', 'C68E', 'C68F', 'C690', 'C691', 'C692', 'C693', 'C694', 'C695', 'C696', 'C697',
        'C698', 'C699', 'C69A', 'C69B', 'C69C', 'C69D', 'C69E', 'C69F', 'C6A0', 'C6A1', 'C6A2', 'C6A3', 'C6A4', 'C6A5',
        'C6A6', 'C6A7', 'C6A8', 'C6A9', 'C6AA', 'C6AB', 'C6AC', 'C6AD', 'C6AE', 'C6AF', 'C6B0', 'C6B1', 'C6B2', 'C6B3',
        'C6B4', 'C6B5', 'C6B6', 'C6B7', 'C6B8', 'C6B9', 'C6BA', 'C6BB', 'C6BC', 'C6BD', 'C6BE', 'C6BF', 'C6C0', 'C6C1',
        'C6C2', 'C6C3', 'C6C4', 'C6C5', 'C6C6', 'C6C7', 'C6C8', 'C6C9', 'C6CA', 'C6CB', 'C6CC', 'C6CD', 'C6CE', 'C6CF',
        'C6D0', 'C6D1', 'C6D2', 'C6D3', 'C6D4', 'C6D5', 'C6D6', 'C6D7', 'C6D8', 'C6D9', 'C6DA', 'C6DB', 'C6DC', 'C6DD',
        'C6DE', 'C6DF', 'C6E0', 'C6E1', 'C6E2', 'C6E3', 'C6E4', 'C6E5', 'C6E6', 'C6E7', 'C6E8', 'C6E9', 'C6EA', 'C6EB',
        'C6EC', 'C6ED', 'C6EE', 'C6EF', 'C6F0', 'C6F1', 'C6F2', 'C6F3', 'C6F4', 'C6F5', 'C6F6', 'C6F7', 'C6F8', 'C6F9',
        'C6FA', 'C6FB', 'C6FC', 'C6FD', 'C6FE', 'C6FF', 'C700', 'C701', 'C702', 'C703', 'C704', 'C705', 'C706', 'C707',
        'C708', 'C709', 'C70A', 'C70B', 'C70C', 'C70D', 'C70E', 'C70F', 'C710', 'C711', 'C712', 'C713', 'C714', 'C715',
        'C716', 'C717', 'C718', 'C719', 'C71A', 'C71B', 'C71C', 'C71D', 'C71E', 'C71F', 'C720', 'C721', 'C722', 'C723',
        'C724', 'C725', 'C726', 'C727', 'C728', 'C729', 'C72A', 'C72B', 'C72C', 'C72D', 'C72E', 'C72F', 'C730', 'C731',
        'C732', 'C733', 'C734', 'C735', 'C736', 'C737', 'C738', 'C739', 'C73A', 'C73B', 'C73C', 'C73D', 'C73E', 'C73F',
        'C740', 'C741', 'C742', 'C743', 'C744', 'C745', 'C746', 'C747', 'C748', 'C749', 'C74A', 'C74B', 'C74C', 'C74D',
        'C74E', 'C74F', 'B8C', '5386']
word = ['像', '艺', '包', '据', '印', '探', '及', '营', '命', '历', '曲', '服', '机', '境', '械', '磁', '飞', '食', '备', '植', '空', '武',
        '设', '水', '居', '油', '洋', '测', '纽', '统', '件', '软', '轻', '美', '丁', '下', '与', '世', '业', '丝', '中', '主', '义', '乌',
        '书', '事', '互', '交', '产', '人', '仪', '价', '休', '会', '伤', '伦', '估', '体', '作', '供', '侦', '俄', '保', '信', '修', '健',
        '儿', '光', '克', '党', '全', '公', '共', '关', '兵', '其', '军', '农', '准', '减', '出', '分', '划', '则', '别', '制', '刷', '力',
        '功', '加', '务', '动', '助', '劳', '化', '医', '华', '卫', '发', '古', '史', '司', '合', '告', '品', '商', '回', '国', '土', '地',
        '型', '培', '声', '大', '天', '女', '媒', '子', '学', '安', '定', '宝', '实', '审', '室', '家', '宾', '密', '小', '少', '尔', '展',
        '属', '嵌', '工', '市', '师', '广', '应', '康', '建', '开', '录', '形', '影', '律', '微', '德', '心', '情', '想', '感', '成', '战',
        '房', '技', '投', '护', '报', '拉', '控', '推', '播', '收', '放', '政', '教', '数', '文', '料', '斯', '无', '日', '时', '景', '智',
        '术', '材', '村', '来', '查', '正', '民', '气', '污', '河', '治', '法', '泰', '海', '源', '灾', '炸', '然', '照', '爆', '版', '物',
        '环', '班', '理', '生', '用', '画', '界', '疗', '监', '知', '石', '研', '种', '科', '秘', '移', '程', '税', '立', '筑', '算', '管',
        '类', '精', '纺', '组', '织', '经', '网', '职', '育', '能', '自', '航', '船', '英', '草', '萄', '葡', '行', '表', '装', '观', '规',
        '视', '计', '论', '评', '识', '译', '试', '语', '财', '质', '资', '路', '车', '轨', '轮', '运', '通', '造', '采', '量', '金', '鉴',
        '间', '非', '韩', '项', '预', '饰', '馆', '验', '高', '麻', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '磁', '历']
# 字体文件
zt = {"6F732": 6, "72EF1": 9, "7D3AE": 2, "A8F2E": 0, "AA86E": 7, "C15F9": 1, "C2E7A": 4, "E7F11": 5, "F8B41": 3,
      "FC6A6": 8}


# mongodb保存数据
def mongo_save_data(tb, content):
    conn = MongoClient("mongodb://{MONGO_HOST}:{MONGO_PORT}/".format(MONGO_HOST=MONGO_HOST, MONGO_PORT=MONGO_PORT))
    # conn.admin.authenticate("root5", "TJRWKJ", mechanism='SCRAM-SHA-1')
    db = conn[MONGO_DB]
    my_set = db[tb]
    my_set.insert_one(content)
    print('执行成功')
    conn.close()


lmt = 5000
threadNum = 8


def fuckdata(data):#获取文字
    try:
        while data:
            s = re.search(rule2, data)
            if not s:
                break
            a = word[code.index(s.group(1).upper())]
            data = re.sub(rule2, a, data, count=1)
    except:
        pass
    finally:
        return data


def fuckNum(i):# 获取数字
    if i != '0':
        nums = re.findall(rule2, i)
        score = ''
        for n in nums:
            score += str(zt[n.upper()])
    else:
        score = 0
    return score


def showNumbers(scores):# 解析css数字
    if scores == 0:
        return '0'
    try:
        process = Popen(['node', 'fuck.js', scores], stdout=PIPE, stderr=PIPE)
    except (OSError, IOError) as err:
        print('请先安装 node.js: https://nodejs.org/')
        sys.exit()
    scoreData = process.communicate()[0].decode().strip('\n').strip('\r').split(',')
    return scoreData[0]


def showWords(st):# 解析css字体
    try:
        process = Popen(['node', 'showWords.js', st[0:len(st) - 1]], stdout=PIPE, stderr=PIPE)
    except (OSError, IOError) as err:
        print('请先安装 node.js: https://nodejs.org/')
        sys.exit()
    data = process.communicate()[0].decode().strip('\n').strip('\r')
    return data


def parseSchoolScoreLine(q, table):
    for data in getdata(q, table):
        # sqlList = []
        # pars = []
        # gid = str(data.get('_id'))
        # schoolsortNo = data['schoolSortNo']
        # courseType = data['course']
        # schoolId = data['collegeId']
        # school = data['collegeName']# 招生名称
        # yzyschool = data['school'] #【专业招生对比数据】这里有个bug，就是“yzyschool”是学校名称，而不是招生名称
        provinceName = data['provinceName']
        # Id = data.get('id')

        # AdmissCode = data.get('admissCode')
        ProvinceId = data.get('provinceId')
        # ProvinceName = data.get('provinceName')
        sqlList = []
        pars = []
        gid = str(data.get('_id'))
        schoolsortNo = data['schoolSortNo']
        courseType = data['course']

        schoolId = data['collegeId']
        school = data['school']
        yzyschool = data['collegeName']
        province = data['provinceName']
        AdmissCode = data.get('admissCode')
        CollegeId = data.get('collegeId')
        IsHome = data.get('IsHome')
        CollegeName = data.get('collegeName')
        Sort = data.get('sort')
        IsOld = data.get('isOld')
        UCodeId = ''
        UCode = data.get('uCodeNum')
        CodeChangeYear = data.get('codeChangeYear')
        par = dict(gid=gid, CollegeId=CollegeId, ProvinceName=provinceName, ProvinceId=ProvinceId,
                   CodeChangeYear=CodeChangeYear, UCode=UCode, Sort=Sort, UCodeId=UCodeId, IsOld=IsOld, IsHome=IsHome,
                   CollegeName=CollegeName, schoolsortNo=schoolsortNo, courseType=courseType, schoolId=schoolId,
                   school=school,
                   yzyschool=yzyschool, province=province, AdmissCode=AdmissCode)
        result = data.get('result', {}).get('result')
        if result and len(result) > 0:
            for idx, D in enumerate(result):
                par2 = copy.copy(par)
                par2['Year'] = D.get('year')

                Course = D['course']
                Batch = D['batch']
                BatchName = D['batchName']
                MaxScore = D['maxScore']
                MinScore = D['minScore']
                AvgScore = D['avgScore']
                LowSort = D['lowSort']
                MaxSort = D['maxSort']
                EnterNum = D['enterNum']
                ChooseLevel = D['chooseLevel']
                IsCollected = ''
                LineDiff = D['lineDiff']
                Id = ''
                Id1 = ''
                sortNo = idx
                par2['Course'] = Course
                par2['Batch'] = Batch
                par2['BatchName'] = BatchName
                par2['MaxScore'] = fuckNum(showNumbers(MaxScore)) if not isinstance(MaxScore, int) else MaxScore
                par2['MinScore'] = fuckNum(showNumbers(MinScore)) if not isinstance(MinScore, int) else MinScore
                par2['AvgScore'] = fuckNum(showNumbers(AvgScore)) if not isinstance(AvgScore, int) else AvgScore
                par2['LowSort'] = fuckNum(showNumbers(LowSort)) if not isinstance(LowSort, int) else LowSort
                par2['MaxSort'] = fuckNum(showNumbers(MaxSort)) if not isinstance(MaxSort, int) else MaxSort
                par2['EnterNum'] = fuckNum(showNumbers(EnterNum)) if not isinstance(EnterNum, int) else EnterNum
                par2['IsCollected'] = IsCollected
                par2['ChooseLevel'] = ChooseLevel
                par2['LineDiff'] = LineDiff
                par2['Id'] = Id
                par2['Id1'] = Id1
                par2['sortNo'] = sortNo
                par2['UCodeNum'] = D.get('uCode')

                pars.append(par2)
                sql = "insert into 学校分数_2 (gid,yzyschool,school,schoolId,Year,province,UCodeNum,AdmissCode,ProvinceId,ProvinceName,CollegeId,CollegeName,IsHome,Sort,IsOld,CodeChangeYear,schoolsortNo,UCodeId,UCode,Course,Batch,BatchName,MaxScore,MinScore,AvgScore,LowSort,MaxSort,EnterNum,ChooseLevel,IsCollected,LineDiff,Id,Id1,sortNo) values(:gid,:yzyschool,:school,:schoolId,:Year,:province,:UCodeNum,:AdmissCode,:ProvinceId,:ProvinceName,:CollegeId,:CollegeName,:IsHome,:Sort,:IsOld,:CodeChangeYear,:schoolsortNo,:UCodeId,:UCode,:Course,:Batch,:BatchName,:MaxScore,:MinScore,:AvgScore,:LowSort,:MaxSort,:EnterNum,:ChooseLevel,:IsCollected,:LineDiff,:Id,:Id1,:sortNo)"
                sqlList.append(sql)

            exsql(Engine, sqlList, select=False, pars=pars)


def parseMajorComparedData(q,table):
    for data in getdata(q, table):
        sqlList = []
        pars = []
        gid = str(data.get('_id'))
        schoolsortNo = data['schoolSortNo']
        courseType = data['course']
        schoolId = data['collegeId']
        school = data['collegeName']  # 招生名称
        yzyschool = data['school']  # 【专业招生对比数据】这里有个bug，就是“yzyschool”是学校名称，而不是招生名称
        province = data['provinceName']
        Id = data.get('id')
        UCodeNum = data.get('uCodeNum')
        AdmissCode = data.get('admissCode')
        ProvinceId = data.get('provinceId')
        ProvinceName = data.get('provinceName')
        CollegeId = data.get('collegeId')
        IsHome = data.get('IsHome')
        CollegeName = data.get('collegeName')
        Sort = data.get('sort')
        IsOld = data.get('isOld')
        CodeChangeYear = data.get('codeChangeYear')
        pid = 'pid'
        par = dict(gid=gid, pid=pid, schoolsortNo=schoolsortNo, CodeChangeYear=CodeChangeYear, courseType=courseType,
                   schoolId=schoolId, school=school,
                   yzyschool=yzyschool, province=province, UCodeNum=UCodeNum, AdmissCode=AdmissCode,
                   ProvinceId=ProvinceId, IsHome=IsHome, IsOld=IsOld, Sort=Sort, ProvinceName=ProvinceName,
                   CollegeId=CollegeId, CollegeName=CollegeName, Course=courseType, Id=Id)

        Batch = data['batch']
        BatchName = data['batchName']
        scoreResult = data['result'].get('result')
        for idxx, score in enumerate(scoreResult):
            p2 = {}
            sortNo = idxx
            OriBatch = score.get('oriBatch')
            UCodeId = score.get('uCodeId')
            UCode = score.get('uCode')
            ProfessionName = fuckdata(showWords(score.get('professionName')))
            MajorCode = score.get('majorCode')
            Code = fuckdata(showWords(score.get('code')))
            PlanNum = fuckNum(showNumbers(score.get('planNum')))
            EnterHisJsonList = json.dumps(score.get('enterHisJsonList'))
            IncOrDec = score.get('incOrDec')
            Cost = fuckdata(showWords(score.get('cost')))
            LearnYear = fuckdata(showWords(score.get('learnYear')))
            Remark = score.get('remark')
            LowSort = score.get('lowSort')
            CountOfZJZY = score.get('countOfZJZY')
            Id1 = score.get('id')
            p2.update(sortNo=sortNo, Batch=Batch, BatchName=BatchName, OriBatch=OriBatch, UCodeId=UCodeId,
                      UCode=UCode, ProfessionName=ProfessionName, MajorCode=MajorCode, Code=Code,
                      PlanNum=PlanNum, EnterHisJsonList='暂无', IncOrDec=IncOrDec, Cost=Cost, LearnYear=LearnYear,
                      Remark=Remark, LowSort=LowSort, CountOfZJZY=CountOfZJZY, Id1=Id1)
            ens = json.loads(score.get('enterHisJsonList'))
            nums17, nums16, nums15 = '', '', '',
            min_score17, min_score16, min_score15 = '', '', ''
            weici17, weici16, weici15 = '', '', ''
            for ye, da in enumerate(ens):
                if ye == 0:
                    nums17 = fuckNum(showNumbers(da.get('eu'))) if not isinstance(da.get('eu'), int) else da.get('eu')
                    min_score17 = fuckNum(showNumbers(da.get('ms'))) if not isinstance(da.get('ms'), int) else da.get(
                        'ms')
                    weici17 = fuckNum(showNumbers(da.get('ls'))) if not isinstance(da.get('ls'), int) else da.get('ls')
                elif ye == 1:
                    nums16 = fuckNum(showNumbers(da.get('eu'))) if not isinstance(da.get('eu'), int) else da.get('eu')
                    min_score16 = fuckNum(showNumbers(da.get('ms'))) if not isinstance(da.get('ms'), int) else da.get(
                        'ms')
                    weici16 = fuckNum(showNumbers(da.get('ls'))) if not isinstance(da.get('ls'), int) else da.get('ls')
                elif ye == 2:
                    nums15 = fuckNum(showNumbers(da.get('eu'))) if not isinstance(da.get('eu'), int) else da.get('eu')
                    min_score15 = fuckNum(showNumbers(da.get('ms'))) if not isinstance(da.get('ms'), int) else da.get(
                        'ms')
                    weici15 = fuckNum(showNumbers(da.get('ls'))) if not isinstance(da.get('ls'), int) else da.get('ls')
            p2.update(nums17=nums17, minscore17=min_score17, weici17=weici17,
                      nums16=nums16, minscore16=min_score16, weici16=weici16,
                      nums15=nums15, minscore15=min_score15, weici15=weici15)

            pp = copy.copy(par)
            pp.update(p2)
            pars.append(pp)
            sql = "insert into 专业招生对比数据_1 (gid,pid,yzyschool,school,schoolId,province,UCodeNum,AdmissCode,ProvinceId,ProvinceName,CollegeId,CollegeName,IsHome,Sort,IsOld,CodeChangeYear,schoolsortNo,UCodeId,UCode,Course,Batch,BatchName,ProfessionName,MajorCode,Code,PlanNum,EnterHisJsonList,IncOrDec,Cost,LearnYear,Remark,LowSort,CountOfZJZY,OriBatch,nums17,minscore17,weici17,nums16,minscore16,weici16,nums15,minscore15,weici15,Id,Id1,sortNo) values(:gid,:pid,:yzyschool,:school,:schoolId,:province,:UCodeNum,:AdmissCode,:ProvinceId,:ProvinceName,:CollegeId,:CollegeName,:IsHome,:Sort,:IsOld,:CodeChangeYear,:schoolsortNo,:UCodeId,:UCode,:Course,:Batch,:BatchName,:ProfessionName,:MajorCode,:Code,:PlanNum,:EnterHisJsonList,:IncOrDec,:Cost,:LearnYear,:Remark,:LowSort,:CountOfZJZY,:OriBatch,:nums17,:minscore17,:weici17,:nums16,:minscore16,:weici16,:nums15,:minscore15,:weici15,:Id,:Id1,:sortNo)"
            sqlList.append(sql)
            if len(sqlList) > 100 or (idxx + 1) == len(scoreResult):
                exsql(Engine, sqlList, select=False, pars=pars)
                sqlList = []
                pars = []


def parseMajorScoreLine(q,table):
    for data in getdata(q, table):
        sqlist, pars = [], []
        school = data.get('school')
        ucode = data.get('uCodeNum')
        province = data.get('provinceName')
        zsname = data.get('collegeName')
        schoolsortNo = data.get('schoolSortNo')
        gid = str(data.get('_id'))
        wl = '理工' if data.get('course') == 0 else '文史'
        result = data.get('result', {}).get('result')
        for idx, i in enumerate(result):
            year = i.get('year')
            batch = i.get('batchName')
            majorcode = fuckdata(showWords(i.get('professionCode')))
            major = fuckdata(showWords(i.get('professionName')))  ######
            maxscore = fuckNum(showNumbers(i.get('maxScore')))  ######
            minscore = fuckNum(showNumbers(i.get('minScore')))  ######
            avgscore = fuckNum(showNumbers(i.get('avgScore')))  ######
            minwc = fuckNum(showNumbers(i.get('lowSort')))  ######
            luqu = fuckNum(showNumbers(i.get('enterNum')))  ######
            sql = "insert into 专业历年招生_1 (gid,文理,ucode,年份,省份,学校,招生名称,专业招生代码,专业名称,招生批次,最高分,最低分,平均分,最低位次,录取数,sortNo,schoolsortNo)values(:gid,:wl,:ucode,:year,:province,:school,:zsname,:majorcode,:major,:batch,:maxscore,:minscore,:avgscore,:minwc,:luqu,:sortNo,:schoolsortNo)"
            sqlist.append(sql)
            pars.append(dict(school=school, gid=gid, wl=wl, ucode=ucode, year=year, province=province, zsname=zsname,
                             majorcode=majorcode,
                             major=major, batch=batch, maxscore=maxscore, minscore=minscore,
                             avgscore=avgscore, minwc=minwc, luqu=luqu, sortNo=idx, schoolsortNo=schoolsortNo))

        if sqlist:
            exsql(Engine, sqlist, select=False, pars=pars)


def parsePlan2019(q,table):
    for data in getdata(q,table):
        sqlist, pars = [], []
        gid = str(data.get('_id'))
        scode = data.get('admissCode')
        yzyid = data.get('schoolId')
        school = data.get('school')
        zsname = data.get('collegeName')
        ucode = data.get('uCodeNum')
        province = data.get('provinceName')
        schoolsortNo = data.get('schoolSortNo')
        result = data.get('result', {}).get('result', {})
        liKePlans = result.get('liKePlans', {}).get('plansBatch', [])
        wenKePlans = result.get('wenKePlans', {}).get('plansBatch', [])
        rt = {"理科": liKePlans, '文科': wenKePlans}
        for k, v in rt.items():
            for i in v:
                professionPlans = i.get('professionPlans')
                batchcc = k + ' ' + i.get('batchName')
                for idx, ip in enumerate(professionPlans):
                    zname = ip.get('professionName')
                    jihua = ip.get('planNum')
                    xuezhi = ip.get('learnYear')
                    code = ip.get('professionCode')
                    xuefei = ip.get('cost')
                    indx = idx

                    sql = "insert into 专业招生计划_1 (gid,yzyid,院校代码,学校名称,招生名称,ucode,招生代码,专业名称,招生批次,计划数,学制,学费,sortNo,省份,schoolsortNo) values(:gid,:yzyid,:scode,:school,:zsname,:ucode,:code,:zname,:batchcc,:jihua,:xuezhi,:xuefei,:indx,:province,:schoolsortNo)"
                    par = dict(gid=gid, scode=scode, yzyid=yzyid, school=school, zsname=zsname, ucode=ucode, code=code,
                               zname=zname,
                               batchcc=batchcc, jihua=jihua, xuezhi=xuezhi, xuefei=xuefei, indx=indx, province=province,
                               schoolsortNo=schoolsortNo)
                    pars.append(par)
                    sqlist.append(sql)
        if sqlist:
            exsql(Engine, sqlist, select=False, pars=pars)


if __name__ == '__main__':
    conn = MongoClient("mongodb://{MONGO_HOST}:{MONGO_PORT}/".format(MONGO_HOST=MONGO_HOST, MONGO_PORT=MONGO_PORT))
    # conn.admin.authenticate("root5", "TJRWKJ", mechanism='SCRAM-SHA-1')
    db = conn[MONGO_DB]
    tbs = {"MajorComparedData": parseMajorComparedData, "SchoolScoreLine": parseSchoolScoreLine,
           "MajorScoreLine": parseMajorScoreLine, "Plan2019": parsePlan2019}
    tbs = {"SchoolScoreLine": parseSchoolScoreLine}

    for k, v in tbs.items():
        tb = db[k]
        size = tb.find().count()
        # 分几次读取解析，防止内存占满
        for s in range(0, size, lmt):
            q = dataQueue(lmt, s, conn, MONGO_DB, k)
            exethread(v, q, k, threadNum=threadNum)
    conn.close()
