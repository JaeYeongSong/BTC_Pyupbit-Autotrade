import pyupbit

access = "your access"
secret = "your secret"
upbit_Token = pyupbit.Upbit(access, secret)

# 둘 중에 하나 골라 사용하시면 됩니다.
# 지정가 매수
upbit_Token.buy_limit_order("KRW-BTC", 40000000, 1) #40,000,000원에 BTC 1개 매수

# 시장가 매수
upbit_Token.buy_market_order("KRW-BTC", 10000) #BTC 10,000원어치 시장가 매수