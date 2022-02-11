import time
import requests
from collections import defaultdict
import json
outputaddandid = defaultdict(list)
errordiction = defaultdict(list)
#address .txt should be in same folder as this script
#########GLOBAL VARIABLES##############
#If test = 1, test mint
#if test='live', api will be called .

test='live'


#nftmakerAPI
apikey='nftmakerapikeyhere'

#nftmakerProjectid
nftprojectid='nftprojectidhere'

#nftmakercount
countnft='1'

failedcount=0




def airdropapicall(receiveraddress):
#api call to nftmaker to mint nft BE CAREFUL WITH THIS  


    if test ==1:
       
        airdropsender='THIS IS A TEST MINT'
        print(f'api call:  https://api.nft-maker.io/MintAndSendRandom/{apikey}/{nftprojectid}/{countnft}/{receiveraddress}')
    elif test=='live':
        print(f'api call:  https://api.nft-maker.io/MintAndSendRandom/{apikey}/{nftprojectid}/{countnft}/{receiveraddress}')
        
        airdropsender=requests.get(f'https://api.nft-maker.io/MintAndSendRandom/{apikey}/{nftprojectid}/{countnft}/{receiveraddress}'.strip())
        


    else:
        airdropsender='No Mint'

    return airdropsender



def airdroprandom(addresslist):
#loop through list of addresses and call api for each    
    failedcount=0
    
    for addresscurrent in addresslist:
        try:
            print('\n\n')
            print(f'Address:  {addresscurrent}')
            
            temp=airdropapicall(addresscurrent)
            print(temp)

            if test=='live':
                
                outputaddandid[addresscurrent.strip()].append(str(temp.json()['sendedNft'][0]['id']))
                
            time.sleep(2)
            
        except:
            print('error on this api call')
            errordiction[addresscurrent.strip()].append(str(temp))
            failedcount = failedcount+1
            time.sleep(2)

    return outputaddandid,temp,failedcount,errordiction

if __name__ == "__main__":


    print("Welcome to the ShelterPets Airdroper Module!")
    
    
    
    nameof = str(input('Name of .txt file with address list:  '))
    
    with open(nameof, 'r', encoding='utf-8') as file:
        addresslist = file.readlines()
    print('\n')
    print("Airdrop will start right after this prompt")
    airdrop1 = input("Are you wanting to do an airdrop right now? Y/N:  ")
    if airdrop1=='Y' or airdrop1=='y':
        
        finaldict,response,failedcount,errordiction =airdroprandom(addresslist)

        
        with open(f'output{nameof[0:-4]}.json', 'w') as outfile:
            json.dump(finaldict, outfile)
        if failedcount > 0:
            print(f'failed api call counter: {failedcount}')
            with open(f'output{nameof[0:-4]}failed.json', 'w') as outfile:
                    json.dump(errordiction, outfile)