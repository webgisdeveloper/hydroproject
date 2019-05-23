"""Simulation to GeoServer

This script functions:
    --  caculate the mean value for each subbasin from the simulation output (.csv) 
    --  generate new shapefile for each scenario
    --  

This tool accepts comma separated value files (.csv) 

"""

import os
import sys
import argparse
import pandas as pd
import shapefile

from settings import *


def addvalue2shpfile(value_list,newshpfile="data/test.shp", fieldname="value"):
    """ add value filed to shapefile """

    shpfile = "data/WatershedsHUC12_WGS84.shp"

    # read the existing shapefile
    r = shapefile.Reader(shpfile)

    # create a new shapefile in memory
    w = shapefile.Writer(newshpfile)

    w.fields = r.fields[1:] # skip first deletion field
    w.field(fieldname,"F",decimal=8)
    print(w.fields)

    for i in range(len(r.records())):
        rec = r.record(i)
        rec.append(value_list.iloc[i]['value'])
        w.record(*rec)
        w.shape(r.shape(i))

    w.close()
    # write prj file
    prjfile = newshpfile.replace(".shp",".prj")

    with open(prjfile,"w") as prj:
        prj.write(EPSG_4326)

def csv2shapefile(csvfile):
    """ main module to process csv file and generate shapefile"""

    # headers:    Unnamed: 0  subbasin  value period rcp variable
    # variable
    # "Precipitation" = "PRECIPmm", "Evapotranspiration" = "ETmm",
    # "Soil water content" = "SWmm","Groundwater Recharge" = "PERCmm", 
    # "Baseflow" = "GW_Qmm","Streamflow" = "FLOW_OUTcms",
    # "Water Yield" = "WYLDmm")),
    variable_list = ["PRECIPmm","ETmm","SWmm","PERCmm", "GW_Qmm","FLOW_OUTcms","WYLDmm"]
    # rcp: Emissions Scenario
    # Medium" = "45", "High" = "85","Historical" = "historical"
    rcp_list = ["45","85","hist"]
    # period: time period
    period_list = ["2020","2050","2080","hist"]
    # stype: Summary Type
    # "Mean Annual Values" = "value"
    # "Percent Change in Mean Annual" = "pct"
    # "Absolute Change in Mean Annual" = "abs"
    stype_list = ["value","pct","abs"]

    data = pd.read_csv(csvfile)
    # drop the first column
    data.drop(data.columns[[0]],axis=1,inplace=True)

    selectdata = data[(data['variable']=="ETmm") & (data['period']=="hist") & (data["rcp"]=="hist")][["subbasin","value"]]
    # for duplicates data, get the mean values
    if selectdata.shape[0] > TOTAL_NUMBER_OF_SUBBASIN:
        #print(selectdata.shape)
        #print(selectdata.head())
        #selectdata = selectdata.drop_duplicates(subset=["subbasin"])
        valuedata = selectdata.groupby('subbasin').mean()
    else:
        valuedata = selectdata[["subbasin","value"]]
        valuedata.set_index(['subbasin'],inplace=True, drop=True)

    #print(valuedata.shape)
    #print(valuedata.head())
    #print(valuedata.loc[[1,2]])
    #addvalue2shpfile(valuedata)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="simulation output csv file"
    )
    args = parser.parse_args()
    csv2shapefile(args.input_file)


if __name__ == "__main__":
    main()