import datetime
import requests
from collections import defaultdict
import json
from blockfrost import BlockFrostApi, ApiError, ApiUrls
outputaddandid = defaultdict(list)
import binascii




#input output file name here
outputjson='outputspwhite6.json'


#nftmakerAPI
apikey='nftmakerapikeyhere'

#nftmakerProjectid
nftprojectid='projectidhere'

#nftmakercount
countnft='1'

#blockfrost project apikeything
blockfrostprojid='blockfrostapikey'    



#time for print
today = datetime.datetime.now()
d2 = today.strftime("%d/%m/%Y %H:%M:%S")
print(d2)


def makeapi(blockfrostprojid):

#blockfrostprojid: blockfrost project ID

    api = BlockFrostApi(
            project_id=blockfrostprojid,

            base_url=ApiUrls.mainnet.value,
    )
    
    return api

api = makeapi(blockfrostprojid)
data = json.load(open(outputjson))

for key in data.keys():
    for kk in range(len(data[key])):
        nftid=data[key][kk]
        
        state=requests.get(f'https://api.nft-maker.io/GetNftDetailsById/{apikey}/{nftprojectid}/{nftid}')
        assetid=binascii.hexlify(state.json()['name'].encode())
        assetid2=str(state.json()['policyid'])+str(assetid).replace("'", '')[1:]
    
        
        try:
            blockfrost=api.asset(assetid2)
            blockout='| BF Minted: y'
            addresscheck=api.asset_addresses(str(state.json()['policyid'])+str(assetid).replace("'", '')[1:])
            if addresscheck[0].address == key.strip():
                addcheck='Match'
            else:
                addcheck='DO NOT MATCH'
        except:
            blockout='| BF Minted: n'
            addcheck='N/A'
        currentstate=state.json()['state']
        minted=state.json()['minted']
        if minted==True:
            minted1='y'
        elif minted==False:
            minted1='n'

        print(key.strip(),'| id: '+str(data[key][kk]),'| state: ' +str(currentstate),'| NFTMKR minted: '+str(minted1),blockout, '| BF Addr check: ' + str(addcheck))