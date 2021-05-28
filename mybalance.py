import pyupbit
import requests
import threading

access = "your_key"
secret = "your_key"
upbit = pyupbit.Upbit(access, secret)

myToken = "your_key"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def restart():
    myKRWs = upbit.get_balance("KRW") # 보유 현금 조회
    myBTCs = upbit.get_balance("KRW-BTC") # KRW-BTC 조회

    myKRW = f"나의 KRW 잔고 : {myKRWs}"
    myBTC = f"나의 BTC 잔고 : {myBTCs}"

    post_message(myToken,"#balance", "-------------------------------------------------")
    post_message(myToken,"#balance", myKRW)
    post_message(myToken,"#balance", myBTC)

    threading.Timer(300, restart).start()

restart()