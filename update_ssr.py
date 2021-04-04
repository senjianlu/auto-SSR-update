#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#
# @AUTHOR: Rabbir
# @FILE: /root/Github/ssr_updater/update_ssr.py
# @DATE: 2021/02/05 Fri
# @TIME: 15:25:54
#
# @DESCRIPTION: 更新 ssr config 配置文件的模块


import os
import json
import requests
import ssr_parser
from rab_python_packages import rab_config


# 存储 SSR 配置信息的文件
ssr_config = rab_config.get_config("ssr.ini")


"""
@description: 修改 SSR 的配置文件
-------
@param:
-------
@return:
"""
def update_ssr_config(ssr_info):
    try:
        # 获取 SSR 配置文件路径
        ssr_config_path = ssr_config["ssr_config"]["ssr_config_path"]
        # 获取 SSR 绑定的本地端口
        ssr_port_dict = {
            "local_port": ssr_config["ssr_config"]["ssr_port"]
        }
        # 读取既存配置并更新
        with open(ssr_config_path+"/config.json", "r") as f:
            origin_config_str = ""
            for line in f.readlines():
                line = line.replace("\n", "").replace("\r", "").strip()
                # 去掉双斜杠的数值
                if ("//" in line):
                    line = line.split("//")[0]
                if (line):
                    origin_config_str = origin_config_str + line
            origin_config = json.loads(origin_config_str)
            # 更新 SSR 代理信息
            origin_config.update(ssr_info)
            origin_config.update(ssr_port_dict)
            origin_config = json.dumps(origin_config,
                                    sort_keys=True,
                                    indent=4,
                                    separators=(',', ':'))
        # 开始写入更新后的代理信息
        with open(ssr_config_path+"/config.json", "w", encoding="UTF-8") as f:
            f.write(origin_config)
        print("已更新代理信息！代理信息：")
        print(ssr_info)
        return True
    except Exception as e:
        print("修改 SSR 的配置文件时出错！错误信息：" + str(e))
        return False

"""
@description: 测试代理对测试网站是否可以访问
-------
@param:
-------
@return:
"""
def test_ssr_access():
    # 需要测试的网站地址
    access_test_urls = json.loads(
        ssr_config["access_test_config"]["access_test_urls"])
    # 超时时间
    timeout = int(ssr_config["access_test_config"]["access_test_timeout"])
    # 本地代理端口
    ssr_port = ssr_config["ssr_config"]["ssr_port"]
    proxy = {
        "http": "socks5://127.0.0.1:" + str(ssr_port),
        "https": "socks5://127.0.0.1:" + str(ssr_port)
    }
    for access_test_url in access_test_urls:
        try:
            response = requests.get(access_test_url,
                                    proxies=proxy,
                                    timeout=timeout)
            if (response.status_code == 200):
                continue
            else:
                print("测试代理访问网站失败！相应码：" + str(response.status_code))
                return False
        except Exception as e:
            print("测试代理访问网站出错！错误信息：" + str(e))
            return False
    return True

"""
@description: 测试代理是否满足限制条件
-------
@param:
-------
@return:
"""
def test_proxy_limit():
    # 超时时间
    timeout = int(ssr_config["access_test_config"]["access_test_timeout"])
    # 本地代理端口
    ssr_port = ssr_config["ssr_config"]["ssr_port"]
    proxy = {
        "http": "socks5://127.0.0.1:" + str(ssr_port),
        "https": "socks5://127.0.0.1:" + str(ssr_port)
    }
    try:
        res = url = requests.get("http://ip-api.com/json/?lang=zh-CN",
                                 proxies=proxy,
                                 timeout=timeout)
        if (json.loads(res.text)["country"] in json.loads(
                ssr_config["proxy_limit"]["proxy_location"])):
            return True
    except Exception as e:
        print("测试代理是否满足限制条件时出错！" + str(e))
    return False


"""
@description: 单体测试
-------
@param:
-------
@return:
"""
if __name__ == "__main__":
    # 从配置文件中获取订阅链接并解析为代理信息
    ssr_subscription_urls = json.loads(
        ssr_config["ssr_config"]["ssr_subscription_urls"])
    ssr_infos = ssr_parser.parse_ssr_subscription_urls(ssr_subscription_urls)
    # 循环每个代理信息
    for ssr_info in ssr_infos:
        # 修改 ssr_config 并测试是否可以网页
        update_ssr_config(ssr_info)
        # 重启 SSR
        os.system("ssr stop")
        os.system("ssr start")
        # 首先测试该代理是否满足限制条件
        if (test_proxy_limit()):
            # 测试此代理是否可以访问所有测试页面
            if (test_ssr_access()):
                print("代理测试通过！当前代理信息：")
                print(ssr_info)
                break

