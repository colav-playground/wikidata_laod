
<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# Wikidata cut
A set of scripts and documentation to download wikidata, uncompress it, load it to mongodb.


# Installation
Please go to https://dumps.wikimedia.org/wikidatawiki/entities/ and download the latest json version.

`pip install joblib pymongo`


Install mongodb
https://www.mongodb.com/docs/v7.0/administration/install-community/


## uncompressing

uncompress de the wikidata-20240101-all.json.gz
gzip -k -d wikidata-20240101-all.json.gz 

It requires 1.4T of space and 287.78 GiB in mongodb


## loading to mongodb

mongoimport --db wikidata --collection data --file wikidata-20240101-all.json --jsonArray

it requires about 287.78 GiB of storage in mongodb.

## Generating wikidata_types.json

It's not needed to run this all the time, you can use the already generated in this repository,
but if you want to run it you will need the kahi databases output, then please edit generate_instances_of.py

run it with `python generate_instances_of.py`

## Using wikidata_cut.py
please edit global variables in wikidata_cut.py first then

`python wikidata_cut.py`

this takes a lot of time, please be patient


# License
BSD-3-Clause License 

# Links
http://colav.udea.edu.co/



