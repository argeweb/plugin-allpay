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
        from ..libs.api import api
        import time
        return api.gen_html_form(api.check_out({
            'TotalAmount': 1000,
            'ChoosePayment': 'ALL',
            # 'MerchantTradeNo': "abc123",
            # 'MerchantTradeDate': "2013/03/12 15:30:23",
            'ReturnURL': 'https://www.allpay.com.tw/receive.php',
            'ItemName': u"Apple iphone 7 手機殼",
            'TradeDesc': u"促銷方案"
        }))

    @route
    def feedback(self):
        from ..libs.api import api
        post = self.request
        self.logging.info('inside the feedback')
        returns = {}
        ar_parameter = {}
        check_mac_value = ''
        try:
            payment_type_replace_map = {'_CVS': '', '_BARCODE': '', '_Alipay': '', '_Tenpay': '', '_CreditCard': ''}
            period_type_replace_map = {'Y': 'Year', 'M': 'Month', 'D': 'Day'}

            for key, val in post.items():
                if key == 'CheckMacValue':
                    check_mac_value = val
                else:
                    ar_parameter[key.lower()] = val
                    if key == 'PaymentType':
                        for origin, replacement in payment_type_replace_map.items():
                            val = val.replace(origin, replacement)
                    elif key == 'PeriodType':
                        for origin, replacement in period_type_replace_map.items():
                            val = val.replace(origin, replacement)
                    returns[key] = val

            sorted_returns = sorted(ar_parameter.items())
            sz_confirm_mac_value = api.gen_mac_code(sorted_returns)

            self.logging.info('sz-checkMacValue: %s & checkMacValue: %s' % (sz_confirm_mac_value, check_mac_value))

            if sz_confirm_mac_value != check_mac_value:
                return False
            else:
                return returns
        except:
            self.logging.info('Exception!')