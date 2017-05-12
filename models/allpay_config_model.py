#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/5/3.

from argeweb import BasicModel
from argeweb import Fields


class AllpayConfigModel(BasicModel):
    class Meta:
        tab_pages = [u'設定', u'伺服器位置']

    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(default=u'AllPay 相關設定', verbose_name=u'服務名稱')
    allpay_sandbox = Fields.BooleanProperty(default=True, verbose_name=u'是否使用測試伺服器')
    merchant_id = Fields.StringProperty(default=u'2000132', verbose_name=u'Merchant ID', tab_page=0)
    hash_key = Fields.StringProperty(default=u'5294y06JbISpM5x9', verbose_name=u'Hash KEY', tab_page=0)
    hash_iv = Fields.StringProperty(default=u'v77hoKGq4kWxNNIS', verbose_name=u'Hash IV', tab_page=0)
    return_url = Fields.StringProperty(default=u'', verbose_name=u'Return Url', tab_page=0)
    client_back_url = Fields.StringProperty(default=u'', verbose_name=u'Client Back Url', tab_page=0)
    payment_info_url = Fields.StringProperty(default=u'', verbose_name=u'Payment Info Url', tab_page=0)
    aio_service_url = Fields.StringProperty(default=u'https://payment.allpay.com.tw/Cashier/AioCheckOut', verbose_name=u'正式伺服器網址', tab_page=1)
    aio_sandbox_service_url = Fields.StringProperty(default=u'http://payment-stage.allpay.com.tw/Cashier/AioCheckOut', verbose_name=u'測試伺服器網址', tab_page=1)

    @property
    def service_url(self):
        if self.allpay_sandbox is True:
            return self.aio_sandbox_service_url
        return self.aio_service_url
