import json
import time
from datetime import datetime, timedelta

import requests
import urllib3
import yaml

from BookingThread import BookingThread
from utils import (AREA_ID_DIC, BASEURL, ENDTIME, HOST, OAUTHURL,
                   getDate, encryptPass)


class SHU24hAPI:
    def __init__(self):
        self.roomdic = json.load(open("data/roomdic.json", "r", encoding="utf-8"))
        self.config_yaml_data = yaml.safe_load(
            open("config.yaml", "r", encoding="utf-8")
        )

        self.username = self.config_yaml_data["username"]
        self.password = encryptPass(self.config_yaml_data["password"])
        self.seat_id = self.roomdic[self.config_yaml_data["seat_id"]]["id"]
        self.area_id = AREA_ID_DIC[self.config_yaml_data["seat_id"][0]]
        self.startDate, self.endDate = getDate()
        self.startTime = datetime.strptime(self.config_yaml_data["startTime"], "%H:%M")
        self.endTime = datetime.strptime(self.config_yaml_data["endTime"], "%H:%M")
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = True

    def login(self):
        self.session.verify = False
        self.session.trust_env = True
        # self.session.proxies = {
        #     "http": "http://127.0.0.1:12347",
        #     "https": "http://127.0.0.1:12347"
        # }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            r = self.session.get(BASEURL + OAUTHURL, verify=False)
        except Exception as emsg:
            print(str(emsg))
            print("\nUnable to connect:(\nPlease use VPN or check network settings")
            exit(1)
        if not r.url.startswith(
                ("https://oauth.shu.edu.cn/", "https://newsso.shu.edu.cn/", BASEURL)
        ):
            raise RuntimeError(1, f"Unexpected Result")
        request_data = {"username": self.username, "password": self.password}
        r = self.session.post(r.url, request_data, verify=False)
        if HOST not in r.url:
            if "too many requests" in r.text:
                raise RuntimeError(2, f"Too many Requests, try again later")
            raise RuntimeError(2, f"Login Failed")
        else:
            print("Login Successful:" + self.username)

    def grab(self):
        # 获取拆分后的时间段
        start_time_ls, end_time_ls = self.get_time_period()

        # 获取当前时间
        current_time = time.strftime("%H:%M:%S", time.localtime())
        # 初始化线程列表
        threads = []
        while current_time < ENDTIME:
            for i in range(len(end_time_ls)):
                t = BookingThread(
                    start_time_ls[i],
                    end_time_ls[i],
                    self.session,
                    self.seat_id,
                    self.area_id,
                    self.startDate,
                    self.endDate,
                )
                t.start()
                threads.append(t)

            # 等待所有线程结束
            for t in threads:
                t.join()

            time.sleep(0.1)  # 每隔 5 秒重试
            current_time = time.strftime("%H:%M:%S", time.localtime())

    def get_time_period(self):
        # 定义最长时间段为 4 小时
        max_hours = 4

        # 初始化本地开始时间为开始时间
        local_start_time = self.startTime

        start_time_ls = []
        end_time_ls = []

        # 循环拆分时间段
        while local_start_time < self.endTime:
            # 计算本地结束时间
            local_end_time = local_start_time + timedelta(hours=max_hours)
            # 如果本地结束时间超过结束时间，则将本地结束时间设置为结束时间
            if local_end_time > self.endTime:
                local_end_time = self.endTime
            # 输出本次时间段的开始时间和结束时间
            start_time_ls.append(local_start_time.strftime("%H:%M"))
            end_time_ls.append(local_end_time.strftime("%H:%M"))
            # 将本地开始时间设置为本地结束时间，然后继续循环
            local_start_time = local_end_time
        return start_time_ls, end_time_ls
