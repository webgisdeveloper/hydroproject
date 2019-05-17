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
    rcp_list = ["45","85","HIST"]
    # period: time period
    period_list = ["2020","2050","2080","HIST"]
    # stype: Summary Type
    # "Mean Annual Values" = "value"
    # "Percent Change in Mean Annual" = "pct"
    # "Absolute Change in Mean Annual" = "abs"
    stype_list = ["value","pct","abs"]

    data = pd.read_csv(csvfile)

    selectdata = data[(data['variable']=="ETmm") & (data['period']=="2050") & (data["rcp"]=="45")]
    print(selectdata.shape)


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