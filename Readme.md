## NFT Collection image scraper

![Teaser image](https://www.larvalabs.com/public/images/product/cryptopunks/punk-variety-2x.png)

**AKA Superchaged Right Click Save**<br>
by <a href="https://twitter.com/filmakarov">fmc</a> <br>

## Basic Usage
It is a python script. Tested on Mac OS and Ubuntu with Python 3.
run it with
```.bash
python scraper_mt2.py
```
or
```.bash
python3 scraper_mt2.py
```

**Setup config**
1. baseuri. BaseUri is returned by collection contract baseURI() function. Find the contract on Etherscan, Read Contract and choose baseURI() for ERC721 or uri for ERC1155.
2. collection size. 
3. Start from. If you are scraping for the first time, set to 0. 
Set another value if you are continuing after it stopped downloading images only.
If you've got an error during parsing JSON, start again from 0. 
4. parse json again or not. set to false only when you've got error during downloading images, so that you've got complete txt file with json uris and you do not want to parse all of them again
5. file extension for resulting files
6. folder to store scraped files
7. multithread workers #. json workers usually ok 2 or 4. imageworkers was 1 on local machine and 2 or 4 on gce instance

**Image URI Tweaking**
Image uris for all the collections differ. 
For most https:// imageuris everything works fine with just 
```.bash
image_uri = data_json['image']
```
However, sometimes we need some tweaking. 
For BAYC it was ipfs:// link, which cannot being open by urlretrieve directly.
So we have to take hash out of the link and request it from public ipfs node with.
```.bash
last_chars = image_uri[-46:]
image_uri = "https://cloudflare-ipfs.com/ipfs/" + last_chars
```
**Good luck, folks**