import base64
import datetime

import rsa

ENDTIME = "20:03:00"
# Base Urls
HOST = "there.shu.edu.cn"
BASEURL = "https://%s/" % HOST
OAUTHURL = "login-oauth2"
GRABURL = "api/v3/bookings"

SECTOR_ALL_ID = "7pcMcUCRxXE6fzXhLp7za7"
AREA_ID_DIC = {
    "A": "WyN53UzbmRsLjpR1t1ttWL",
    "B": "DsNjTXf8icSMh3SXB5HPge",
    "C": "YLyBwnQ7frVRt49UMSCtnX",
}

KEYSTR = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDl/aCgRl9f/4ON9MewoVnV58OLOU2ALBi2FKc5yIsfSpivKxe7A6FitJjHva3WpM7gvVOinMehp6if2UNIkbaN+plWf5IwqEVxsNZpeixc4GsbY9dXEk3WtRjwGSyDLySzEESH/kpJVoxO7ijRYqU+2oSRwTBNePOk1H+LRQokgQIDAQAB
    -----END PUBLIC KEY-----"""


def getDate():
    # 获取当前日期的datetime对象
    today = datetime.date.today()

    # 将datetime对象加上一天的timedelta，得到下一天的datetime对象
    next_day = today + datetime.timedelta(days=1)
    endDate = startDate = next_day.strftime("%Y-%m-%d")
    return startDate, endDate


def encryptPass(passwd):
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(KEYSTR.encode("utf-8"))
    encryptpwd = base64.b64encode(rsa.encrypt(passwd.encode("utf-8"), pubkey)).decode()
    return encryptpwd
