#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route


class Allpay(Controller):
    class Scaffold:
        display_in_list = ['title', 'mail_title']

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

    @route
    def pay_with_aio(self):
        from ..libs.api import api
        payment_record = self.params.get_ndb_record('payment_record')
        if payment_record is None:
            self.context['message'] = u'付款資訊不存在'
            self.context['data'] = {'result': 'failure'}
            return
        self.context['data'] = {'result': 'success'}
        self.context['html_code'] = api.gen_html_form(api.check_out({
            'TotalAmount': int(payment_record.amount),
            'ChoosePayment': 'ALL',
            # 'MerchantTradeNo': "abc123",
            # 'MerchantTradeDate': "2013/03/12 15:30:23",
            'ReturnURL': payment_record.return_rul,
            'TradeDesc': payment_record.title,
            'ItemName': payment_record.detail
        }))

    @route
    def pay_with_atm(self):
        return 'atm'

    @route
    def pay_with_card(self):
        return 'card'

    @route
    def taskqueue_after_install(self):
        try:
            from plugins.payment_middle_layer.models.payment_type_model import PaymentTypeModel
            PaymentTypeModel.get_or_create(
                name='allpay_aio',
                title=u'歐付寶支付',
                pay_uri='allpay:allpay:pay_with_aio'
            )
            PaymentTypeModel.get_or_create(
                name='allpay_atm',
                title=u'ATM 付款',
                pay_uri='allpay:allpay:pay_with_atm'
            )
            PaymentTypeModel.get_or_create(
                name='allpay_card',
                title=u'信用卡',
                pay_uri='allpay:allpay:pay_with_card'
            )
            return 'done'
        except ImportError:
            self.logging.error(u'需要 "付款中間層"')
            return 'ImportError'
