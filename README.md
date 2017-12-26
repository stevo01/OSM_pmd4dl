# pmd4dl
OSM Project: prepare meta data for download layer

# location for example chart bundles
kap files neu: ftp://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/charts/kap/

# requirements
geojson

https://pypi.python.org/pypi/geojson 

# install procedure of the script
```
pip install geojson
git clone https://github.com/stevo01/OSM_pmd4dl.git
cd OSM_pmd4dl
```
# sample call of the script
```
mkdir .downloads
wget -c -P .downloads ftp://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/charts/kap/*.json
python pmd4dl.py -i ./.downloads/ -o dl.geojseon -u ftp://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/charts/kap/ -f 0.5
```
