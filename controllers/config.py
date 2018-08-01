#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, route


class Config(Controller):
    class Scaffold:
        display_in_list = ['is_enable', 'category']
        hidden_in_form = ['name', 'title', 'use']

    @route
    @route_menu(list_name=u'system', group=u'歐付寶', text=u'歐付寶金流設定', sort=803)
    def admin_config(self):
        config_record = self.meta.Model.get_config()
        return scaffold.edit(self, config_record.key)

