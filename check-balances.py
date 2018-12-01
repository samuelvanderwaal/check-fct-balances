import json
from factom import Factomd, FactomWalletd
from coinmarketcap import Market

FACTOSHI_CONV = 1.0E8
total_balance = 0

f = open("config.json")

config = json.load(f)

host = config["host"]

factomd = Factomd(
    host=host
    )
walletd = FactomWalletd()

cmc = Market()
listings = cmc.listings()

for currency in listings["data"]:
    if currency["symbol"] == "FCT":
        fct_id = currency["id"]

price = cmc.ticker(fct_id, convert="USD")["data"]["quotes"]["USD"]["price"]


for name, addr in config["addresses"].items():
    spacing_offset = 27 - len(name)
    balance = int(factomd.factoid_balance(addr)["balance"])/FACTOSHI_CONV
    print("{} balance:             {:>{}}".format(name, balance, spacing_offset))
    total_balance += balance

print("-------------------------------------------------")
print("Total Factoids:              {:>20}".format(total_balance))
print("-------------------------------------------------")
print("Price:                  {:>19}${:,.2f}".format(" ", price))
print("-------------------------------------------------")
print("Current FCT Value: {:>20}${:,.2f}".format(" ", total_balance * price))