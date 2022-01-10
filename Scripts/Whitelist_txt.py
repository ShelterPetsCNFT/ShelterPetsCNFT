import sys 
import time
from blockfrost import BlockFrostApi, ApiError, ApiUrls
import requests
import pandas as pd
import argparse
import random
import os
import datetime
from collections import Counter

os.system('cls||clear')

blockfrostprojid=input('BlockFrostApi key:  ')    








def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '*' * int(percent/100 * barLength - 1) 
    spaces  = ' ' * (barLength - len(arrow))

    print('Loading all assets: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

def makeapi(blockfrostprojid):

    api = BlockFrostApi(
            project_id=blockfrostprojid,

            base_url=ApiUrls.mainnet.value,
    )
    
    return api
    
    
    
def addrcsv():
    
    dict=[]
    dict1=[]
    for i in range(1,len(assets)):
        progressBar(i, len(assets)-1, barLength = 20)
        address=str(api.asset_addresses(asset=assets[i].asset)[0].address)
        

        dict.append(address)
        temp=api.address(address, return_type='json')
        dict1.append(temp['stake_address'])
    print('\n')
    
    dict=list(set(dict))
    with open("Whitelist.txt", 'w') as file:
            for addr in dict:
                file.write(addr+'\n')
       
if __name__ == "__main__":    
    
    
    api = makeapi(blockfrostprojid)
    print('Welcome to the ShelterPets Whitelist Script')
    policy_id=input('Enter Policy ID of project:  ')
    
    assets = api.assets_policy(policy_id=policy_id)

    addrcsv()
    print('Whitelist.exe saved in current directory')
    exit()
 
            
