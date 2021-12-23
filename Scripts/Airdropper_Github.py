import sys 
import time
from blockfrost import BlockFrostApi, ApiError, ApiUrls
import requests
import pandas
import argparse
import random
import os
import datetime

#########GLOBAL VARIABLES##############
#If test = 1, test mint
#if test='live', airdrop will be live (be careful as this can mint using nftmakerwallet). backup varible must be changed in airdropapicall function
test=1


#blockfrost project id
blockfrostprojid=''    

#nftmakerAPI
apikey=''

#nftmakerProjectid
nftprojectid=''

#nftmakercount
countnft='1'


#start and end time for time based airdrop
timestart= datetime.datetime(2021, 12, 20, 23, 59, 59)
timeend= datetime.datetime(2021, 12, 25, 23, 59, 59)


def makeapi(blockfrostprojid):

#blockfrostprojid: blockfrost project ID

    api = BlockFrostApi(
            project_id=blockfrostprojid,

            base_url=ApiUrls.mainnet.value,
    )
    
    return api


def airdropapicall(receiveraddress):
#api call to nftmaker to mint nft BE CAREFUL WITH THIS
#backup here just to be safer. change to live to mint.     
#Can be replaced with other minitng methods  
    backup=1
    if test ==1:
       
       print('THIS IS A TEST MINT')
   
    elif test=='live' and backup=='live':
    
        airdropsender=requests.get(f'https://api.nft-maker.io/MintAndSendRandom/{apikey}/{nftprojectid}/{countnft}/{receiveraddress}')
        print(airdropsender)
   
    else:
        print('No Mint')   







def airdroprandom(policy_id,randomwinnercount=None,ShowMetaData=None ):
    

#policy_id: policy id of project to airdrop to
#randomwinnercount: number of random winners
#ShowMetaData: show metadata during airdrop if 1

    assets = api.assets_policy(policy_id=policy_id) 
    addressesrando=[]
   
    for asset in assets[1:]:

        addressesrando.append(api.asset_addresses(asset=asset.asset)[0].address)      
              
    shufflingdeck = random.sample(addressesrando, len(addressesrando))
    print("Airdrops winners: ")
    

    if ShowMetaData=='y' or ShowMetaData=='yes' or ShowMetaData=='Yes' or ShowMetaData=='Y':
        meta=api.asset(asset.asset)
        args = vars(meta.onchain_metadata)
        print('Metadata of Asset: ')   
        print(args)
           
   
    for q in range(0,int(randomwinnercount)):
        
        receiveraddress=str(shufflingdeck[q])
        print(shufflingdeck[q])
        val = input("Execute API Call for Airdrop? ")

        if val=='y' or val=='yes' or val=='Yes' or val=='Y':
        
            print('NFT-MAKER API Call to MintAndSendRandom...')
            print('Printing API Call Response...')
            temp=airdropapicall(receiveraddress)

        else:
        
            print('No Mint')

    return


def airdropmeta(fulladd, policy_id, whatmeta2=None,whatmeta3=None,ShowMetaData=None ):
    
#fulladd: full address to be printed (yes) or shorted address (no)
#policy_id: policy id of project to airdrop to
#whatmeta2: is the metadata header of choice
#whatmeta3: is the specific metadata value of choice
#ShowMetaData: show metadata during airdrop if 1

    
    
    
    assets = api.assets_policy(policy_id=policy_id)
    
    

    for asset in assets[1:]:
    
        print('Asset Number : ' +str(asset.asset))  
        receiveraddress=str(api.asset_addresses(asset=asset.asset)[0].address)
        
        if fulladd=='yes' or fulladd=='yes' or fulladd=='Yes' or fulladd=='Y'or fulladd=='y':
           
           print('Address of Asset: ' +receiveraddress)
        
        else:
           
           print('Address of Asset: ' +receiveraddress[0:12]+'...'+receiveraddress[-12:-1])
        
        meta=api.asset(asset.asset)
        args = vars(meta.onchain_metadata)    
        
        if ShowMetaData=='y' or ShowMetaData=='yes' or ShowMetaData=='Yes' or ShowMetaData=='Y':
            
            print('Metadata of Asset: ')   
            print(args)
        
  
    
        if args[str(whatmeta2)][0] == str(whatmeta3):

            print('Airdrop : True')
            val = input("Execute API Call for Airdrop? ")
        

            if val=='y' or val=='yes' or val=='Yes' or val=='Y':
                
                print('NFT-MAKER API Call to MintAndSendRandom...')
                print('Printing API Call Response...')
                temp=airdropapicall(receiveraddress)
            
    
        
        elif args[str(whatmeta2)] == whatmeta3:
          
            print('Airdrop : True')
            val = input("Execute API Call for Airdrop? ")
        
        
            if val=='y' or val=='yes' or val=='Yes' or val=='Y':
               
                print('NFT-MAKER API Call to MintAndSendRandom...')
                print('Printing API Call Response...')
                temp=airdropapicall() 
        
        else:
           
            print('Airdrop : False ')            

    

      
        print("\n")
        print("\n")    
        print("\n")
    return



def airdropminttime(timestart, timeend, policy_id,  ShowMetaData=None):
    #timestart:  time for which to start accepting for airdrop (defined at top of page)
    #timeend:   time for which to send accepting for airdrop
    #policy)id: policy id for airdrop
    #ShowMetaData: if meta data should be printed for each airdrop
        
        
        
        
        assets = api.assets_policy(policy_id=policy_id) 
        for asset in assets[1:]:
        
        
            meta=api.asset(asset.asset)
            args = vars(meta.onchain_metadata)  
            print(args['name'])
            transaction=api.asset_transactions(asset=asset.asset)
            datetime_time = datetime.datetime.fromtimestamp(transaction[0].block_time)
            print(datetime_time)
            
            
            if datetime_time > timestart and datetime_time < timeend:
                receiveraddress=str(api.asset_addresses(asset=asset.asset)[0].address) 
                print('Address of Asset: ' +receiveraddress)
                
            
                if ShowMetaData=='y' or ShowMetaData=='yes' or ShowMetaData=='Yes' or ShowMetaData=='Y':
                    meta=api.asset(asset.asset)
                    args = vars(meta.onchain_metadata)
                    print('Metadata of Asset: ')   
                    print(args)
           
                val = input("Execute API Call for Airdrop? ")
                
                if val=='y' or val=='yes' or val=='Yes' or val=='Y':
                   
                    print('NFT-MAKER API Call to MintAndSendRandom...')
                    print('Printing API Call Response...')
                    temp=airdropapicall(receiveraddress) 
            
            else:
               
                print('Airdrop : False ') 



####         Main "program" below       ############



if __name__ == "__main__":
    try:

        api = makeapi(blockfrostprojid)
        print("Welcome to the ShelterPets Airdroper Module!")
        airdrop1 = input("Are you wanting to do an airdrop? Y/N:  ")
        
        if airdrop1=='Y' or airdrop1=='y':
            
            
            print("Airdrop options include: 'metadata' , 'random' , 'minttime'")
            what=input("Choose Airdrop option:   ")
                
            if what=='metadata':
            
                policy_id= input("Policy ID of project to airdrop to?    ")
                assets = api.assets_policy(policy_id=policy_id)
                metaexample=api.asset(assets[1].asset)
                args = vars(metaexample.onchain_metadata)
                print('Example metadata : \n')
                print('\n')
                print('\n')
                print(args)
                print('\n')
                print('\n')
                print('\n')
                whatmeta2=input("Enter metadata header:   ")
                whatmeta3=input('Enter metadata value to send to:   ')
                randomsend=None
                randomwinnercount=None
                fulladd = input("Print full Addresses? Y/N:  ")  
                ShowMetaData=input("Show Meta Data? Y/N:  ")
                airdropmeta(fulladd,str(policy_id), whatmeta2,whatmeta3,ShowMetaData) 
                exit()
            elif what =='random':
            
                policy_id= input("Policy ID of project to airdrop to?    ")
                randomwinnercount=input("Enter number of winners:   ")
                ShowMetaData=input("Show Meta Data? Y/N:  ")
                print('Random send started...')
                airdroprandom(str(policy_id),randomwinnercount,ShowMetaData)
                exit()

            elif what =='minttime':
                
                policy_id= input("Policy ID of project to airdrop to?    ")
                ShowMetaData=input("Show Meta Data? Y/N:  ")
                airdropminttime(timestart, timeend, policy_id,  ShowMetaData)
                exit()
            
            
            else:
                
                print("there are no more options, Goodbye!")
                exit()
          
    except ApiError as e:
        print(e)
