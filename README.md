# destiny-ebook-lore-hacksession
Quick "hack session" style Destiny Lore Ebook generator (EPUB format).

## Requirements
This software requires the following to be run

1. Python 2.7 (https://www.python.org/download/releases/2.7/)
2. pip (https://pip.pypa.io/en/stable/installing)
3. jq (https://stedolan.github.io/jq/)
4. curl (https://curl.haxx.se/)
5. A created Bungie app credential (https://www.bungie.net/en/Application/Create)

## Running

1. Install all requirements
2. Make a note of the created API Key
3. Install all Python dependencies by running
```bash
pip install -r requirements.txt
```
4. Run the _retrieveAndGenerateGrimoire.sh_ script, providing it the Bungie API key as a parameter
```
./retrieveAndGenerateGrimoire.sh <API_KEY>
```

After execution, you should find a _destinyGrimoire.epub_ file on the same folder.

## Details on what is happening

When running the script above, the following happens:

1. The Destiny Grimoire is downloaded (using curl) from Bungie using the provided API Key.
2. Using jq, the json Grimoire is "distilled" to the attributes that are of relevance for creating the epub. The result is stored under _destinyGrimoire.json_.
3. A folder _images_ is created (it is deleted first if it exists)
4. All images described in the grimoire are downloaded to said _images_ folder.
5. The epub is generated using all the previously retrieved resources and Python.