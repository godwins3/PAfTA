# from mt5 import MetaTrader5

# mt5 = MetaTrader5()
# mt5.initialize()
# print(mt5.terminal_info())
# mt5.shutdown()
# assert True

from mt5.api.mql import Metatrader as mt5

api =mt5()

accountInfo = api.accountInfo()
print(accountInfo)
print(accountInfo['broker'])
print(accountInfo['balance'])