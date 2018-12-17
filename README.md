# pmd4dl
OSM Project: prepare meta data for download layer

# specification for osm geo json file structure
https://wiki.openseamap.org/wiki/OpenSeaMap-dev:De:Chart_Download_Layer

# online check for geojson files
http://geojsonlint.com/

# location for chart bundles
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
# sample call of the merge script
```
mkdir .downloads
python FetchJsonFiles.py -a ftp5.gwdg.de -i /pub/misc/openstreetmap/openseamap/charts/history/kap -d sample/geojson/kap/
python merge_geojson_files.py -d .sample/geojson/kap/ -o download.geojson
```
