import argparse
import os
import uuid

from grass_session import Session
from grass.script import core as gcore
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import vector as v


from config import DATA, LOCATION, MAPSET
from utils import uniq_name

def main(index, AOI, grass_params):
    PERMANENT = Session()
    PERMANENT.open(gisdb=grass_params[0], location=grass_params[1], mapset=grass_params[2])

    aoi = uniq_name('aoi')
    tiles = uniq_name('tiles')
    intersection = uniq_name('common')

    try:
        v.in_ogr(input=index, output=tiles)
        v.in_ogr(input=AOI, output=aoi)
        v.select(binput=aoi, ainput=tiles, output=intersection, operator='overlap')
        v.db_select(map=intersection, columns='location', flags='c')
    finally:
        g.remove(type='vector', name=tiles, flags='f')
        g.remove(type='vector', name=aoi, flags='f')
        g.remove(type='vector', name=intersection, flags='f')



if __name__ == "__main__":
    from config import DATA, LOCATION, MAPSET

    parser = argparse.ArgumentParser(description='Detect clouds.')
    parser.add_argument('index', help='Index file (tiles bbox)')
    parser.add_argument('AOI', help='AOI file (GeoJSON)')

    args = parser.parse_args()
    index = args.index
    aoi = args.AOI
    main(index, aoi, (DATA, LOCATION, MAPSET))
 
