import pyupbit

access = "your access"
secret = "your secret"
upbit_Token = pyupbit.Upbit(access, secret)

ret = upbit_Token.buy_limit_order("KRW-BTC", 4000000, 1) # 매수
ret = upbit_Token.sell_limit_order("KRW-BTC", 4000000, 1) # 매도

uuid = ret['uuid'] # 주문번호 얻기
upbit_Token.cancel_order(uuid) # 주문 취소