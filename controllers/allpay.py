#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search


class Allpay(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)

    class Scaffold:
        display_in_list = ['title', 'mail_title']
        hidden_in_form = ['name']
        excluded_in_form = ()

    def admin_list(self):
        return scaffold.list(self)

    @route
    def test(self):
        from ..allpay import AllPay
        a = AllPay()
        import time
        return a.gen_html_form(a.check_out({
            'TotalAmount': 1000,
            'ChoosePayment': 'ALL',
            'MerchantTradeNo': "allpay20130312153023",
            'MerchantTradeDate': "2013/03/12 15:30:23",
            'ReturnURL': 'https://www.allpay.com.tw/receive.php',
            'ItemName': u"Apple iphone 7 手機殼",
            'TradeDesc': u"促銷方案"
        }))
