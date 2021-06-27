import pyupbit

access = "gZcEWFSMlT7bBuesSNtyPvVbGiM4754Hh6BIG02n"
secret = "zDI7wgqOZx51f9Av3LiK1YFczZWaqwjC45AfN6Pg"
upbit_Token = pyupbit.Upbit(access, secret)

my_krw = upbit_Token.get_balance("KRW") # 보유 원화 조회
my_btc = upbit_Token.get_balance("KRW-BTC") # 보유 비트코인 조회

print(f'나의 KRW 잔고 : {my_krw}')
print(f'나의 BTC 잔고 : {my_btc}')