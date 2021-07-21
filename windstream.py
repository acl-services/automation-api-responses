
#import all the necessary packages

#system defined module
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import json
import requests
from genericpath import exists, isfile
from pandas import json_normalize
import pandas as pd
import logging
import os


#user-defined module
import tree_structure
import access_credentials
import extract_resources_from_api_tree
import export_to_excel_from_tree
import windstream_logger

logging= windstream_logger.get_logger("windstream_main")


def windstream_main():

    token = input("Enter your access token \n")
    
    # error handling for empty token
    if token == '':
        
        logging.critical('Token not provided, exiting the program')
        exit()
    
    # function call for api access credentials
    else:
        input_url_list = access_credentials.access_credentials()
       

        for index, row in input_url_list.iterrows():
            if 'base_url' in input_url_list.columns: 
                if row.base_url !='nan' :
                    
                    logging.info("the base url is :"+str(row.base_url))
            
                    # function call for extract_resources_from_url
                    high_bond_root = tree_structure.build_tree_for_org(row.org_id)
                    
                    list_of_df = extract_resources_from_api_tree.extract_resources_from_api_tree(high_bond_root, str(row.base_url), token)
                    #export_to_excel(list_of_df)
                    export_to_excel_from_tree.export_to_excel_from_tree(high_bond_root, row.org_id, row.region_code)
            else:
                continue

windstream_main()

