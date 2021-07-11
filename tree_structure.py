# importing all the libraries and packages
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter
from pandas import pandas as pd

#Declare the HB as root resource
high_bond_root = Node("high_bond",url="high_bond",api_response=pd.DataFrame)

#Declare the collections as the child of HBR
collections = Node("collections", parent=high_bond_root,url="/collections",api_response=pd.DataFrame)
questionnaires = Node("questionnaires", parent=collections,url="/questionnaires",api_response=pd.DataFrame)
analyses = Node("analyses", parent=collections,url="/analyses",api_response=pd.DataFrame)
table = Node("table", parent=analyses,url="/tables",api_response=pd.DataFrame)

# Asset type is the main resource
asset_types = Node("asset_types",parent=high_bond_root,url="/asset_types",api_response=pd.DataFrame)
assets = Node("assets", parent=asset_types,url="/assets",api_response=pd.DataFrame)


# events is the main resource at HB
events = Node("events",parent=high_bond_root,url="/events",api_response=pd.DataFrame)

# attribute_types is the main resource at HB
attribute_types = Node("attribute_types",parent=high_bond_root,url="/attribute_types",api_response=pd.DataFrame)

# Roles is the main resource at HB
roles = Node("roles",parent=high_bond_root,url="/roles",api_response=pd.DataFrame)

# handlers is the main resource at HB
handlers = Node("handlers",parent=high_bond_root,url="/handlers",api_response=pd.DataFrame)



# Asset Record typse is the main resource at HB
asset_record_types= Node("record_types",parent=high_bond_root,url="/record_types",api_response=pd.DataFrame)

# records are the child of record -type
#records = Node("records", parent=asset_record_types,url="statuses")
#asset_record_types = Node("asset_record_types",url="/statuses")


#Project type is the main resource at HB
project_type= Node("project_types",parent=high_bond_root,url="/project_types",api_response=pd.DataFrame)

#custom_attributes is the child resource of project
custom_attributes= Node("custom_attributes", parent=project_type, url='/custom_attributes',api_response=pd.DataFrame)

#workflows is the child resource of HB
workflows= Node("workflows",parent=high_bond_root,url="/workflows",api_response=pd.DataFrame)

#workflow_status is the child resource of workflow
workflow_status= Node("workflow_status", parent=workflows,url="?include=statuses",api_response=pd.DataFrame)

#workflow_status_events is the child resource of workflow
workflow_status_events= Node("workflow_status_events", parent=workflows,url="?include=statuses.events",api_response=pd.DataFrame)


# printing the tree structre at the console
[print(node.name,node.parent,node.url) for node in PreOrderIter(high_bond_root)]

print(RenderTree(high_bond_root))







