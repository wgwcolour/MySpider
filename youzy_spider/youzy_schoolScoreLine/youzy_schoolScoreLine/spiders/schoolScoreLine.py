# -*- coding: utf-8 -*-
import scrapy
from sqlalchemy import create_engine, text
import sys
from subprocess import Popen, PIPE
import json
import re
from youzy_schoolScoreLine.items import SchoolScoreLineItem, MajorComparedDataItem, MajorScoreLineItem, Plan2019Item,ErrorSchoolItem


class SchoolscorelineSpider(scrapy.Spider):
    parseData = r'E:\PycharmProjects\my_scrapy\youzy_spider\parseData.js'  # 解析datajs文件地址
    # parseData = r'C:\Users\Administrator\Desktop\youzy_spider\parseData.js'  # 解析datajs文件地址
    name = 'schoolScoreLine'
    allowed_domains = ['www.youzy.cn']
    # sqlserver = "mssql+pymssql://sa:tjrw#EDC@127.0.0.1/gaokao9?charset=utf8"
    sqlserver = "mssql+pymssql://sa:wgwqqq@127.0.0.1/gaokao4?charset=utf8"
    Engine = create_engine(sqlserver)
    rule = re.compile("'(.*?)'", re.S)
    ##############################基础配置############################
    # 需要采集的数据
    SchoolScoreLine = True  # 学校分数线
    MajorComparedData = False  # 专业招生对比数据
    MajorScoreLine = False  # 专业分数线-历年(2012-2018)
    Plan2019 = False  # 2019年招生计划

    # 省份列表 这个所有都用的到
    provinceList = [835]
    # 文理科列表 这个除了【学校分数线】，其他都用得到
    courseList = [0, 1]
    # 年份列表 2012-2018年  这个是学校主页的【专业分数线】用到
    years = range(2012, 2019)
    ##################################################################

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Host": "www.youzy.cn",
        "Origin": 'https://www.youzy.cn',
        "Referer": "https://www.youzy.cn/tzy/search/scoreLines",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        # "Cookie":"UM_distinctid=16b647c94ef24b-08fa7a4a5cd17b-591d3314-144000-16b647c94f0253; connect.sid=s%3A4051E5VEA_XyMqjRgzzcMSrp8ThMdNHe.yF4dr6NjTWTGoT3Q0kKTk9cf5JY4rKYCtDMQizua660; Youzy2CCurrentProvince=%7B%22provinceId%22%3A835%2C%22provinceName%22%3A%22%E5%A4%A9%E6%B4%A5%22%2C%22isGaokaoVersion%22%3Afalse%7D; Youzy2CUser=%7B%22numId%22%3A11686457%2C%22realName%22%3Anull%2C%22avatarUrl%22%3Anull%2C%22gender%22%3A0%2C%22provinceId%22%3A835%2C%22cityId%22%3A14835%2C%22countyId%22%3A14850%2C%22schoolId%22%3A17243%2C%22class%22%3Anull%2C%22gkYear%22%3A2019%2C%22isZZUser%22%3Afalse%2C%22zzCount%22%3A0%2C%22isElective%22%3Afalse%2C%22active%22%3Atrue%2C%22courseType%22%3A0%2C%22secretName%22%3A%22156****5171%22%2C%22userPermissionId%22%3A3%2C%22identityExpirationTime%22%3A%222022-03-20T02%3A09%3A28.17Z%22%2C%22username%22%3A%2215620745171%22%2C%22mobilePhone%22%3A%2215620745171%22%2C%22provinceName%22%3Anull%2C%22cityName%22%3Anull%2C%22countyName%22%3Anull%2C%22schoolName%22%3Anull%2C%22updateGaoKaoCount%22%3A0%2C%22lastLoginDate%22%3A%220001-01-01T00%3A00%3A00%22%2C%22creationTime%22%3A%222018-08-22T14%3A45%3A29.59%2B08%3A00%22%2C%22id%22%3A%225cf584d09e742b1f88768888%22%2C%22vipPermission%22%3Atrue%7D; Youzy2CCurrentScore=%7B%22numId%22%3A2841180%2C%22provinceNumId%22%3A835%2C%22provinceName%22%3A%22%E5%A4%A9%E6%B4%A5%22%2C%22total%22%3A500%2C%22courseTypeId%22%3A0%2C%22rank%22%3A0%2C%22chooseLevelOrSubjects%22%3A%22%3D%2C%3D%22%2C%22scoreType%22%3A1%2C%22chooseLevelFormat%22%3A%5B%5D%2C%22chooseSubjectsFormat%22%3A%5B%5D%7D; CNZZDATA1254568697=1670195845-1560757693-https%253A%252F%252Fwww.youzy.cn%252F%7C1561081807"
    }

    # 执行sql语句
    def exsql(self, engine, sql, select=True, pars=None, echo=True):
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

    def getData(self, input):
        try:
            process = Popen(['node', self.parseData, json.dumps(input)], stdout=PIPE, stderr=PIPE)
        except (OSError, IOError) as err:
            print('请先安装 node.js: https://nodejs.org/')
            sys.exit()
        data = process.communicate()[0].decode().strip('\n').strip('\r')
        d = re.findall(self.rule, data)[0]
        return d

    def recordError(self, **kwargs):
        # 这个方法用来记录所有采集过程中出现错误的学校
        # 出现的错误只有一种：isSuccess为False
        provinceId, course, schoolId, school = kwargs.get('provinceId', ''), kwargs.get('course', ''), kwargs.get(
            'schoolId', ''), kwargs.get('school', '')
        with open("Error.csv", 'a+', encoding='utf-8') as f:
            result = [provinceId, course, schoolId, school]
            print("Error:" + ' '.join(result))
            f.write(','.join(result))

    schoolList=[]

    def start_requests(self):
        # 读取优志愿的全部学校列表
        # sql = "select top 5 id,名称 from 学校_优志愿 where 名称 = '天津大学'"
        # sql = "select top 5 id,名称 from 学校_优志愿"
        sql = "select id,名称 from 学校_优志愿"
        schoolList, _ = self.exsql(self.Engine, sql)
        for provinceId in self.provinceList:
            for idx, school in enumerate(schoolList):
                self.schoolList.append(school[1])
                print(provinceId,school)
                input1 = {
                    "provinceId": str(provinceId),
                    "collegeId": str(school[0])
                }
                data = self.getData(input1)
                url = "https://www.youzy.cn/Data/ScoreLines/UCodes/QueryList"
                yield scrapy.Request(url=url, method='POST', headers=self.headers, body=json.dumps({'data': data}),
                                     meta=dict(provinceId=provinceId, course=None, schoolId=school[0],
                                               school=school[1]))



    def parse(self, response):
        meta = response.meta
        provinceId = meta.get('provinceId')
        # 获取学校列表
        schoolList = json.loads(response.text)
        isSuccess = schoolList.get('isSuccess')
        if isSuccess:
            result = schoolList.get('result')
            if not result:
                self.schoolList.remove(meta['school'])
            for idx, i in enumerate(result):
                meta.update(i)
                meta.update(schoolSortNo=idx)
                ucode = meta.get('uCodeNum')
                if self.SchoolScoreLine:
                    input = {
                        "provinceNumId": provinceId,
                        "ucode": ucode
                    }
                    data = self.getData(input)
                    url = "https://www.youzy.cn/Data/ScoreLines/Fractions/Colleges/Query"
                    # 这里是请求的【学校分数线数据】
                    yield scrapy.Request(url=url, method='POST', headers=self.headers, body=json.dumps({'data': data}),
                                         meta=meta, callback=self.parseScoreLine)
                if self.MajorScoreLine or self.MajorComparedData or self.Plan2019:
                    # 获取批次列表 这里已经开始分文理科了
                    for course in self.courseList:
                        meta['course'] = course
                        if self.MajorComparedData:  # 是否采集【专业招生对比数据】
                            dli = "ucode={0}&courseType={1}&provinceId={2}".format(ucode, course, provinceId)
                            url = "https://www.youzy.cn/Data/TZY/CollegeEnroll/QueryBatchsByLatestPlan?{0}".format(dli)
                            # 这里请求的批次列表
                            yield scrapy.Request(url=url, method='POST', headers=self.headers,
                                                 meta=meta, callback=self.parseBatchList)
                        if self.MajorScoreLine:  # 是否采集【专业分数线】
                            # 这里请求【专业分数线】
                            for year in self.years:
                                input = {
                                    "uCode": ucode,
                                    "batch": 0,
                                    "courseType": course,
                                    "yearFrom": year,
                                    "yearTo": year
                                }
                                data = self.getData(input)
                                url = 'https://www.youzy.cn/Data/ScoreLines/Fractions/Professions/Query'
                                yield scrapy.Request(url=url, body=json.dumps({"data": data}), headers=self.headers,
                                                     method='POST', callback=self.parseMajorScoreLine,meta=meta)
                        if self.Plan2019:  # 是否采集【2019年招生计划】
                            # 这里请求学校主页的【2019年招生计划】
                            input = {
                                "year": '2019',
                                "ucodes": ucode
                            }
                            data = self.getData(input)
                            url = "https://www.youzy.cn/Data/ScoreLines/Plans/Professions/Query"
                            yield scrapy.Request(url=url, body=json.dumps({"data": data}), headers=self.headers,
                                                 method='POST', callback=self.parsePlan2019,meta=meta)
        else:
            self.recordError(**meta)

    def parseBatchList(self, response):
        meta = response.meta
        BatchList = json.loads(response.text)
        isSuccess = BatchList.get('isSuccess')
        if isSuccess:
            result = BatchList.get('result')
            for i in result:
                batch = i.get('batch')
                batchName = i.get('batchName')
                meta.update(i)
                input = dict(provinceId=meta.get('provinceId'), uCode=meta.get('uCodeNum'), batch=batch,
                             courseType=meta.get('course'), isFillPro=False, totalScore=0, rank=0, lineDiff=0)
                data = self.getData(input)
                url = "https://www.youzy.cn/Data/TZY/Recommendation/QueryProfessionHistoriesDecrypt"
                # 这个请求是获取【专业招生对比数据】的 TODO 回调函数还没写
                yield scrapy.Request(url=url, method='POST', headers=self.headers,
                                     meta=meta, body=json.dumps({"data": data}), callback=self.parseMajorComparedData)
        else:
            self.recordError(**meta)

    def parseScoreLine(self, response):
        item = SchoolScoreLineItem()
        meta = response.meta
        meta['result'] = json.loads(response.text)
        item._values=meta
        yield item

    def parseMajorComparedData(self, response):
        item = MajorComparedDataItem()
        meta = response.meta
        meta['result'] = json.loads(response.text)
        item._values = meta
        yield item

    def parseMajorScoreLine(self, response):
        item = MajorScoreLineItem()
        meta = response.meta
        meta['result'] = json.loads(response.text)
        item._values = meta
        yield item

    def parsePlan2019(self, response):
        item = Plan2019Item()
        meta = response.meta
        meta['result'] = json.loads(response.text)
        item._values = meta
        yield item
