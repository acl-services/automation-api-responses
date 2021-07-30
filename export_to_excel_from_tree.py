import windstream_logger
logging= windstream_logger.get_logger("write_into_excel")

import os
import pandas as pd
import requests
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter


# Function to export the dataframe results into an excel sheet
def export_to_excel_from_tree(high_bond_tree, org_id, region_code):

    """
    Function traverse the node structure and pick each of the resources and make the api call and converts the response into dataframe rows only
    if the response code is 200(success)
    :param high_bond_tree: root node
    :return: excel sheet
    """

    # create the output file path
    root_path = 'Resources_Extraction'

    # create the sub folder to write the excel
    excel_path = root_path + '/org_id_' + str(int(org_id)) + '_' + region_code

    #Logging the output file path
    logging.info("The output is written into this "+ excel_path + " path")

    os.makedirs(root_path, exist_ok=True)
    os.makedirs(excel_path, exist_ok=True)

    #create the excel sheet
    excel_filename = 'Resources_from_api_' + str(int(org_id)) + '_' + region_code + '.xlsx'

    logging.info("The output excel file is written into this " + excel_filename + " folder")

    #Use excel path
    excel_file = os.path.join(excel_path, excel_filename)

    #use excelwriter to write into excel
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

   

    for node in PreOrderIter(high_bond_tree):

        #check the depth of the node if it is greater than 0 to confirm  it has nested structure
        if(node.depth > 0):

          # if(node.api_response.empty==False):
          if(node.api_response is not  None and isinstance(node.api_response, pd.DataFrame)):
            node.api_response.to_excel(writer, sheet_name=node.name, index=False)
            logging.info(node.api_response)

            
            

    writer.save()
    
    logging.info("Saving the resources aPI reponses into a destination location " + str(int(org_id)) )
    print("Saved the resources from org id ", str(int(org_id)))