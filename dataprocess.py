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

from settings import *

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

    selectdata = data[(data['variable']=="GW_Qmm") & (data['period']=="2020") & (data["rcp"]=="45")]
    # drop duplicates data
    if selectdata.shape[0] > TOTAL_NUMBER_OF_SUBBASIN:
        print(selectdata.shape)
        selectdata = selectdata.drop_duplicates(subset=["subbasin"])
        print(selectdata.shape)
        print(selectdata.head())
        print(selectdata.tail())


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