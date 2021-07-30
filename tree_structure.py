# importing all the libraries and packages

from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter
from pandas import pandas as pd

def build_tree_for_org(org_id):
    
    #Declare the HB as root resource

    high_bond_root = Node("high_bond",url="high_bond",api_response=pd.DataFrame,org_id=org_id, node_type='normal')
    
    #Declare the collections as the child of HBR
    collections = Node("collections", parent=high_bond_root,url="/collections",api_response=pd.DataFrame,node_type='normal')
    questionnaires = Node("questionnaires", parent=collections,url="/questionnaires",api_response=pd.DataFrame,node_type='normal')
    analyses = Node("analyses", parent=collections,url="/analyses",api_response=pd.DataFrame,node_type='normal')
    table = Node("table", parent=analyses,url="/tables",api_response=pd.DataFrame,node_type='normal')

    # Robots are the main resource under HB
    robots=Node("robots", parent=high_bond_root,url="/robots",api_response=pd.DataFrame,node_type='normal')
    robot_tasks=Node("robot_tasks", parent=robots,url="/robot_tasks",api_response=pd.DataFrame,node_type='normal')
    
    #why the api says list a robot's analytic scripts
    robot_versions=Node("robot_versions", parent=robots,url="/robot_apps",api_response=pd.DataFrame,node_type='normal')
    

    #system_users
    System_users=Node("system_users", parent=high_bond_root,url="/system_users",api_response=pd.DataFrame,node_type='normal')

    # Asset type is the main resource
    asset_types = Node("asset_types",parent=high_bond_root,url="/asset_types",api_response=pd.DataFrame,node_type='normal')
    assets = Node("asset_types_assets", parent=asset_types,url="/assets",api_response=pd.DataFrame,node_type='normal')
    # #asset_type_attribute type 
    # #{{ _.base_url }}{{ _.org_id }}/asset_types/1027157/attribute_types
    asset_type_attribute_types=Node("asset_type_attribute_types",parent=asset_types, url="/attribute_types", api_response=pd.DataFrame,node_type='normal')


    # events is the main resource at HB
    events = Node("events",parent=high_bond_root,url="/events",api_response=pd.DataFrame,node_type='normal')

    #attribute_types is the main resource at HB
    
    attribute_types = Node("attribute_types",parent=high_bond_root,url="/attribute_types",api_response=pd.DataFrame,node_type='normal',)
    attribute_types_option=Node("attribute_types_option",parent=attribute_types,url="", api_response=pd.DataFrame,node_type='nested',api_json_list=[],col_name_list=['type_options'])
 
    #Roles is the main resource at HB
    roles = Node("roles",parent=high_bond_root,url="/roles",api_response=pd.DataFrame,node_type='normal')
 
    #handlers is the main resource at HB
    handlers = Node("handlers", parent=high_bond_root, url="/handlers", api_response=pd.DataFrame,node_type='normal')
    handler_nested_structure = Node ("handler_nested_structure", parent=handlers,url="", api_response=pd.DataFrame, node_type='nested',api_json_list= [], col_name_list=['conditions','actions','triggers'])
    

    #There is no Asset Record type in API Doc, record types is the org-level resource at HB(Asset record type is record types in API endpoint)
    record_types= Node("record_Types",parent=high_bond_root,url="/record_types",api_response=pd.DataFrame,node_type='normal')
    # records are the child of record -type
    records = Node("record_types_records", parent=record_types,url="/records",api_response=pd.DataFrame,node_type='normal')
    

    # Project type is the main resource at HB
    project_type= Node("project_types",parent=high_bond_root,url="/project_types",api_response=pd.DataFrame,node_type='normal')
    #project_type_nested = Node("project_types_nested_structure", parent = project_type , url="", api_response=pd.DataFrame,node_type='nested',api_json_list=[],col_name_list=['project_terms','objective_terms','narrative_terms','walkthrough_terms','control_test_terms','finding_terms','control_terms','risk_terms','planning_terms','results_terms','certification_terms','test_plan_terms'])
   
    # custom_attributes is the child resource of project
    custom_attributes= Node("custom_attributes", parent=project_type, url='/custom_attributes',api_response=pd.DataFrame,node_type='normal')

    # #workflows is the child resource of HB
    workflows= Node("workflows",parent=high_bond_root,url="/workflows",api_response=pd.DataFrame,node_type='normal')

    # #workflow_status is the child resource of workflow
    workflow_status= Node("workflow_status", parent=workflows,url="?include=statuses",api_response=pd.DataFrame,node_type='normal')

    # #workflow_status_events is the child resource of workflow
    workflow_status_events= Node("workflow_status_events", parent=workflows,url="?include=statuses.events",api_response=pd.DataFrame,node_type='normal')

    return high_bond_root
    
    
    #printing the tree structre at the console
    #[print(node.name,node.parent,node.url) for node in PreOrderIter(high_bond_root)]

    #print(RenderTree(high_bond_root))







