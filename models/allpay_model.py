#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.
import time

from argeweb import BasicModel
from argeweb import Fields


class MailModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(verbose_name=u'樣版名稱')
    mail_title = Fields.StringProperty(verbose_name=u'信件標題')
    mail_content = Fields.RichTextProperty(verbose_name=u'信件內容')

    @classmethod
    def all_enable(cls, *args, **kwargs):
        return cls.query(cls.is_enable == True).order(-cls.sort)

    @classmethod
    def replace_context(cls, name, title=None, mail_title=None, mail_content=None):
        record = cls.get_or_create(name)
        record.name = name
        if title:
            record.title = title
        if mail_title:
            record.mail_title = mail_title
        if mail_content:
            record.mail_content = mail_content
        record.put()

    @classmethod
    def get_or_create(cls, name):
        record = cls.query(cls.name==name).get()
        if record is None:
            record = cls()
            record.name = name
        record.put()
        return record

