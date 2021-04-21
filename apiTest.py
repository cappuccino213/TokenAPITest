#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 9:38 
# @Author  : Zhang yp
# @File    : apiTest.py
# @Software: PyCharm
# @license : Copyright(C), eWord Technology Co., Ltd.
# @Contact : yeahcheung213@163.com
from config import cfg
from requests import request


# 从cfg获取多个参数的list
def multiple_para2list(mul_par):
    par_list = mul_par.split(',')
    # 去除换行符
    par_list = [par.replace('\n', '') if '\n' in par else par for par in par_list]
    # print(par_list)
    return par_list


# 生成API请求的多组入参
def in_parameter_list():
    retrieve_list = cfg.get_raw('TASK', 'retrieve')
    validate_list = cfg.get_raw('TASK', 'validate')
    product_list = cfg.get_raw('TASK', 'productName')
    for product in product_list:
        for retrieve in retrieve_list:
            if retrieve == 'Retrive':
                retrieve_case = []
                body = {
                    "uniqueIdentity": "QWYHZYFZX",
                    "hospitalCode": "QWYHZYFZX",
                    "timestamp": "1595314032",
                    "requestIP": "192.168.1.56",
                    "audience": product,
                    "appId": ""
                }
                retrieve_case.append(body)
            if retrieve == 'InternalRetrive':
                retrieve_internal_case = []
                body = {
                    "ProductName": product,
                    "HospitalCode": "QWYHZYFZX",
                    "RequestIP": "192.168.1.56"
                }
                retrieve_internal_case.append(body)
            if retrieve == 'InteractiveRetrive':
                retrieve_interactive_case = []
                body = {
                    "ProductName": product,
                    "HospitalCode": "QWYHZYFZX"
                }
                retrieve_interactive_case.append(body)

        for validate in validate_list:
            if validate == 'Validate':
                validate_case = []
                body = {
                    "appId": "",
                    "timestamp": "1595314032",
                    "sign": "string",
                    "productName": product,
                    "hospitalCode": "QWYHZYFZX",
                    "requestIP": "192.168.1.56"
                }
                validate_case.append(body)
            if validate == 'InternalValidate':
                validate_internal_case = []
                body = {
                    "ProductName": product,
                    "HospitalCode": "QWYHZYFZX",
                    "RequestIP": "192.168.1.56"
                }
                validate_internal_case.append(body)
            if validate == 'InteractiveValidate':
                validate_interactive_case = []
                body = {
                    "ProductName": product,
                    "HospitalCode": "QWYHZYFZX"
                }
                validate_interactive_case.append(body)


# http请求的通用方法
def api_test(path, auth, payload):
    """
    :param path: api的url完整路径
    :param auth: 是否需要在header里面加入token
    :param payload: 请求入参
    :return:
    """
    api_url = cfg.get_raw('API', 'host') + ':' + cfg.get_raw('API', 'port') + path
    # print(api_url)
    hea = {'Content-Type': 'application/json'}
    if auth:
        hea['Authorization'] = auth
        # hea['Content-Length'] = 0
    res = request(method='POST', url=api_url, headers=hea, json=payload)
    return res


"""验证逻辑"""


# 老产品
def old_token(product):
    retrieve = api_test('/Token/Retrive', None, {
        "uniqueIdentity": "QWYHZYFZX",
        "hospitalCode": "QWYHZYFZX",
        "requestIP": "192.168.1.56",
        "audience": product,
        "customData": {},
        "expire": 3
    })
    # print(retrieve.status_code)
    if retrieve.status_code == 200:
        if retrieve.json()['status'] == 0:
            token = retrieve.json()['token']
            validate = api_test('/Token/Validate', token, None)
            if validate.json()['status'] == 0:
                print(f'{product} retrieve成功，validate成功')
            else:
                print('{}retrieve成功，validate失败，失败原因{}'.format(product, validate.json()['desc']))
        else:
            print('{}retrieve失败，失败原因{}'.format(product, retrieve.json()['desc']))


# 新产品
def new_token(product):
    retrieve = api_test('/Token/RetriveInternal', None, {
        "ProductName": product,
        "HospitalCode": "QWYHZYFZX",
        "RequestIP": "192.168.1.56"
    })
    # print(retrieve.status_code)
    if retrieve.status_code == 200:
        if retrieve.json()['status'] == 0:
            token = retrieve.json()['token']
            validate = api_test('/Token/ValidateInternal', token, {
                "ProductName": product,
                "HospitalCode": "QWYHZYFZX",
                "RequestIP": "192.168.1.56"
            })
            if validate.json()['status'] == 0:
                print(f'{product} RetriveInternal成功，ValidateInternal成功')
                # pass
            else:
                print('{}RetriveInternal成功，ValidateInternal失败，失败原因{}'.format(product, validate.json()['desc']))
        else:
            print('{}RetriveInternal失败，RetriveInternal失败原因{}'.format(product, retrieve.json()['desc']))


# 新产品互相调用
def new_token_interactive(call, called):
    retrieve = api_test('/Token/RetriveInteractive', None, {
        "ProductName": call,
        "HospitalCode": "QWYHZYFZX",
    })
    # print(retrieve.status_code)
    if retrieve.status_code == 200:
        if retrieve.json()['status'] == 0:
            token = retrieve.json()['token']
            validate = api_test('/Token/ValidateInteractive', token, {
                "ProductName": called,
                "HospitalCode": "QWYHZYFZX"
            })
            if validate.json()['status'] == 0:
                print(f'{call} RetriveInteractive成功，{called} ValidateInteractive成功')
                # pass
            else:
                print('{} RetriveInteractive成功，{} ValidateInteractive失败，失败原因{}'.format(call, called,
                                                                                       validate.json()['desc']))
        else:
            print('{} RetriveInteractive失败，{} ValidateInteractive失败原因{}'.format(call, called, retrieve.json()['desc']))


# 新-老产品互相调用
def new_old_token_interactive(call, called):
    retrieve = api_test('/Token/RetriveInteractive', None, {
        "ProductName": call,
        "HospitalCode": "QWYHZYFZX",
    })
    # print(retrieve.status_code)
    if retrieve.status_code == 200:
        if retrieve.json()['status'] == 0:
            token = retrieve.json()['token']
            validate = api_test('/Token/Validate', token, None)
            if validate.json()['status'] == 0:
                print(f'{call} RetriveInteractive成功，{called} Validate成功')
                # pass
            else:
                print('{} RetriveInteractive成功，{} Validate失败，失败原因{}'.format(call, called,
                                                                            validate.json()['desc']))
        else:
            print('{} RetriveInteractive失败，{} Validate失败原因{}'.format(call, called, retrieve.json()['desc']))


# 老-新产品互相调用
def old_new_token_interactive(call, called):
    retrieve = api_test('/Token/Retrive', None, {
        "uniqueIdentity": "QWYHZYFZX",
        "hospitalCode": "QWYHZYFZX",
        "requestIP": "192.168.1.56",
        "audience": call,
        "customData": {},
        "expire": 3
    })
    # print(retrieve.status_code)
    if retrieve.status_code == 200:
        if retrieve.json()['status'] == 0:
            token = retrieve.json()['token']
            validate = api_test('/Token/ValidateInteractive', token, {
                "ProductName": called,
                "HospitalCode": "QWYHZYFZX"
            })
            if validate.json()['status'] == 0:
                print(f'{call} Retrive成功，{called} ValidateInteractive成功')
                # pass
            else:
                print('{} Retrive成功，{} ValidateInteractive失败，失败原因{}'.format(call, called,
                                                                            validate.json()['desc']))
        else:
            print('{} Retrive失败，{} ValidateInteractive失败原因{}'.format(call, called, retrieve.json()['desc']))


def main():
    product_list = multiple_para2list(cfg.get_raw('TASK', 'productName'))
    for product in product_list:
        print(f'old_token_case{product_list.index(product) + 1}')
        old_token(product)

        print(f'new_token_case{product_list.index(product) + 1}')
        new_token(product)

    product_call_list = multiple_para2list(cfg.get_raw('TASK', 'productCall'))
    product_called_list = multiple_para2list(cfg.get_raw('TASK', 'productCalled'))
    for call in product_call_list:
        for called in product_called_list:
            if call != called:
                new_token_interactive(call, called)
                new_old_token_interactive(call, called)
                old_new_token_interactive(call, called)
                # pass


if __name__ == '__main__':
    main()
