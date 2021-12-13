import vcr
import nytimesGet
from urllib.request import urlopen

f= open("keys/nytKey.txt", "r+")
key=f.read()
f.close()

import vcr
from urllib.request import urlopen

with vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml'):
    response = urlopen("https://www.tagesschau.de/multimedia/video/videoarchiv2.html").read()
    assert b"viewB" in response