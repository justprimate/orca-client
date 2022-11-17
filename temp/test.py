

import time
import json
import requests
import pandas as pd


base_uri = "https://public-api.solscan.io/"

def get_holders(address, n=3):
    holders = {}
    uri = base_uri+"token/holders"
    for i in range(n):
        payload = {"tokenAddress": address, "limit": 100, "offset": 100*i}
        raw = requests.get(uri, payload)
        response = raw.json()["data"]
        for item in response:
            holder = item["address"]
            if (holder not in holders):
                holders[holder] = {"address": holder, "amount": item["amount"], "decimals": item["decimals"], "owner": item["owner"]}
    data = sorted([holders[holder] for holder in holders], key=lambda x: x["amount"], reverse=True)
    return data

def get_metadata(holders):
    data = []
    for holder in holders:
        uri = base_uri+"account/"+holder["owner"]
        raw = requests.get(uri)
        response = raw.json()
        if ("lamports" in response):
            print(holder, response)
            holder["lamports"] = response["lamports"]
            holder["ownerProgram"] = response["ownerProgram"]
            holder["type"] = response["type"]
            holder["rentEpoch"] = response["rentEpoch"]
            holder["executable"] = response["executable"]
            data.append(holder)
        time.sleep(1.5)
    return sorted(data, key=lambda x: x["amount"], reverse=True)

holders = get_holders("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", n=3)
json.dump(holders, open("temp.json", "w"))
holders = json.load(open("temp.json", "r"))
metadata = get_metadata(holders)

df = pd.DataFrame(metadata)
df.to_csv("USDC_metadata.csv")
date = int(time.time())
df = pd.read_csv("USDC_metadata_{date}.csv".format(date=date))
print(df)