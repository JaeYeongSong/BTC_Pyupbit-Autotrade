import time
import pyupbit
import datetime
import schedule
import requests
from fbprophet import Prophet

access = "gZcEWFSMlT7bBuesSNtyPvVbGiM4754Hh6BIG02n"
secret = "zDI7wgqOZx51f9Av3LiK1YFczZWaqwjC45AfN6Pg"
myToken = "xoxb-2069540101936-2038962172598-TAbFTFbOz5S7Zc2BuNkvGsFf"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

upbit_Token = pyupbit.Upbit(access, secret)

myKRWs = upbit_Token.get_balance("KRW") # 보유 현금 조회
myBTCs = upbit_Token.get_balance("KRW-BTC") # KRW-BTC 조회

myKRW = f"나의 KRW 잔고 : {myKRWs}"
myBTC = f"나의 BTC 잔고 : {myBTCs}"

post_message(myToken,"#stock", myKRW)
post_message(myToken,"#stock", myBTC)

# 비트코인 결재 전 잔고
BeforemyKRW = f"나의 비트코인 구매 전 KRW 잔고 : {myKRWs}"
BeforemyBTC = f"나의 비트코인 구매 전 BTC 잔고 : {myBTCs}"

# 비트코인 결재 후 잔고
AftermyKRW = f"나의 비트코인 구매 후 KRW 잔고 : {myKRWs}"
AftermyBTC = f"나의 비트코인 구매 후 BTC 잔고 : {myBTCs}"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

predicted_close_price = 0
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue
predict_price("KRW-BTC")
schedule.every().hour.do(lambda: predict_price("KRW-BTC"))

# 로그인
upbit = pyupbit.Upbit(access, secret)
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "비트코인 자동화 시작합니다.")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            ma15 = get_ma15("KRW-BTC")
            current_price = get_current_price("KRW-BTC")

            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    # 내 비트코인 구매 전 잔고 스톡으로 보내기 
                    post_message(myToken,"#stock", BeforemyKRW)
                    post_message(myToken,"#stock", BeforemyBTC)

                    # 비트코인 매수하기
                    buy_result = upbit.buy_market_order("KRW-BTC", krw*0.9995)

                    post_message(myToken,"#stock", "BTC buy : " +str(buy_result))

                    # 내 비트코인 구매 후 잔고 스톡으로 보내기 
                    post_message(myToken,"#stock", AftermyKRW)
                    post_message(myToken,"#stock", AftermyBTC)
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                sell_result = upbit.sell_market_order("KRW-BTC", btc*0.9995)
                post_message(myToken,"#stock", "BTC buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        post_message(myToken,"#stock", e)
        time.sleep(1)