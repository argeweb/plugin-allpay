#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import ViewDatastore
from allpay import AllPay, AllpayConfigModel


__all__ = (
    'AllPay'
    'AllpayConfigModel'
)

plugins_helper = {
    'title': u'歐付寶金流串接相關功能',
    'desc': u'歐付寶為台灣金流廠商，此為其相關串接',
    'controllers': {
        'allpay': {
            'group': u'串接記錄管理',
            'actions': [
                {'action': 'list', 'name': u'串接記錄'},
                {'action': 'add', 'name': u'新增記錄'},
                {'action': 'edit', 'name': u'編輯記錄'},
                {'action': 'view', 'name': u'檢視記錄'},
                {'action': 'delete', 'name': u'刪除記錄'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
            ]
        },
        'allpay_config': {
            'group': u'歐付寶設定',
            'actions': [
                {'action': 'config', 'name': u'歐付寶相關設定'},
            ]
        },
    }
}
