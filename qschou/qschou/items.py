# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class QschouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Project_ID = Field()  # 项目ID
    Project_recordnum = Field()  # 民政部备案编号
    Project_url = Field()  # 项目URL
    Project_TIT = Field()  # 项目标题
    Project_Domain = Field()  # 项目所属领域
    Project_LAB = Field()  # 项目标签
    Project_LAB_ID = Field()  # 项目标签ID
    Project_Top_ID = Field()  # 项目主题ID
    Project_Intr_S = Field()  # 项目简介
    Project_Money = Field()  # 项目筹款/已筹金额（元）
    Project_Target = Field()  # 目标筹款/目标金额（元）
    Project_Donate = Field()  # 捐款次数（次）【注：非捐赠人次！！】
    Project_PCT = Field()  # 项目完成度
    Feed_count = Field()  # feed数量
    Backer_count = Field()  # follower数量
    Follow_count = Field()  # follow次数
    Share_count = Field()  # 转发次数
    Front_cover = Field()  # 项目首页图片
    Follow_state = Field()  # follow状态

    Project_Intr_date = Field()  # 项目故事时间
    Project_Intr = Field()  # 项目故事内容
    Project_Intr_pic = Field()  # 项目故事图片
    Launch_day = Field()  # 项目进行总时长
    Project_video = Field()  # 项目视频链接
    Match_amount = Field()  # 配捐数量
    Match_subject = Field()  # 配捐人
    Match_proportion = Field()  # 配捐占比
    Share_match_state = Field()  # 配捐分享状态
    Share_match_amount = Field()  # 配捐分享数量
    Match_count = Field()  # 配捐次数
    Match_id = Field()  # 配捐id
    Total_digicash = Field()  # 总数字现金筹款
    Active = Field()  # 是否激活
    State = Field()  # 项目状态
    Is_test = Field()  # 是否是test项目

    Execution = Field() # 存进展追溯的内容
    # Execution_date = Field()  # 进展追溯时间
    # Execution_Plan_content = Field()  # 进展追溯内容
    # Execution_Plan_pic = Field()  # 进展追溯图片

    NPO_LAU = Field()  # 发起机构名称
    NPO_LAU_Logo = Field()  # 发起机构logo
    NPO_LAU_Slogan = Field()  # 发起机构slogan
    NPO_LAU_Ptype = Field()  # 发起机构支付类型
    NPO_LAU_Pay = Field()  # 发起机构是否支付
    NPO_LAU_recodnum = Field()  # 发起机构统一社会信用代码
    NPO_LAU_Email = Field()  # 发起机构邮箱
    NPO_LAU_TEL = Field()  # 发起机构电话
    NPO_LAU_Intro = Field()  # 发起机构介绍
    NPO_EXE = Field()  # 执行机构名称
    NPO_EXE_Logo = Field()  # 执行机构logo
    NPO_EXE_Slogan = Field()  # 执行机构slogan
    NPO_EXE_recodnum = Field()  # 执行机构统一社会信用代码
    NPO_EXE_Email = Field()  # 执行机构邮箱
    NPO_EXE_TEL = Field()  # 执行机构电话

    P_LAU = Field()  # 发起人姓名
    P_LAU_Logo = Field()  # 发起人logo/头像
    P_LAU_Slogan = Field()  # 发起人slogan/介绍
    P_LAU_Email = Field()  # 发起人邮箱
    P_LAU_TEL = Field()  # 发起人电话
    NPO_REC = Field()  # 善款接收方名称
    NPO_REC_Bank = Field()  # 善款接收方银行
    NPO_REC_card = Field()  # 善款接收方银行卡号
    NPO_REC_Email = Field()  # 善款接收方邮箱
    NPO_REC_TEL = Field()  # 善款接收方电话

    Project_Donor = Field()  # 总人数
    Donor = Field()# 用来存捐赠者信息

    # Donor_ID = Field()  # 捐赠者ID
    # Donor_Name = Field()  # 昵称/姓名
    # Donor_Pic = Field()  # 头像图片
    # Donor_Address = Field()  # 地址
    # Donor_DA = Field()  # 捐赠时间
    # Donor_Money = Field()  # 捐赠额
    # Donor_Content = Field()  # 捐赠者留言
    # Donor_Match = Field()  # 配捐？？？
    # Donor_Rank = Field()  # 捐赠排名
    # Love_value = Field()  # 爱心值
    # Backer_type = Field()  # 返回类型
    # Donor_Comment = Field()  # 评论
