#################################
# NFT Collection images parser
# FMC for GoNifty
# twitter.com/filmakarov
# 2021
##################################

from urllib.request import urlopen
import json
import urllib.request
import os
from tqdm import tqdm
import concurrent.futures as cf
import time
from tqdm import tqdm

start_time = time.time()

########################  CONFIG ####################

#collection baseuri
#baseuri = "https://raw.githubusercontent.com/recklesslabs/wickedcraniums/main/"
#baseuri = "https://deekhash.xyz/json/"
baseuri = "https://cloudflare-ipfs.com/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/"

# size of collection
# do not change when parsing a collection after stop
COLLECTION_SIZE = 20;  

#can continue from last stop
#0 = from beginning
START_FROM = 0;

# switch to false if you want to continue from previously parsed txt file
parse_json = True

#image extension
EXTENSION = ".png"
#folder 
FOLDER = "images/bgapes/originals"

jsonworkers = 4

# usually 4 is ok, but it you get Connection refused error, try less
imageworkers = 1

#########################################################

#create nested folder
if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

tokenuris = []
img_uris = []
filepaths = []

print ("SCRAPING COLLECTION " + FOLDER)

#create arrays for token uris and file paths
for i in tqdm(range(START_FROM, COLLECTION_SIZE)):
        tokenuris.append(baseuri + str(i))
        file_path = FOLDER + "/" + str(i) + EXTENSION
        filepaths.append(file_path)

# make imguris
# we get them from json, here we can modify them if needed
def make_imguris(tokenuri):
        response = urlopen(tokenuri)
        data_json = json.loads(response.read())
        image_uri = data_json['image']
        #here you can do smthng with image uri, if needed

        #for bayc
        last_chars = image_uri[-46:]
        image_uri = "https://cloudflare-ipfs.com/ipfs/" + last_chars

        return(image_uri)

# run imguris threaded only if needed
# else we just continue from previously parsed txt file   
if (parse_json):
    print ("PARSING JSON...")
    with cf.ProcessPoolExecutor(max_workers=jsonworkers) as executor:
        for n in tqdm(executor.map(make_imguris, tokenuris), total=len(tokenuris)):
            img_uris.append(n)     

    # for big datasets actual image downloading may crash 
    # so may not want to wait for jsons to be parsed again
    # so you better save image uris to the file
    with open(FOLDER+'/image_uris.txt', 'w') as f:
        for item in img_uris:
            f.write("%s\n" % item)
    print ("IMAGE URIS SAVED " + str(len(img_uris)))

# and then read from file

if (not parse_json and START_FROM>0) :
    #in case we continue from stop and we do not make new txt file, 
    # we should start not from beginning of current txt
    with open(FOLDER+'/image_uris.txt') as f:
        img_uris_from_file = f.readlines()
        # calculate offset. offset is how much images was parsed in current txt already
        offset = START_FROM - (COLLECTION_SIZE - len(img_uris_from_file))
        img_uris_from_file = img_uris_from_file[offset:]
else:
    with open(FOLDER+'/image_uris.txt') as f:
        img_uris_from_file = f.readlines()   

print ('IMAGE URIS TO DOWNLOAD ' + str(len(img_uris_from_file)))

# run download threaded
print ("DOWNLOADING IMAGES...")    
with cf.ProcessPoolExecutor(max_workers=imageworkers) as executor:
    list(tqdm(executor.map(urllib.request.urlretrieve, img_uris_from_file, filepaths), total=len(img_uris)))

print("--- %s seconds ---" % (time.time() - start_time))