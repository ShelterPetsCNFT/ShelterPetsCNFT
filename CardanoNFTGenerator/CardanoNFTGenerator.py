#updated 05/2022 

import time
import sys
import requests
import base64
import  json 
from PIL import Image,ImageEnhance, ImageSequence
import random
import os
import numpy as np
from collections import Counter
import pprint
import  logging
from joblib import Parallel, delayed
import multiprocessing






#edit project details in the create project function variable "project"






logging.basicConfig(level=logging.ERROR)
uploadyn=int(input('Do you need any NFTMAKER usage? (0 for no, 1 for yes) '))
print('NFTMAKER disabled by deafualt. Edit code to enable')
uploadyn=0
if uploadyn==1:
    nftmakers=int(input('Do you want to upload to NFTMAKER? (0 for no, 1 for yes) '))
    if nftmakers ==1 :
        apikey= str(input(" Enter NFTMAKERAPI key:   "))
        customerid= str(input(" Enter Customer-Id key:   ")) 
        
imageloc=str(input(" Enter location to save NFTs:   "))+'/'
folder = input(" Enter location of Layers:   ")


if imageloc[0:5]=='\u202a':
    imageloc.strip("\u202a")
if folder[0:5]=='\u202a':
        folder.strip("\u202a")


imagesize1= int(input("Input image output dimension 1 (eg if 400x800 put 400):   "))
imagesize2= int(input("Input image output dimension 2 (eg if 400x800 put 800):   "))



gifs=int(input('input 1 if there are gifs, 0 if not: '))
if gifs==1:
                                   
    gifindex=int(input('input gif index: '))
    gifontop=int(input('input 1 if gif on top, zero otherwise: '))  
else:
    gifindex=''
    gifontop=''
    
    
def create_project(namelistr, newproj):
    
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
        metalistheader=''
        for namer in namelistr:
            metadatastring['721']['<policy_id>']['<asset_name>'][namer]=f'<{namer}>'
            
    

    admeta=input('additional constant metadata values (not based on layers)? Y/N  ')
    if admeta=='y' or admeta == 'Y':
        
        howmany=input('How many more?  ')
        metvalue=[]
        headername=[]
        print('63 character limit for values')
        for tt in range(0,int(howmany)):
            headername.append(input('Header name:  '))
            metvalue.append(input(f'Value for {headername[tt]}:  '))
            metadatastring['721']['<policy_id>']['<asset_name>'][headername[tt]]=f'{metvalue[tt]}'
            print('\n')
            pprint.pprint(metadatastring)
            print('\n')
    else:
        
        metvalue=[]
        headername=[]    
    
    removemeta=input('Remove layer values from metadata? Y/N  ')
    if removemeta=='y' or removemeta == 'Y':
        if listoflist=='y' or listoflist=='Y':
            
            headername1=[]

            conta=0
            howmany=input('How many?  ')
            for tt in range(0,int(howmany)):
                headername1.append(input('Header name:  '))
                del metadatastring['721']['<policy_id>']['<asset_name>'][metalistheader][headername1[conta]]
                print('\n')
                pprint.pprint(metadatastring)
                print('\n')    
                conta=conta+1
        
        
        else:
            headername1=[]

            conta=0
            howmany=input('How many?  ')
            for tt in range(0,int(howmany)):
                headername1.append(input('Header name:  '))
                del metadatastring['721']['<policy_id>']['<asset_name>'][headername1[conta]]
                print('\n')
                pprint.pprint(metadatastring)
                print('\n')    
                conta=conta+1
    
    
    else:

        headername1=[]
    
    
    metadatastringjson=json.dumps(metadatastring)
    metadatastringexport=metadatastring
    if newproj == 'y' or newproj =='Y':
        namer=input('NFTMAKER Project Name:  ')
    else:
        namer=''
    project={
          "projectname": str(namer),
          "description": "",
          "projecturl": "",
          "tokennamePrefix": "",
          "policyExpires": True,
          "policyLocksDateTime": "2022-12-31T21:33:38.286Z",
          "maxNftSupply": 1,
          "metadata": str(metadatastringjson),
          "addressExpiretime": 20
        }
    
    if newproj == 'y' or newproj =='Y':
        r = requests.post(f'https://api.nft-maker.io/CreateProject/{apikey}', json=project)
        nftmakprojid=r.json()['projectId']
        print(r.json()['projectId'])
    else:
        nftmakprojid=''
    return nftmakprojid,listoflist, metadatastringexport, metalistheader,headername,metvalue,headername1
    
    
def create_meta(item, listoflist, metadatastring, metalistheader, nftname,headername,metvalue, assetname):

    metadatastring={"721": {"<policy_id>": {"<asset_name>":{}}, "version": "1.0"}}
        
        
    filler={"name": nftname, "image": "<ipfs_link>", "mediaType": "<mime_type>",
        
         "files": [{"name": nftname, "mediaType": "<mime_type>", "src": "<ipfs_link>"}]}    
    
    
    metadatastring['721']['<policy_id>']={"<asset_name>": {}}
    

    
    
    if listoflist=='y' or listoflist=='Y':
        tempdic={}

        
        for items in item.keys():
            tempdic[items]=f'{item[items]}'
        filler[metalistheader]=tempdic
        metadatastring['721']['<policy_id>']["<asset_name>"]=filler
        for tt in range(0,len(headername)):

            metadatastring['721']['<policy_id>']['<asset_name>'][headername[tt]]=f'{metvalue[tt]}'
        
    else:

        for items in item.keys():
            filler[items]=f'{item[items]}'
            metadatastring['721']['<policy_id>']["<asset_name>"]=filler
        for tt in range(0,len(headername)):

            metadatastring['721']['<policy_id>']['<asset_name>'][headername[tt]]=f'{metvalue[tt]}'
          
      
    # assetnamedic = metadatastring['721']['<policy_id>']['<asset_name>']   
    # del metadatastring['721']['<policy_id>']
    # metadatastring['721']['<policy_id>']={assetname: assetnamedic, "version": "1.0"}
    
    return metadatastring
    
    
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


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def generate_unique_images(a,amount, config,countaaa,traitorder,metadataPlaceholder,namelistr,traitcount, imageloc,projectname,previousimage,leadingzero, assetname,uploadyn,headername,metvalue,loadmetadata,metalistheader,newproj,layeropac,nftprojectid,headername1,listoflist):

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
        print("loading metadata from nftmaker")
    
    

    elif loadmetadata=='y' or loadmetadata=='y':
        if newproj != 'y' and newproj !='Y':
        
            nftprojectid=input('Input NFT-MAKER Project ID:  ')
        countmeta= requests.get(f'https://api.nft-maker.io/GetProjectDetails/{apikey}/{customerid}/{nftprojectid}')
        countmeta=str(countmeta.json()['total'])


        metanames=requests.get(f'https://api.nft-maker.io/GetNfts/{apikey}/{nftprojectid}/all/{countmeta}/1')
                                 
        nftmakerdata=[]
        
        for nn in range(0,len(metanames.json())):
            nftid=metanames.json()[nn]['id']
            tempdata=requests.get(f'https://api.nft-maker.io/GetNftDetailsById/{apikey}/{nftprojectid}/{nftid}')
            

            tempdata=tempdata.json()
            aaa=json.loads(tempdata['metadata'])
            plcyid=tempdata['policyid']
            for key in aaa['721'][plcyid].keys():
                asstnam=str(key)
            if metalistheader != '':
                temper=aaa['721'][plcyid][asstnam][metalistheader]
                nftmakerdata.append(temper)
            else:
                templist={}
                for namer in namelistr:
                    templist[namer]=aaa['721'][plcyid][asstnam][namer]
                nftmakerdata.append(templist)
        
        all_images = nftmakerdata
        counter=len(nftmakerdata)
    
    
    
    else:
        all_images = []
        counter=0
    namenum=[] 
    nameimage=[]
    for i in range(amount): 
        new_trait_image = create_new_image(all_images, config)
        all_images.append(new_trait_image)
        namenum.append(i+countaaa)
        nameimage.append([i+countaaa,new_trait_image])    
    
    
    
    names1=all_images[0].keys()
    counter2=len(all_images)
    totalcounter2=[]

        
    for key in all_images[0].keys():
        counts2=[]
        for i in range(counter2):
            counts2.append(all_images[i][f'{key}'])
        
        totalcounter2.append(Counter(counts2[:]))
    tempnames=[]
    for tempname in names1:
        tempnames.append(tempname)
    ii=0
    for count in totalcounter2:
        
        
        print(tempnames[ii])
        print('\n')
        for key, value in count.items():
            print(key, '{:.2%}'.format(value/counter2))
        print('\n')
        ii=ii+1
    
    input('These are the resulting weights, Press Enter to generate images')
    print('images are generating (and uploading if selected)...')
    

    
    def imagesaver(inputlist):
        
        item=inputlist[1]
        namenum=inputlist[0]
        for i in range(0,len(a['previewImageNft']['metadataPlaceholder'])):
            
            a['previewImageNft']['metadataPlaceholder'][i]['value']=item[namelistr[i]]
            
        layers = [];

        for index, attr in enumerate(item):

            if attr != 'tokenId':
                layers.append([])
                if gifs==1 and index==gifindex:
                    layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.gif')
                else:
                    layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')
                if opac=='y' or opac=='Y':
                    layers[index]=reduce_opacity(layers[index], layeropac[index]/255)

        
        if len(layers) == 1:
            
            if gifs==1:
                
                rgb_im = layers[0].convert('RGB')
                maxsize=(imagesize1,imagesize2)
                rgb_im.thumbnail(maxsize)
                
    
                
                nftname=projectname+str(namenum).zfill(leadingzero)
    
                file_name = nftname + ".gif"
                print(file_name, flush=True)
                rgb_im.save(imageloc + file_name, save_all=True, append_images=rgb_im[1:], duration=250, loop=0)
            
            else:
            
                rgb_im = layers[0].convert('RGB')
                maxsize=(imagesize1,imagesize2)
                rgb_im.thumbnail(maxsize)
                
    
                
                nftname=projectname+str(namenum).zfill(leadingzero)
    
                file_name = nftname + ".png"
                print(file_name, flush=True)
                rgb_im.save(imageloc + file_name)

            
       
        elif len(layers) == 2:
            
            
            if gifs==1:
                if gifontop==1:
                    
                    imagelayer   = layers[0]#.convert('RGBA')
                   
                    animated_gif = layers[1]
                    
                    all_frames = []
                    
                    for gif_frame in ImageSequence.Iterator(animated_gif):
                    
                        # duplicate background image because we will change it
                        new_frame = imagelayer.copy()  
                    
                        # need to convert from `P` to `RGBA` to use it in `paste()` as mask for transparency
                        gif_frame = gif_frame.convert('RGBA')  
                    
                        # paste on background using mask to get transparency 
                        new_frame.paste(gif_frame, mask=gif_frame) 
                        
                        all_frames.append(new_frame)
                        
                    # save all frames as animated gif
                    
                    

                        
                    # save all frames as animated gif
                    
                    nftname=projectname+str(namenum).zfill(leadingzero)
                    rgb_im = all_frames[0].convert('RGB')
                    file_name = nftname + ".gif"
                    rgb_im.save(imageloc + file_name, save_all=True, append_images=all_frames, duration=200, loop=0)
                
                
                
                
                elif gifontop==0:
                    imagelayer   = layers[1]#.convert('RGBA')
                   
                    animated_gif = layers[0]
                    
                    all_frames = []
                    
                    for gif_frame in ImageSequence.Iterator(animated_gif):
                    
                        # duplicate background image because we will change it
                        new_frame = imagelayer.copy()  
                    
                        # need to convert from `P` to `RGBA` to use it in `paste()` as mask for transparency
                        gif_frame = gif_frame.convert('RGBA')  
                    
                        # paste on background using mask to get transparency 
                        gif_frame.paste(new_frame, mask=new_frame) 
                        
                        all_frames.append(gif_frame)
                        
                    # save all frames as animated gif
                        
                    nftname=projectname+str(namenum).zfill(leadingzero)
                    rgb_im = all_frames[0].convert('RGB')
                    file_name = nftname + ".gif"
                    print(file_name, flush=True)
                    rgb_im.save(imageloc + file_name, save_all=True, append_images=all_frames[1:], duration=200, loop=0)
            
            
            else:
                    
            
                main_composite = Image.alpha_composite(layers[0], layers[1])
                rgb_im = main_composite.convert('RGB')
                maxsize=(imagesize1,imagesize2)
                rgb_im.thumbnail(maxsize)
                
    
                
                nftname=projectname+str(namenum).zfill(leadingzero)
    
                file_name = nftname + ".png"
                print(file_name, flush=True)
                rgb_im.save(imageloc + file_name)

                 
        elif len(layers) >= 3:
            
            
            
            if gifs==1:
                
                main_composite = Image.alpha_composite(layers[0], layers[1])
                layers.pop(0)
                layers.pop(0)
    
                for index, remaining in enumerate(layers[:-1]):
    
                    main_composite = Image.alpha_composite(main_composite, remaining)
                    
                    
                if gifontop==1:
                    
                    imagelayer   = main_composite
                   
                    animated_gif = layers[-1]
                    
                    all_frames = []
                    
                    for gif_frame in ImageSequence.Iterator(animated_gif):
                    
                        # duplicate background image because we will change it
                        new_frame = imagelayer.copy()  
                    
                        # need to convert from `P` to `RGBA` to use it in `paste()` as mask for transparency
                        gif_frame = gif_frame.convert('RGBA')  
                    
                        # paste on background using mask to get transparency 
                        new_frame.paste(gif_frame, mask=gif_frame) 
                        
                        all_frames.append(new_frame)
                        
                    # save all frames as animated gif
                    
                    

                        
                    # save all frames as animated gif
                    
                    nftname=projectname+str(namenum).zfill(leadingzero)
                    rgb_im = all_frames[0].convert('RGB')
                    file_name = nftname + ".gif"
                    rgb_im.save(imageloc + file_name, save_all=True, append_images=all_frames, duration=200, loop=0)
                
                
                
                
                elif gifontop==0:
                    imagelayer   = main_composite
                   
                    animated_gif = layers[-1]
                    
                    all_frames = []
                    
                    for gif_frame in ImageSequence.Iterator(animated_gif):
                    
                        # duplicate background image because we will change it
                        new_frame = imagelayer.copy()  
                    
                        # need to convert from `P` to `RGBA` to use it in `paste()` as mask for transparency
                        gif_frame = gif_frame.convert('RGBA')  
                    
                        # paste on background using mask to get transparency 
                        gif_frame.paste(new_frame, mask=new_frame) 
                        
                        all_frames.append(gif_frame)
                        
                    # save all frames as animated gif
                        
                    nftname=projectname+str(namenum).zfill(leadingzero)
                    rgb_im = all_frames[0].convert('RGB')
                    file_name = nftname + ".gif"
                    print(file_name, flush=True)
                    rgb_im.save(imageloc + file_name, save_all=True, append_images=all_frames[1:], duration=200, loop=0)
            
            
            else:
            
            
            
                main_composite = Image.alpha_composite(layers[0], layers[1])
                layers.pop(0)
                layers.pop(0)
    
                for index, remaining in enumerate(layers):
    
                    main_composite = Image.alpha_composite(main_composite, remaining)
    
                rgb_im = main_composite.convert('RGB')
                maxsize=(imagesize1,imagesize2)
                rgb_im.thumbnail(maxsize)
                
    
                
                nftname=projectname+str(namenum).zfill(leadingzero)
    
                file_name = nftname + ".png"
                print(file_name, flush=True)
                rgb_im.save(imageloc + file_name)

           
       
        a['assetName']=assetname+str(namenum).zfill(leadingzero)
        a['previewImageNft']['displayname']=projectname+str(namenum).zfill(leadingzero)
        
        for i in range(0,len(a['previewImageNft']['metadataPlaceholder'])):
            if (a['previewImageNft']['metadataPlaceholder'][i]['name'] in headername1):
            
                del a['previewImageNft']['metadataPlaceholder'][i]

                

        bb=create_meta(item, listoflist, metadatastring,metalistheader,nftname,headername,metvalue, assetname)
        metadatasave=bb
        for head in headername1:
            del metadatasave['721']['<policy_id>']['<asset_name>'][head]
        
        with open(imageloc + nftname +'.metadata', 'w') as outfile:
            json.dump(metadatasave, outfile,indent=2)
        if uploadyn == 1:
            
            if gifs==1:
                with open(imageloc + nftname + ".gif", "rb") as img_data:
                    
                    data1 = base64.b64encode(img_data.read())
                    a['previewImageNft']['fileFromBase64']=data1.decode('utf-8')
                    errorsapi=[]
                    r=requests.post(f'https://api.nft-maker.io/UploadNft/{apikey}/{nftprojectid}', json=a)
                    if r.ok:
                        pass
                    else:
                        errorsapi.append(f'{imageloc}{nftname}.png')
            
            else:
            
                with open(imageloc + nftname + ".png", "rb") as img_data:
                    
                    data1 = base64.b64encode(img_data.read())
                    a['previewImageNft']['fileFromBase64']=data1.decode('utf-8')
                errorsapi=[]
                r=requests.post(f'https://api.nft-maker.io/UploadNft/{apikey}/{nftprojectid}', json=a)
                if r.ok:
                    pass
                else:
                    errorsapi.append(f'{imageloc}{nftname}.png')
        return 

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(imagesaver)(xx) for xx in nameimage[counter:])
    
    

    
    
    return all_images
 

try:  

    print("Welcome to ShelterPets Cardano NFT Generator")

    sys.setrecursionlimit(1500)
    
    
    projectname=input('Display name for NFT (ShelterPets# for example): ')
    assetname=input('Assetname for NFT (ShetlerPets for example):')
    if uploadyn==1:
        newproj=input('New project: Y/N?  ')
    else:
        newproj=''
    if newproj != 'y' and newproj !='Y':
        if uploadyn == 1: 
            nftprojectid=input('Input NFT-MAKER Project ID:  ')

       
    if gifs==1:
        a={
          "assetName": "string",
          "previewImageNft": {
            "mimetype": "image/gif",
            "fileFromBase64": "string",
            "displayname": "string",
            "metadataPlaceholder": [ 
            ]
          }
        }
    else:
        a={
          "assetName": "string",
          "previewImageNft": {
            "mimetype": "image/png",
            "fileFromBase64": "string",
            "displayname": "string",
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
    
    loadmetadata=''
    # value='name'
    # d[f'{value}']='name'
    # metadataPlaceholder.append(d)
    a['previewImageNft']['metadataPlaceholder']=metadataPlaceholder
    
    if newproj == 'y' or newproj =='Y':
        nftprojectid,listoflist, metadatastring, metalistheader, headername,metvalue,headername1=create_project(namelistr,newproj)
        previousimage=0
    else:
        nftprojectid=''
        nftprojectid1,listoflist, metadatastring, metalistheader, headername,metvalue, headername1=create_project(namelistr,newproj)
        
        previousimage=input('Have you previously used this uploader before on this project? Y/N?  ')
        if previousimage == 'y' or previousimage == 'y':
            previousimage=1
            loadmetadata=''
        else:
        
            # loadmetadata=input('Do you want to load and check a NFTMAKER projects metadata? Y/N?  ')
            loadmetadata=''
            previousimage=0
            


    totalimages=int(input("total images:  "))
    totalimages=totalimages+1
    leadingzero=int(input('How many leading zeros in nft name?  '))
    leadingzero=leadingzero+1

    
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
    opac=input('Opacity values for layers? Y/N?  ')
    layeropac=[]
    if opac=='y' or opac=='Y':
        for tempnamelist in namelistr:
            layeropac.append(int(input(f'Enter alpha values for Header: {tempnamelist} (between 0, 255)  ')))
    
    
    for k in range(0, len(sub_folders)):
        
        
        size=(len(traitnames[k]))

        
        if weightrand== 'True' or weightrand== 'true' or weightrand== 't':
                weight=np.random.dirichlet(np.ones(len(traitnames[k])),size=1)*100
                weight=weight.tolist()
                layerslist[k]=   {
                          "name": namelistr[k],
                          "values": traitnames[k],
                          "trait_path": sub_folders2[k],
                          "filename": traitnames[k],
                          "weights": weight[0]
                        }
        elif weightrand== 'False' or weightrand== 'false' or weightrand== 'f':
            print(f'List of traits for {namelistr[k]}:')
            print('\n')
            print(traitnames[k])
            print('\n')
            weight = [float(input(f'Enter weight values for Header: {namelistr[k]} and Trait: ({traitnames[k][qq]}): ')) for qq in range(size)]
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
                weight = [float(input(f'Enter weight values for Header: {namelistr[k]} and Trait: ({traitnames[k][qq]}): ')) for qq in range(size)]
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
            print('No option selected for weights, exiting..')
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

    # for incomp in config["incompatibilities"]:
    #     for attr in new_image:
    #         if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
    #             return create_new_image(all_images, config)

            
            
    layersdict=  {
      "layers": layerslist
      ,
      "incompatibilities": incompat,
      "baseURI": ".",
      "name": str(assetname)
    }


    countaaa=int(input('NFT name start number (for example, ShelterPets#005 would be 5):  '))
        
    keyindex=countaaa+1
    outputmeta=generate_unique_images(a,totalimages-1, layersdict,countaaa,traitorder,metadataPlaceholder, namelistr,traitcount,imageloc,projectname,previousimage,leadingzero, assetname, uploadyn, headername,metvalue, loadmetadata,metalistheader,newproj,layeropac,nftprojectid,headername1,listoflist)   


    
    with open(projectname+'metadata.json', 'w') as fout:
        json.dump(outputmeta, fout)

    print('metadata list printed to '+ str(projectname)+'metadata.json in current directory')
    print('Upload Complete')
    press=input('Hit enter to save collection rarity data')
    
    
    with open('Rarityinfo.txt','w') as outfile:
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
        for count in totalcounter:
            
            
            print(str(tempnames[ii]), file=outfile)
            print('\n', file=outfile)
            for key, value in count.items():
                print(str(key), str('{:.2%}'.format(value/counter)), file=outfile)
            print('\n', file=outfile)
            ii=ii+1
    
    press=input('Hit enter to exit')


except:
    logging.exception("Something has gone wrong, please evaluate the error listed below")
    time.sleep(5)
    print("program closing in 25 seconds...")
    time.sleep(25)
