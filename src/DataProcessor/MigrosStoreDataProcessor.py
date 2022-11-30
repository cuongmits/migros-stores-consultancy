# This file is to create raw data of all Migros Stores in Switzerland
#
#

import osmnx as ox

tags = {"name":"Migros"}
points = [
    tuple((46.523178, 6.667361)), # - Lausanne
    tuple((46.941743, 7.439682)), # - Bern
    tuple((47.355897, 8.493598)), # - Zurich
    tuple((47.021578, 9.192196)), # - Glarus
    tuple((46.702594, 9.744721)), # - Davos
    tuple((46.485156, 8.880970)), # - Blenio District
    tuple((46.320559, 7.680142)), # - Leuk District
    tuple((46.779742, 8.411049))  # - Wolfenschiessen
]
index = 0
for point in points:
    # this is for the cases when sth wrong happens during the process
    # then we will need to rerun this code, but befor rerunning
    # we will need to enter generated file index(es) here to pass already-generated index(es)
    # if index in [0, 1, 2]:
    #     index +=1
    #     continue

    # https://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=geometries_from_address#osmnx.geometries.geometries_from_point
    # http://darribas.org/gds4ae/content/notebooks/06-OpenStreetMap.html
    # https://shapely.readthedocs.io/en/stable/migration.html#multi-part-geometries-will-no-longer-be-sequences-length-iterable-indexable
    gdf = ox.geometries.geometries_from_point(point, tags, dist=100000)
    gdf.to_csv(f'migros_stores_data_{index}.csv')
    print(f'migros_stores_data_{index}.csv file created!')
    index += 1