# pmd4dl
OSM Project: prepare meta data for download layer

# specification for osm geo json file structure
https://wiki.openseamap.org/wiki/OpenSeaMap-dev:De:Chart_Download_Layer

# online check for geojson files
http://geojsonlint.com/

# location for chart bundles
kap files:     https://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/charts/history/kap/
mbtiles files: https://ftp5.gwdg.de/pub/misc/openstreetmap/openseamap/charts/history/mbtiles/

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
rm -fr work
mkdir -p work
python3 FetchJsonFiles.py -a ftp.gwdg.de -i /pub/misc/openstreetmap/openseamap/charts/history/kap      -o ./work/
python3 FetchJsonFiles.py -a ftp.gwdg.de -i /pub/misc/openstreetmap/openseamap/charts/history/mbtiles/ -o ./work/
rm download.geojson
python3 merge_geojson_files.py -d ./work/ -o download.geojson
```