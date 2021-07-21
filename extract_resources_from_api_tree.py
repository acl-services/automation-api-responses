import windstream_logger

logging= windstream_logger.get_logger("api_tree_process")


import os
import pandas as pd
import requests
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter

# Function to extract the resources from anytree
def extract_resources_from_api_tree(hb_root, url_returned, token):
    """
    Function traverse the node structure and pick each of the resources and make the api call and converts the response into dataframe rows only
    if the response code is 200(success)
    :param hb_root: root node from tree
    :param url_returned: base_url to make the api endpoint
    :param token:bearer token to access the org-id
    :return: list of df
    """
    # intializing the dataframe
    list_of_df = []

    #intialize the dataframe
    df_result = pd.DataFrame()

    #Traverse the Tree in preorder traversal
    for node in PreOrderIter(hb_root):

        #If node is parent - call parent endpoint
        if node.parent == None:

            # Logging the org level node's endpoint failure 
            logging.error(node.name+"Org-level resources  cannot be empty")
            continue

        #if the node's parent os highbond
        elif node.parent.name == 'high_bond':
            
            #Logging the org level names and corresponding url
            logging.info("Entering into"+ node.name+ " url"+ url_returned)
           
            #intialize the dataframe
            df_result = pd.DataFrame()
            
            # form the api-endpoint with the current child name
            api_endpoint = url_returned + '/' + node.name
            
            # make the api call with bearer token
            resp = requests.get(api_endpoint, headers={'Authorization': 'Bearer ' + token, 'Accept-Encoding': ""})

            #Logging the API responses for org-level endpoints
            logging.info("API response for org-level endpoints" + api_endpoint)

            # if the status code is successful then normalize the responses
            if resp.status_code == 200:

                logging.info("Reponse code is 200 - successful")

                #store the response in dict
                response_dict = resp.json()

                #Normalize the reponse data as dataframe row
                df_result = pd.json_normalize(response_dict['data'])

                node.api_response = df_result

                # start appending the dataframes
                list_of_df.append(df_result)

            else:
               # Logging the api response code for the nodes which fails
                logging.error(node.name + "API response code" + resp.status_code)

        #if node is child - call endpoint of child - base_url- base_url/parent/parent id/child
        elif node.parent != 'high_bond':

             #form the child base_url endpoint by calling the build child base_url function
             child_resource_endpoint_list = build_child_url(url_returned, node.parent.name, node.url, node.parent.api_response)

              #intialize the df_child_result as a pandas dataframe to append
             df_child_result = pd.DataFrame()

               #traverse the child resource end point list
             for child_resource_endpoint in child_resource_endpoint_list:

                    #store the responses in child_resp variable
                    child_resp = requests.get(child_resource_endpoint, headers={'Authorization': 'Bearer ' + token, 'Accept-Encoding': ""})

                    #check the response status code if it successful
                    if child_resp.status_code == 200:
                        
                        #Logging the api response code
                        logging.info("Reponse code is 200 /successful")
                       
                        #store the reponse as a dict
                        response_dict = child_resp.json()

                        # normalize the dict
                        temp_df = pd.json_normalize(response_dict['data'])

                        #concatinating the child data frames with child result dataframe
                        df_child_result = pd.concat([df_child_result, temp_df])
                        
                        node.api_response = df_child_result

                        #Logging the child base_url to understand the children which makes the successful response code
                        logging.info("Printing the child base_url for the debugging purpose"+ child_resource_endpoint)

                    else:

                        #capture the node names which has end point failure
                        logging.error("The child resource which not able to make the api call is" + child_resource_endpoint)

                        #Loggingthe node names with API response code
                        logging.error(node.name + "API response code" + str(child_resp.status_code))

            #Logging the node name as well as node depth for debugging purpose
             logging.info("The node's depth from its root tree is:" + str(node.name) + "-" + str(node.depth))

            #append the dataframe with child node base_url
             list_of_df.append(df_child_result)

    #return list_of _df
    return list_of_df

# Function to build the child base_url to extract the resources from api response


def build_child_url(base_url, parent_name, child_name, df_parent):

    """
    Function traverse the node structure and pick each of the 
    resources and make the api call and converts the 
    response into dataframe rows only
    if the response code is 200(success)
    :param base_url: base_url
    :param parent_name: parent node name
    :param child_name: child node name
    :param df_parent: dataframe
    :return:  child-base_url
    """
    #intialize a list to store the child_urls
    child_url_list = []

    if(df_parent is not None and isinstance(df_parent, pd.DataFrame) and not df_parent.empty):
        
        logging.info("the org level resources are" + df_parent.to_string())

        #Iterate through every row in org-level resources to call the nested level resources under them
        for index, row in df_parent.iterrows():

           #loop through the df_parent dataframe for every row form the child URL
            child_url_list.append(base_url + "/" + parent_name + "/" + row['id'] + child_name)
        
        logging.info("nested level resources list" + str(child_url_list))

    #returns the child base_url list
    return child_url_list