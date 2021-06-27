import pyupbit

access = "your access"
secret = "your secret"
upbit_Token = pyupbit.Upbit(access, secret)

my_krw = upbit_Token.get_balance("KRW") # 보유 원화 조회
my_btc = upbit_Token.get_balance("KRW-BTC") # 보유 비트코인 조회

print(f'나의 KRW 잔고 : {my_krw}')
print(f'나의 BTC 잔고 : {my_btc}')
