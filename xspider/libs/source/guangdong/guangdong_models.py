#!usr/bin/env python
# -*- coding:utf-8 -*-
# Created on 2017-03-08 03:50:36
# Project: guangdong
from __future__ import unicode_literals

import datetime
from mongoengine import *
from django.db import models
from collector.models import Project


class GuangdongTask (Document):

    (STATUS_LIVE, STATUS_DISPATCH, STATUS_PROCESS, STATUS_FAIL, STATUS_SUCCESS, STATUS_INVALID) = range(0, 6)
    STATUS_CHOICES = ((STATUS_LIVE, u"新增"),
                      (STATUS_DISPATCH, u'分发中'),
                      (STATUS_PROCESS, u"进行中"),
                      (STATUS_FAIL, u"下载失败"),
                      (STATUS_SUCCESS, u"下载成功"),
                      (STATUS_INVALID, u"任务失效"),)

    project = ReferenceField(Project, reverse_delete_rule=CASCADE)
    status = IntField(default=STATUS_LIVE, choices=STATUS_CHOICES)
    task_id = StringField(max_length=120)
    update_time = DateTimeField(default=datetime.datetime.now)
    schedule = StringField(max_length=1024)
    url = StringField(max_length=8000)
    args = StringField(max_length=2048, null=True)    # 存储cookie， header等信息
    info = StringField(max_length=2048, null=True)    # 源数据的信息,如数据分类,公司名称,权限等
    retry_times = IntField(default=0)
    callback = StringField(max_length=120)
    track_log = StringField(max_length=10240)
    spend_time = StringField(max_length=120, default='0')
    meta = {
        "allow_inheritance": True,
        "db_alias": "xspider_task",
        "indexes": ["task_id", "url", "status"],
    }    # 默认连接的数据库


class GuangdongResult (Document):

    project = ReferenceField(Project)
    task = ReferenceField(GuangdongTask)
    url = StringField(max_length=256)
    update_datetime = DateTimeField(default=datetime.datetime.now)
    result = StringField(max_length=10240)
    meta = {
        "allow_inheritance": True,
        "db_alias": "xspider_result",
        "indexes": ["task"]
    }    # 默认连接的数据库
