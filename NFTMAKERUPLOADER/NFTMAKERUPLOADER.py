
import pandas as pd
import time
import sys
import requests
import base64
from io import BytesIO
import requests, json 
from PIL import Image
import random
import os
import shutil
import numpy as np
import csv
#edit project details in the create project fucntion variable "project"
from collections import Counter
import pprint
os.system('cls||clear')


##config input used for testing, can be activate##
# fileloc=input('Location of user config:  ')
        
# inputs = []
# with open(fileloc, newline='') as inputfile:
    # for row in csv.reader(inputfile):
        # inputs.append(row[0])

# print(inputs)          


# apikey= inputs[0]
# customerid= inputs[1]

# imageloc=str(inputs[2])+'/'
# folder = inputs[3]
import sys, traceback, logging

logging.basicConfig(level=logging.ERROR)


apikey= str(input(" Enter NFTMAKERAPI key:   "))
customerid= str(input(" Enter Customer-Id key:   "))

imageloc=str(input(" Enter location to save NFTs:   "))+'/'
folder = input(" Enter location of Layers:   ")


imagesize= int(input("Input image output dimension (eg if 400x400 put 400):   "))
  

def create_project(namelistr):

    metadatastring={"721": {"<policy_id>":
         {"<asset_name>": 
        {"name": "<display_name>", "image": "<ipfs_link>", "mediaType": "<mime_type>",
        
         "files": [{"name": "<display_name>", "mediaType": "<mime_type>", "src": "<ipfs_link>"}]}}, "version": "1.0"}}

        
 
    listoflist=input('Do you want all variable metadata values stored in a single header? Y/N  ')
    if listoflist=='y' or listoflist=='Y':
        metalistheader=str(input('Input name of metadata header:  '))
        tempdic={}
        for namer in namelistr:
            tempdic[namer]=f'<{namer}>'
        metadatastring['721']['<policy_id>']['<asset_name>'][metalistheader]=tempdic
    else:
    
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
            print('\n')
            pprint.pprint(metadatastring)
            print('\n')
    
    
    
    
    
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


def generate_unique_images(a,amount, config,countaaa,traitorder,metadataPlaceholder,namelistr,traitcount, imageloc,projectname,previousimage,leadingzero):

    trait_files = {}
    for trait in config["layers"]:
        trait_files[trait["name"]] = {}
        for x, key in enumerate(trait["values"]):
            trait_files[trait["name"]][key] = trait["filename"][x];
    if previousimage==1:
        
        metaname=input(f'Is {str(projectname)}metadata.json the correct filename from previous upload? Y/N?  ')
        if metaname == 'y' or metaname =='Y':  
            f = open(str(projectname+'metadata.json'))
        
        elif metaname == 'n' or metaname =='N': 

            fileloc1=input('Location of previous metadata:  ')
            f = open(str(fileloc1))
         
        else:
            print('something went wrong')
            time.sleep(5)
            exit()
            
        data = json.load(f)
        all_images = data
        counter=len(data)
    else:
        all_images = []
        counter=0
        
    for i in range(amount): 
        new_trait_image = create_new_image(all_images, config)
        all_images.append(new_trait_image)


    for item in all_images[counter:]:
  
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
            maxsize=(imagesize,imagesize)
            rgb_im.thumbnail(maxsize)
            

            
            nftname=projectname+str(countaaa).zfill(leadingzero)

            file_name = nftname + ".png"
            print(file_name)
            rgb_im.save(imageloc + file_name)

            countaaa=countaaa+1
       
        a['assetName']=nftname
        with open(imageloc + nftname + ".png", "rb") as img_data:
            
            data1 = base64.b64encode(img_data.read())
            a['previewImageNft']['fileFromBase64']=data1.decode('utf-8')
        
        r = requests.post(f'https://api.nft-maker.io/UploadNft/{apikey}/{nftprojectid}', json=a)
    return all_images
 

try:  

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
            previousimage=0
        else:
            previousimage=1
        shutil.rmtree(imageloc)
        os.mkdir(imageloc)


        totalimages=int(input("total images:  "))
        totalimages=totalimages+1
        leadingzero=int(input('How many leading zeros in nft name?  '))
        leadingzero=leadingzero+1
        #namenumber=random.sample(range(1,totalimages,1), totalimages-1)
        
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





        countaa= requests.get(f'https://api.nft-maker.io/GetProjectDetails/{apikey}/{customerid}/{nftprojectid}')
        countaaa=countaa.json()['total']+1
        keyindex=countaaa+1
        outputmeta=generate_unique_images(a,totalimages-1, layersdict,countaaa,traitorder,metadataPlaceholder, namelistr,traitcount,imageloc,projectname,previousimage,leadingzero)   


        
        with open(projectname+'metadata.json', 'w') as fout:
            json.dump(outputmeta, fout)

        print('metadata list printed to '+ str(projectname)+'metadata.json in current directory')
        print('Upload Complete')
        press=input('Hit enter to view collection data')
        
        
        class Transcript(object):

            def __init__(self, filename):
                self.terminal = sys.stdout
                self.logfile = open(filename, "w")

            def write(self, message):
                self.terminal.write(message)
                self.logfile.write(message)

            def flush(self):
                # this flush method is needed for python 3 compatibility.
                # this handles the flush command by doing nothing.
                # you might want to specify some extra behavior here.
                pass

        def start(filename):
            """Start transcript, appending print output to given filename"""
            sys.stdout = Transcript(filename)

        def stop():
            """Stop transcript and return print functionality to normal"""
            sys.stdout.logfile.close()
            sys.stdout = sys.stdout.terminal






        start('Rarityinfo.txt')
        
        
        
        
        data = outputmeta
        names=data[0].keys()
        counter=len(data)
        totalcounter=[]

            
        for key in data[0].keys():
            counts=[]
            for i in range(counter):
                counts.append(data[i][f'{key}'])
            
            totalcounter.append(Counter(counts[:]))
        tempnames=[]
        for tempname in names:
            tempnames.append(tempname)
        ii=0
        #print(totalcounter)
        for count in totalcounter:
            
            
            print(tempnames[ii])
            print('\n')
            for key, value in count.items():
                print(key, '{:.2%}'.format(value/counter))
            print('\n')
        ii=ii+1
        stop()
        press=input('Hit enter to exit')










except:
    logging.exception("Something has gone wrong, please evaluate the error listed below")
    time.sleep(5)
    print("program closing in 25 seconds...")
    time.sleep(25)
    stop()
