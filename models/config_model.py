#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/3.

from argeweb import BasicModel
from argeweb import Fields


class ConfigModel(BasicModel):
    class Meta:
        tab_pages = [u'串接參數', u'正式環境', u'測試環境']

    title = Fields.StringProperty(verbose_name=u'設定名稱', default=u'AllPay 相關設定')
    is_sandbox = Fields.BooleanProperty(verbose_name=u'使用測試伺服器', default=True)
    return_url = Fields.StringProperty(verbose_name=u'Return Url', tab_page=0, default=u'')
    client_back_url = Fields.StringProperty(verbose_name=u'Client Back Url', tab_page=0, default=u'')
    payment_info_url = Fields.StringProperty(verbose_name=u'Payment Info Url', tab_page=0, default=u'')

    formal_merchant_id = Fields.StringProperty(verbose_name=u'Merchant ID', tab_page=1, default=u'')
    formal_hash_key = Fields.StringProperty(verbose_name=u'Hash KEY', tab_page=1, default=u'')
    formal_hash_iv = Fields.StringProperty(verbose_name=u'Hash IV', tab_page=1, default=u'')
    formal_service_url = Fields.StringProperty(verbose_name=u'正式伺服器網址', tab_page=1, default=u'https://payment.allpay.com.tw/Cashier/AioCheckOut')

    sandbox_merchant_id = Fields.StringProperty(verbose_name=u'Merchant ID', tab_page=2, default=u'2000132')
    sandbox_hash_key = Fields.StringProperty(verbose_name=u'Hash KEY', tab_page=2, default=u'5294y06JbISpM5x9')
    sandbox_hash_iv = Fields.StringProperty(verbose_name=u'Hash IV', tab_page=2, default=u'v77hoKGq4kWxNNIS')
    sandbox_service_url = Fields.StringProperty(verbose_name=u'測試伺服器網址', tab_page=2, default=u'http://payment-stage.allpay.com.tw/Cashier/AioCheckOut')

    @property
    def merchant_id(self):
        if self.is_sandbox:
            return self.sandbox_merchant_id
        return self.formal_merchant_id

    @property
    def hash_key(self):
        if self.is_sandbox:
            return self.sandbox_hash_key
        return self.formal_hash_key

    @property
    def hash_iv(self):
        if self.is_sandbox:
            return self.sandbox_hash_iv
        return self.formal_hash_iv

    @property
    def service_url(self):
        if self.is_sandbox:
            return self.sandbox_service_url
        return self.formal_service_url