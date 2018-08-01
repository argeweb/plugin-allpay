#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/3

import time
import datetime
import hashlib
import weakref
from rfc3986 import urlparse
from ..models.config_model import ConfigModel


def str_replace(string, type_check_out=True):
    if type_check_out:
        mapping_dict = {'-': '%2d', '_': '%5f', '.': '%2e', '!': '%21', '*': '%2a', '(': '%28', ')': '%29',
                        '+': '%20', '%2f': '/', '%3a': ':'}
    else:
        mapping_dict = {'-': '%2d', '_': '%5f', '.': '%2e', '!': '%21', '*': '%2a', '(': '%28', ')': '%29', '+': '%20'}
    for key, val in mapping_dict.items():
        string = string.replace(val, key)

    return string


def str_parse(text):
    n = urlparse(text.encode('utf8'))
    if n.scheme is None:
        if n.path is None:
            return u''
        return n.path
    else:
        return text


class AllpayApi(object):
    _config = None
    # If it is in sandbox mode ?
    url_dict = dict()

    def __init__(self):
        pass

    @property
    def config(self):
        if self._config is None:
            self._config = weakref.proxy(ConfigModel.get_config())
        return self._config

    def gen_dict(self, payment_conf):
        self.url_dict['MerchantID'] = self.config.merchant_id
        self.url_dict['EncryptType'] = '1'
        self.url_dict['PaymentType'] = 'aio'
        self.url_dict['MerchantTradeNo'] = hashlib.sha224(str(datetime.datetime.now())).hexdigest().upper()
        self.url_dict['MerchantTradeDate'] = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        self.url_dict['TotalAmount'] = 300
        self.url_dict['TradeDesc'] = 'Default Description'
        self.url_dict['ItemName'] = 'Default Item Name'
        self.url_dict['ChoosePayment'] = 'ATM'
        self.url_dict['ReturnURL'] = self.config.return_url
        self.url_dict['PaymentInfoURL'] = self.config.payment_info_url
        if self.config.client_back_url is not u'':
            self.url_dict['OrderResultURL'] = self.config.client_back_url
        if self.config.client_back_url is not u'':
            self.url_dict['ClientBackURL'] = self.config.client_back_url

        self.url_dict.update(payment_conf)
        if self.url_dict['ChoosePayment'] == 'ATM':
            self.url_dict['ExpireDate'] = ''
        elif 'ChooseSubPayment' in self.url_dict and self.url_dict['ChooseSubPayment'] == 'CVS':
            self.url_dict['Desc_1'] = self.url_dict['Desc_2'] = self.url_dict['Desc_3'] = self.url_dict['Desc_4'] = ''
        self.url_dict.update(payment_conf)

    def gen_html_form(self, dict_url, service_method='post', auto_send=True):
        """
        Generate The Form Submission
        :param service_method:
        :param dict_url:
        :return: the html of the form
        """
        form_html = u'<form id="allPay-Form" name="allPayForm" ' \
                    u'method="%s" target="_self" action="%s" style="display: none;">' % \
                    (service_method, self.config.service_url)

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

    def check_out(self, payment_conf=None):
        if payment_conf is not None:
            self.gen_dict(payment_conf)
        self.url_dict['CheckMacValue'] = self.gen_mac_code(sorted(self.url_dict.items()))
        return self.url_dict

    def gen_mac_code(self, sorted_dict):
        sorted_dict.insert(0, ('HashKey', self.config.hash_key))
        sorted_dict.append(('HashIV', self.config.hash_iv))
        s = []
        for item in sorted_dict:
            sn = item[1]
            if not isinstance(sn, basestring):
                sn = str(sn)
            s.append(u'%3d'.join((item[0], str_parse(sn))))
        result_request_str = str_replace(u'%26'.join(s)).lower()
        return hashlib.sha256(result_request_str).hexdigest().upper()

api = AllpayApi()
