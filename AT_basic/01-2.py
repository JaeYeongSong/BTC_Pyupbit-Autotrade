import pyupbit
import requests
import threading

access = "your access"
secret = "your secret"
myToken = "your key"
upbit = pyupbit.Upbit(access, secret)

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def restart():
    myKRW_balance = upbit.get_balance("KRW") # 보유 현금 조회
    myBTC_balance = upbit.get_balance("KRW-BTC") # KRW-BTC 조회

    myKRW = f"나의 KRW 잔고 : {myKRW_balance}"
    myBTC = f"나의 BTC 잔고 : {myBTC_balance}"

    # 맨 위에 '---'표시는 전에 전송된 정보와 구분하기 위해 사용했습니다
    post_message(myToken,"#balance", "-------------------------------------------------")
    post_message(myToken,"#balance", myKRW)
    post_message(myToken,"#balance", myBTC)

    # 몇초마다 반복하는지 설정합니다(초(s) 단위)
    threading.Timer(300, restart).start() # 현재는 300초(5분) 마다

restart()