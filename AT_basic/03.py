import pyupbit

access = "your access"
secret = "your secret"
upbit_Token = pyupbit.Upbit(access, secret)

# 둘 중에 하나 골라 사용하시면 됩니다.
# 지정가 매도
upbit_Token.sell_limit_order("KRW-BTC", 4000000, 1) #40,000,000원에 BTC 1개 매도

# 시장가 매도
upbit_Token.sell_market_order("KRW-BTC", 1)  #BTC 1개 시장가 매도