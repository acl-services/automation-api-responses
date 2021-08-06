# import all the necessary packages

# system defined module
import warnings
from pathlib import Path

from anytree import AsciiStyle, LevelOrderIter, Node, PreOrderIter, RenderTree

warnings.filterwarnings("ignore")
import json
import logging
import os

import pandas as pd
import requests
from genericpath import exists, isfile
from pandas import json_normalize

import access_credentials
import export_to_excel_from_tree
import extract_resources_from_api_tree
import tree_structure
import windstream_logger

logging = windstream_logger.get_logger("windstream_main")

# Main of the script-Entry point
def windstream_main():
    # Get the token from the user
    token = input("Enter your access token \n")

    # error handling for empty token
    if token == "":

        # log the error
        logging.critical("Token not provided, exiting the program ")

        # log and exit the program smoothly
        exit()


    # function call for api access credentials
    else:

        # store the api end point urls as a list
        input_url_list = access_credentials.access_credentials()

        # iterate through every row in the list of api end point url
        for index, row in input_url_list.iterrows():

            # if there is a base url
            if "base_url" in input_url_list.columns:

                # is base url is not "NAN"
                if row.base_url != "nan":

                    # log the base url for the purpose of debugging
                    logging.info(f"the base url is :  + {str(row.base_url)}")

                    # function call for extract_resources_from_url
                    high_bond_root = tree_structure.build_tree_for_org(row.org_id)

                    # function call to extract the resources from api tree
                    extract_resources_from_api_tree.extract_resources_from_api_tree(
                        high_bond_root, str(row.base_url), token
                    )

                    # export_to_excel(list_of_df)
                    export_to_excel_from_tree.export_to_excel_from_tree(
                        high_bond_root, row.org_id, row.region_code
                    )
            else:
                continue


# Call main()
windstream_main()
