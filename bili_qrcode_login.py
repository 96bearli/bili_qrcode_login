# -*- coding = utf-8 -*-
# @Python : 3.8
import requests
import qrcode
import time

headers = {"Referer": "https://www.bilibili.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/83.0.4103.116 Safari/537.36", }


def start_login(session):
    req = session.get("https://passport.bilibili.com/qrcode/getLoginUrl", headers=headers)
    print(req.text)
    data = req.json()["data"]
    return data["url"], data["oauthKey"]


"""
{"code": 0, "status": true, "ts": 1647939177,
 "data": {"url": "https://passport.bilibili.com/qrcode/h5/login?oauthKey=60b6b6944f9ea04ebfc2ef2ee58a8c7c",
          "oauthKey": "60b6b6944f9ea04ebfc2ef2ee58a8c7c"}}
"""


def gen_qrcode(url):
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    filename = 'qrcode_dome.png'
    img.save(filename)
    img.show()
    print(f"图片已弹出，若未出现，请手动点击 https://api.qrserver.com/v1/create-qr-code/?size=150%C3%97150&data={url}")


def check_state(session, oauthKey):
    data = {'oauthKey': oauthKey, }
    response = session.post('https://passport.bilibili.com/qrcode/getLoginInfo', headers=headers, data=data)
    if response.json()["status"] is not False:
        return s.cookies.get_dict()
    else:
        return "Waiting......"


s = requests.session()
url, oauthKey = start_login(s)
gen_qrcode(url)
while True:
    time.sleep(1)
    ck = check_state(s,oauthKey)
    print(ck)
    if ck != "Waiting......":
        break
with open(f"./cookie_{ck['DedeUserID']}.json", "w", encoding="utf-8") as f:
    f.write(str(ck).replace("'", '"'))
