
# import all the necessary packages

from pandas import json_normalize
from anytree import Node, RenderTree
import pandas as pd
import requests
import os
import json
import tree_structure
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter

org_id=0

url=''


# Function to form  the Org level-base URL
def parent_resource_access_credentials():
    
    """
    Function to get the user access credentials as input to make the api endpoints
    :return: base url along with token for other functions
    """
    #Hardcoded basepath
    basepath='https://apis-us.highbond.com/v1/'
    
    # Get the org-id as user input 
    org_id=input("Enter the org-id")
    
    # Get the access token as user input
    token=input("Enter your access token")

    # forming the base url for api call
    url=basepath+'orgs/'+str(org_id)
    
    #cross check the base url for the purpose of validation
    print("The base url is ",url)
    return url,token

# Function to extract the resources from anytree
def extract_resources_from_api_tree(hb_root,url_returned,token):
    """
    Function traverse the node structure and pick each of the resources and make the api call and converts the response into dataframe rows only
    if the response code is 200(success)
    :param hb_root: root node from tree
    :param url_returned: url to make the api endpoint
    :param token:bearer token to access the org-id
    :return: list of df
    """
    list_of_df=[]
    
    #intialize the dataframe
    df_result = pd.DataFrame()
    
    #Traverse the Tree in preorder traversal
    for node in PreOrderIter(hb_root):
    
    #If node is parent - call parent endpoint
        if node.parent==None: 
            continue
        
        #if the node's parent os highbond 
        elif node.parent.name=='high_bond':
            
            #intialize the dataframe
            df_result = pd.DataFrame()
            
            # form the api-endpoint with the current child name
            api_endpoint= url_returned+'/'+ node.name
            
            # make the api call with bearer token
            resp = requests.get(api_endpoint, headers = {'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
            print("API response for org-level endpoints",api_endpoint)
            

            # if the status code is successful then normalize the responses
            if resp.status_code == 200:
                
                #store the response in dict
                response_dict = resp.json()
                
                #Normalize the reponse data as dataframe row
                df_result = pd.json_normalize(response_dict['data'])


                node.api_response = df_result
                
                # start appending the dataframes 
                list_of_df.append(df_result)
                
            else:
               # print("Failed API endpoint")
                print(node.name,"API response code",resp.status_code)

    #if node is child - call endpoint of child - url- base_url/parent/parent id/child
        elif node.parent!='high_bond':
                
                #form the child url endpoint by calling the build child url function
                child_resource_endpoint_list=build_child_url(base_url,node.parent.name,node.url,node.parent.api_response)
                
                #intialize the df_child_result as a pandas dataframe to append
                df_child_result = pd.DataFrame()
                
                #traverse the child resource end point list
                for child_resource_endpoint in child_resource_endpoint_list:

                    #store the responses in child_resp variable
                    child_resp=requests.get(child_resource_endpoint,headers = {'Authorization':'Bearer ' + token, 'Accept-Encoding' : "" })
                    
                    #check the response status code if it successful
                    if child_resp.status_code == 200:

                        #store the reponse as a dict
                        response_dict = child_resp.json()

                        # normalize the dict
                        temp_df = pd.json_normalize(response_dict['data'])
                        
                        #concatinating the child data frames with child result dataframe
                        df_child_result = pd.concat([df_child_result, temp_df])
                        node.api_response = df_child_result

                        #printing the child url to understand the children which makes the successful response code
                        print("Printing the child url for the debugging purpose",child_resource_endpoint)

                    else:

                        #capture the node names which has end point failure
                        print("The child resource which not able to make the api call is",child_resource_endpoint)
                        
                        #print the node names with API response code
                        print(node.name,"API response code",child_resp.status_code)

                
                #print the node name as well as node depth for debugging purpose
                print(node.name,node.depth)
                #append the dataframe with child node url
                list_of_df.append(df_child_result)
    
    #return list_of _df            
    return list_of_df

# Function to build the child url to extract the resources from api response
def build_child_url(base_url,parent_name,child_name,df_parent):
    """
    Function traverse the node structure and pick each of the 
    resources and make the api call and converts the 
    response into dataframe rows only
    if the response code is 200(success)
    :param base_url: url
    :param parent_name: parent node name
    :param child_name: child node name
    :param df_parent: dataframe
    :return:  child-url
    """
    #intialize a list to store the child_urls
    child_url_list=[]

    #Iterate through every row in org-level resources to call the nested level resources under them
    for index, row in df_parent.iterrows():
       
       #loop through the df_parent dataframe for every row form the child URL
       child_url_list.append(base_url + "/"+ parent_name + "/" + row['id']+ child_name)
    
    #returns the child url list   
    return child_url_list 
    
# function call for api access credentials
base_url,token =parent_resource_access_credentials()

# function call for extract_resources_from_url
list_of_df =extract_resources_from_api_tree(tree_structure.high_bond_root,base_url,token)


# Function to export the dataframe results into an excel sheet 
def export_to_excel_from_tree(high_bond_tree):
    """
    Function traverse the node structure and pick each of the resources and make the api call and converts the response into dataframe rows only
    if the response code is 200(success)
    :param high_bond_tree: root node
    :return: excel sheet
    """

    # create the output file path
    root_path = 'API_extraction'

    # create the sub folder to write the excel
    excel_path = root_path+'/excel_resources'

    os.makedirs(root_path, exist_ok=True)
    os.makedirs(excel_path, exist_ok=True)

    #create the excel sheet
    excel_filename = 'Extracted_resources_from_api_31966.xlsx'
    
    #Use excel path
    excel_file = os.path.join(excel_path, excel_filename)
    
    #use excelwriter to write into excel
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    
    #maintain a counter
    df_list_counter=0
 
    for node in PreOrderIter(high_bond_tree):

        #check the depth of the node if it is greater than 0 to confirm  it has nested structure
        if(node.depth > 0):

          if(node.api_response.shape[0]>0):
            node.api_response.to_excel(writer, sheet_name = node.name, index=False)
            df_list_counter+=1
  
    writer.save()

#export_to_excel(list_of_df) 
export_to_excel_from_tree(tree_structure.high_bond_root)







