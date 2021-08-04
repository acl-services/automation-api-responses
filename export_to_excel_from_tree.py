<<<<<<< HEAD
from pandas.core.frame import DataFrame
=======
>>>>>>> e2a36b2ceac6c7d03b71985e40a635bf0e9c87d5
import windstream_logger
logging= windstream_logger.get_logger("write_into_excel")

import os
<<<<<<< HEAD
import itertools
import pandas as pd
import json
import requests
from collections import defaultdict
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter


# Function to parse the attribute_types json response from an api end point call
def json_parse_attribute_types(json_data):

  #Intialize the empty dataframe
  df_result = pd.DataFrame()
  #log the json data as it is 
  logging.info("json_data is :"+ json.dumps(json_data, indent = 4))
  
  # check for the "type options"
  if "type_options" in json_data['data']['attributes']:
          
            
            if "select_values" in json_data['data']['attributes']["type_options"]:
              
              for select_value in json_data['data']['attributes']["type_options"]["select_values"]:
           
                logging.info("select_value is :"+ str(select_value))

                temp_df = pd.json_normalize(select_value)
                
                temp_df.insert(0,"attribute_id",json_data['data']["id"])

                temp_df.insert(1, "type",json_data['data']["type"])

                df_result=pd.concat([df_result,temp_df])
           


  #logging.info(df_result)
  return df_result


# Function to parse the attribute_types json response from an api end point call
def json_parse_attribute_types1(json_data):

  #Intialize the empty dataframe
  df_result = pd.DataFrame()
  #log the json data as it is 
  logging.info("json_data is :"+ json.dumps(json_data, indent = 4))
  
  # check for the "type options"
  if "type_options" in json_data['data']['attributes']:
          
            
            if "select_values" in json_data['data']['attributes']["type_options"]:
              
              for select_value in json_data['data']['attributes']["type_options"]["select_values"]:
           
                logging.info("select_value is :"+ str(select_value))

                temp_df = pd.json_normalize(select_value)
                
                temp_df.insert(0,"attribute_id",json_data['data']["id"])

                temp_df.insert(1, "type",json_data['data']["type"])

                df_result=pd.concat([df_result,temp_df])
           


  #logging.info(df_result)
  return df_result

# Function to parse the node if the node has the nested structures- but not as a child json response from an api end point call
def  custom_dataframe_nested(api_json_list,col_name):

    handler=pd.DataFrame()
    #intialize the dataframe
    nested_structures=pd.DataFrame()
    
    for api_json in api_json_list:
            
            #run a for loop for every items
            for i,values in api_json.items():
                #check for the type options column
                if col_name=='type_options' or col_name == " ":
                    temp_df= json_parse_attribute_types(api_json)
                    nested_structures=pd.concat([nested_structures,temp_df])
                elif col_name in api_json:
                    temp_df=pd.json_normalize(values['attributes'][col_name])
                    temp_df.insert(0,"id",api_json['data']["id"])
                    temp_df.insert(1, "type",api_json['data']["type"])
                    nested_structures=pd.concat([nested_structures,temp_df])
                   
                    
    #return the nested structures json response as a data frame
    return nested_structures


def  custom_dataframe_nested1(api_json_list,col_name):

    handler=pd.DataFrame()
    #intialize the dataframe
    nested_structures=pd.DataFrame()
    
    for api_json in api_json_list:
            
            #run a for loop for every items
            for i,values in api_json.items():
                #check for the type options column
                if col_name=='type_options' or col_name == " ":
                    temp_df= json_parse_attribute_types1(api_json)
                    nested_structures=pd.concat([nested_structures,temp_df])
                else:
                    
                    temp_df=pd.json_normalize(values['attributes'][col_name])
                    temp_df.insert(0,"id",api_json['data']["id"])
                    temp_df.insert(1, "type",api_json['data']["type"])
                    nested_structures=pd.concat([nested_structures,temp_df])
                   
                    
    #return the nested structures json response as a data frame
    return nested_structures


=======
import pandas as pd
import requests
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter


>>>>>>> e2a36b2ceac6c7d03b71985e40a635bf0e9c87d5
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

<<<<<<< HEAD
=======
   

>>>>>>> e2a36b2ceac6c7d03b71985e40a635bf0e9c87d5
    for node in PreOrderIter(high_bond_tree):

        #check the depth of the node if it is greater than 0 to confirm  it has nested structure
        if(node.depth > 0):

<<<<<<< HEAD
          #if node is nested
            if node.node_type=='nested':

                #run a for loop for ever column in col_name_list
                for col_name in node.col_name_list:

                  #logging the col name
                  logging.info("col_name " + col_name)
                        
                  #logging the col list
                  logging.info("json list: " + str(len(node.api_json_list)))
                        
                  #call custom_dataframe_nested function
                  df=custom_dataframe_nested1(node.api_json_list,str(col_name)) 
                        
                  #write into an excel sheet with the name of the column
                  df.to_excel(writer, sheet_name= col_name , index=False)
            
            # # check if the node type is not nested and normal          
            # if node.node_type=='normal':
            #     if(node.api_response is not None and isinstance(node.api_response, pd.DataFrame) or node.api_response is None ):
            #         node.api_response.to_excel(writer, sheet_name=node.name, index=False)
            #         logging.info(node.api_response)

            if node.node_type=='normal':
              if(node.api_response is not None and isinstance(node.api_response, pd.DataFrame) or node.api_response is None ):
                     node.api_response.to_excel(writer, sheet_name=node.name, index=False)
                     logging.info(node.api_response)

            
            
    #save
    writer.save()
    
    #log this message to know the status of the script
    logging.info("Saving the resources aPI reponses into a destination location " + str(int(org_id)) )
    
    #Leave this print message to the use to ge to know that script has completed one org
    print("Saved the resources from org id ", str(int(org_id)))
=======
          # if(node.api_response.empty==False):
          if(node.api_response is not  None and isinstance(node.api_response, pd.DataFrame)):
            node.api_response.to_excel(writer, sheet_name=node.name, index=False)
            logging.info(node.api_response)

            
            

    writer.save()
    
    logging.info("Saving the resources aPI reponses into a destination location " + str(int(org_id)) )
    print("Saved the resources from org id ", str(int(org_id)))
>>>>>>> e2a36b2ceac6c7d03b71985e40a635bf0e9c87d5
