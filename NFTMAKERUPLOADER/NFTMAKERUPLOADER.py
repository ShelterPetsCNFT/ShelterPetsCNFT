import requests
import pandas
import time
import sys
import requests
import json
import base64
from PIL import Image
from io import BytesIO
import requests, json 
import requests
from PIL import Image
import random
import json
import os
import shutil
import numpy as np

#edit project details in the create project fucntion variable "project"


os.system('cls||clear')

countaaa=0

metadataloc='' 
apikey= str(input(" Enter NFTMAKERAPI key:   "))
imageloc=str(input(" Enter location to save NFTs:   "))+'/'
folder = input(" Enter location of Layers:   ")





def create_project(namelistr):

    metadatastring={"721": {"<policy_id>":
         {"<asset_name>": 
        {"name": "<display_name>", "image": "<ipfs_link>", "mediaType": "<mime_type>",
        
         "files": [{"name": "<display_name>", "mediaType": "<mime_type>", "src": "<ipfs_link>"}]}}, "version": "1.0"}}

        
 
    for namer in namelistr:
        metadatastring['721']['<policy_id>']['<asset_name>'][namer]=f'<{namer}>'
    
    admeta=input('additional constant metadata values (not based on layers)? Y/N  ')
    if admeta=='y' or admeta == 'Y':
        howmany=input('How many more?  ')
        metvalue=[]
        for tt in range(0,int(howmany)):
            headername=input('Header name:  ')
            metvalue=input(f'Value for {headername}:  ')
            metadatastring['721']['<policy_id>']['<asset_name>'][headername]=f'{metvalue}'
            print(metadatastring)
    
    namer=input('NFTMAKER Project Name:  ')
    project={
          "projectname": str(namer),
          "description": "",
          "projecturl": "",
          "tokennamePrefix": "",
          "policyExpires": True,
          "policyLocksDateTime": "2022-12-31T21:33:38.286Z",
          "maxNftSupply": 1,
          "metadata": str(metadatastring),
          "addressExpiretime": 20
        }

    r = requests.post(f'https://api.nft-maker.io/CreateProject/{apikey}', json=project)
    print(r.json()['projectId'])
    return r.json()['projectId']

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
        new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    for incomp in config["incompatibilities"]:
        for attr in new_image:
            if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
                return create_new_image(all_images, config)

    if new_image in all_images:
        return create_new_image(all_images, config)
    else:
        return new_image


def generate_unique_images(a,amount, config,countaaa,traitorder,metadataPlaceholder,namelistr,traitcount, metadataloc, imageloc,projectname):

    trait_files = {}
    for trait in config["layers"]:
        trait_files[trait["name"]] = {}
        for x, key in enumerate(trait["values"]):
            trait_files[trait["name"]][key] = trait["filename"][x];

    all_images = []
    for i in range(amount): 
        new_trait_image = create_new_image(all_images, config)
        all_images.append(new_trait_image)


    for item in all_images:
  
        for i in range(0,int(traitcount)):
            
            a['previewImageNft']['metadataPlaceholder'][i]['value']=item[namelistr[i]]
            
        layers = [];

        for index, attr in enumerate(item):

            if attr != 'tokenId':
                layers.append([])
                layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

        if len(layers) >= 3:
            main_composite = Image.alpha_composite(layers[0], layers[1])
            layers.pop(0)
            layers.pop(0)

            for index, remaining in enumerate(layers):

                main_composite = Image.alpha_composite(main_composite, remaining)

            rgb_im = main_composite.convert('RGB')
            maxsize=(1500,1500)
            rgb_im.thumbnail(maxsize)
            nftname=projectname+str(namenumber[countaaa]).zfill(4)

            file_name = nftname + ".png"
            print(file_name)
            rgb_im.save(imageloc + file_name)

            countaaa=countaaa+1
       
        a['assetName']=nftname
        with open(imageloc + nftname + ".png", "rb") as img_data:
            
            data1 = base64.b64encode(img_data.read())
            a['previewImageNft']['fileFromBase64']=data1.decode('utf-8')
        
        r = requests.post(f'https://api.nft-maker.io/UploadNft/{apikey}/{nftprojectid}', json=a)

 

  
print("Welcome to ShelterPets Uploader")
print("Are you wanting to upload an NFT?")   



yesno=input('yes or no? ')
if yesno=='yes' or yesno=='yes' or yesno=='Yes' or yesno=='Y'or yesno=='y':
    
    
    
    projectname=input('Base name for NFT (ShelterPets for example): ')
    newproj=input('New project: Y/N?  ')
    if newproj != 'y' and newproj !='Y':
       nftprojectid=input('Input NFT-MAKER Project ID:  ')
       
    a={
      "assetName": "string",
      "previewImageNft": {
        "mimetype": "image/png",
        "fileFromBase64": "string",
        "metadataPlaceholder": [ 
        ]
      }
    }

    d={}
    namelistr=[]
    traitorder=[]
    traitcount=input('Number of traits:  ')
    metadataPlaceholder=[]
    print('enter traits from back to front')
    for i in range(0,int(traitcount)):
        name=input('name:  ')
        namelistr.append(name)
        value='name'
        d[f'{value}']=name
        metadataPlaceholder.append(d)
        d={}
    a['previewImageNft']['metadataPlaceholder']=metadataPlaceholder
    
    if newproj == 'y' or newproj =='Y':
        nftprojectid=create_project(namelistr)

    shutil.rmtree(imageloc)
    os.mkdir(imageloc)


    totalimages=int(input("total images:  "))
    totalimages=totalimages+1
    
    
    namenumber=random.sample(range(1,totalimages,1), totalimages-1)
    
    traitnames=[]
    sub_folders2=[]
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    sub_folders =namelistr
    for i in range(0,len(sub_folders),1):
        
        sub_folders2.append(folder+'/'+sub_folders[i])
        

    for j in range(0,len(sub_folders),1):
            l=os.listdir(sub_folders2[j])
            li=[x.split('.')[0] for x in l]
            traitnames.append(li)


    layerslist=[[] for i in range(len(sub_folders))]
    weightrand=input('Random Weights ( True or False): ')
    for k in range(0, len(sub_folders)):
        
        
        size=(len(traitnames[k]))

        
        if weightrand== 'True':
                weight=np.random.dirichlet(np.ones(len(traitnames[k])),size=1)*100
                weight=weight.tolist()
                layerslist[k]=   {
                          "name": namelistr[k],
                          "values": traitnames[k],
                          "trait_path": sub_folders2[k],
                          "filename": traitnames[k],
                          "weights": weight[0]
                        }
        elif weightrand== 'False':
            print(f'List of traits for {namelistr[k]}:')
            print('\n')
            print(traitnames[k])
            print('\n')
            weight = [int(input(f'Enter weight values for Header: {namelistr[k]} and Trait: ({traitnames[k][qq]}): ')) for qq in range(size)]
            if sum(weight)==100:
                print('\n')
                layerslist[k]=   {
                          "name": namelistr[k],
                          "values": traitnames[k],
                          "trait_path": sub_folders2[k],
                          "filename": traitnames[k],
                          "weights": weight
                        }
            else:
                print('Weight doesnt sum to 100')
                print('\n')
                print('try again: 1 more attempt or program will exit')
                weight = [int(input(f'Enter weight values for Header: {namelistr[k]} and Trait: ({traitnames[k][qq]}): ')) for qq in range(size)]
                if sum(weight)==100:
                    print('\n')
                    layerslist[k]=   {
                          "name": namelistr[k],
                          "values": traitnames[k],
                          "trait_path": sub_folders2[k],
                          "filename": traitnames[k],
                          "weights": weight
                        }
                else:
                    print('Weight doesnt sum to 100')
                    time.sleep(10)
                    exit()
        else:
            print('No option selected, exiting..')
            time.sleep(10)
            exit()
        
        
        




    incompat=[
        # {
        #   "layer": "Toy",
        #   "value": "Mouse Gold",
        #   "incompatible_with": ["Green Fish", "Orange Fish","Pink Fish"]
        # },  #  Blue backgrounds will never have the attribute "Python Logo 2".

        # {
        #   "layer": "Toy",
        #   "value":"Mouse Gray", 
        #   "incompatible_with": ["Green Fish", "Orange Fish","Pink Fish"]
        # },  #  Blue backgrounds will never have the attribute "Python Logo 2".
        # {
        #   "layer": "Toy",
        #   "value": "Mouse Red",
        #   "incompatible_with": ["Green Fish", "Orange Fish","Pink Fish"]
        # },  #  Blue backgrounds will never have the attribute "Python Logo 2".


        # {
        #   "layer": "Toy",
        #   "value":  "Mouse White",
        #   "incompatible_with": ["Green Fish", "Orange Fish","Pink Fish"]
        # },  #  Blue backgrounds will never have the attribute "Python Logo 2".

      ]



    layersdict=  {
      "layers": layerslist
        
      ,
      "incompatibilities": incompat,
      "baseURI": ".",
      "name": "NFT #"
    }






    generate_unique_images(a,totalimages-1, layersdict,countaaa,traitorder,metadataPlaceholder, namelistr,traitcount,metadataloc,imageloc,projectname)   
    print('Upload Complete')
    press=input('Hit enter to Exit')

   
