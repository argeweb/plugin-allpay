#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/3

import time
import datetime
import urllib
import hashlib
import logging
from google.appengine.api import app_identity
import weakref
from libs.rfc3986 import urlparse

from models.allpay_config_model import AllpayConfigModel


def do_str_replace(string, type_check_out=True):
    if type_check_out:
        mapping_dict = {'-': '%2d', '_': '%5f', '.': '%2e', '!': '%21', '*': '%2a', '(': '%28', ')': '%29',
                        '%2f': '%252f', '%3a': '%253a', '+': '%20', '%2f': '/', '%3a': ':'}
    else:
        mapping_dict = {'-': '%2d', '_': '%5f', '.': '%2e', '!': '%21', '*': '%2a', '(': '%28', ')': '%29', '+': '%20'}
    for key, val in mapping_dict.items():
        string = string.replace(val, key)

    return string

class AllPay():
    _config = None
    # If it is in sandbox mode ?
    url_dict = dict()

    @property
    def config(self):
        if self._config is None:
            self._config = weakref.proxy(AllpayConfigModel.find_by_name('allpay_config'))
        return self._config

    def gen_dict(self, payment_conf, service_method='post'):
        self.service_method = service_method

        self.url_dict['MerchantID'] = self.config.merchant_id
        if 'ReturnURL' in payment_conf:
            self.url_dict['ReturnURL'] = payment_conf['ReturnURL']
        else:
            self.url_dict['ReturnURL'] = self.config.return_url
        self.url_dict['EncryptType'] = '1'
        self.url_dict['PaymentType'] = 'aio'
        self.url_dict['MerchantTradeNo'] = hashlib.sha224(str(datetime.datetime.now())).hexdigest().upper() if not ('MerchantTradeNo' in payment_conf) else payment_conf['MerchantTradeNo']
        self.url_dict['TotalAmount'] = 300 if not ('TotalAmount' in payment_conf) else payment_conf['TotalAmount']
        self.url_dict['TradeDesc'] = 'Default Description' if not ('TradeDesc' in payment_conf) else payment_conf['TradeDesc']
        self.url_dict['ItemName'] = 'Default Item Name' if not ('ItemName' in payment_conf) else payment_conf['ItemName']
        self.url_dict['ChoosePayment'] = 'ATM' if not ('ChoosePayment' in payment_conf) else payment_conf['ChoosePayment']
        self.url_dict['MerchantTradeDate'] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())) if not ('MerchantTradeDate' in payment_conf) else payment_conf['MerchantTradeDate']
        # self.url_dict['MerchantTradeDate'] = '2014/02/08 15:13:20'
        if 'ItemURL' in payment_conf:
            self.url_dict['ItemURL'] = payment_conf['ItemURL']
        if 'Remark' in payment_conf:
            self.url_dict['Remark'] = payment_conf['Remark']
        if 'ChooseSubPayment' in payment_conf:
            self.url_dict['ChooseSubPayment'] = payment_conf['ChooseSubPayment']
        if 'OrderResultURL' in payment_conf:
            self.url_dict['OrderResultURL'] = payment_conf['OrderResultURL']
        elif self.config.client_back_url is not u'':
            self.url_dict['OrderResultURL'] = self.config.client_back_url
        if 'ClientBackURL' in payment_conf:
            self.url_dict['ClientBackURL'] = payment_conf['ClientBackURL']
        elif self.config.client_back_url is not u'':
            self.url_dict['ClientBackURL'] = self.config.client_back_url

        if self.url_dict['ChoosePayment'] == 'ATM':
            self.url_dict['ExpireDate'] = '' if not ('ExpireDate' in payment_conf) else payment_conf['ExpireDate']
            self.url_dict['PaymentInfoURL'] = self.config.payment_info_url if not ('PaymentInfoURL' in payment_conf) else payment_conf['PaymentInfoURL']
        elif 'ChooseSubPayment' in self.url_dict and self.url_dict['ChooseSubPayment'] == 'CVS':
            self.url_dict['Desc_1'] = '' if not ('Desc_1' in payment_conf) else payment_conf['Desc_1']
            self.url_dict['Desc_2'] = '' if not ('Desc_2' in payment_conf) else payment_conf['Desc_2']
            self.url_dict['Desc_3'] = '' if not ('Desc_3' in payment_conf) else payment_conf['Desc_3']
            self.url_dict['Desc_4'] = '' if not ('Desc_4' in payment_conf) else payment_conf['Desc_4']
            self.url_dict['PaymentInfoURL'] = self.config.payment_info_url if not ('PaymentInfoURL' in payment_conf) else payment_conf['PaymentInfoURL']

    def gen_html_form(self, dict_url, auto_send=True):
        """
        Generate The Form Submission
        :param dict_url:
        :return: the html of the form
        """
        form_html = u'<form id="allPay-Form" name="allPayForm" method="post" target="_self" action="%s" style="display: none;">' % self.config.service_url

        for i, val in enumerate(dict_url):
            try:
                s = u"<input type='hidden' name='%s' value='%s' />" % (val, dict_url[val])
            except:
                s = u"<input type='hidden' name='%s' value='%s' />" % (val, dict_url[val].decode('utf8'))
            form_html = u"".join((form_html, s))

        form_html = u"".join((form_html, u'<input type="submit" class="large" id="payment-btn" value="BUY" /></form>'))
        if auto_send:
            form_html = u"".join((form_html, u"<script>document.allPayForm.submit();</script>"))
        return form_html

    def str_parse(self, text):
        n = urlparse(text.encode('utf8'))
        if n.scheme is None:
            return n.path
        else:
            return text

    def check_out(self, payment_conf=None):
        if payment_conf is not None:
            self.gen_dict(payment_conf)
        sorted_dict = sorted(self.url_dict.items())

        # insert the HashKey to the head of dictionary & HashIv to the end
        sorted_dict.insert(0, ('HashKey', self.config.hash_key))
        sorted_dict.append(('HashIV', self.config.hash_iv))
        s = []
        for item in sorted_dict:
            sn = item[1]
            if not isinstance(sn, basestring):
                sn = str(sn)
            s.append(u'%3d'.join((item[0], self.str_parse(sn))))
        result_request_str = do_str_replace(u'%26'.join(s)).lower()
        self.url_dict['CheckMacValue'] = hashlib.sha256(result_request_str).hexdigest().upper()
        return self.url_dict

    @classmethod
    def checkout_feedback(cls, post):
        """
        :param post: post is a dictionary which allPay server sent to us.
        :return: a dictionary containing data the allpay server return to us.
        """
        logging.info('inside the feedback')
        returns = {}
        ar_parameter = {}
        check_mac_value = ''
        try:
            payment_type_replace_map = {'_CVS': '', '_BARCODE': '', '_Alipay': '', '_Tenpay': '', '_CreditCard': ''}
            period_type_replace_map = {'Y': 'Year', 'M': 'Month', 'D': 'Day'}
            for key, val in post.items():

                print key, val
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
            sz_confirm_mac_value = "HashKey=" + HASH_KEY

            for val in sorted_returns:
                sz_confirm_mac_value = "".join((str(sz_confirm_mac_value), "&", str(val[0]), "=", str(val[1])))

            sz_confirm_mac_value = "".join((sz_confirm_mac_value, "&HashIV=", HASH_IV))
            sz_confirm_mac_value = do_str_replace((urllib.quote_plus(sz_confirm_mac_value)).lower(), False)
            sz_confirm_mac_value = hashlib.md5(sz_confirm_mac_value).hexdigest().upper()

            logging.info('sz-checkMacValue: %s & checkMacValue: %s' % (sz_confirm_mac_value, check_mac_value))

            if sz_confirm_mac_value != check_mac_value:
                return False
            else:
                return returns
        except:
            logging.info('Exception!')

    @classmethod
    def query_payment_info(cls, merchant_trade_no):
        """
        Implementing ...
        :param merchant_trade_no:
        :return:
        """
        logging.info('== Query the info==')
        returns = {}
        logging.info(merchant_trade_no)

        return returns
