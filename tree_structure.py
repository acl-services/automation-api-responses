# importing all the libraries and packages
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, LevelOrderIter

#DEclare the HB as root resource
high_bond_root = Node("high_bond",url="high_bond")

#DEclare the collections as the child of HBR
collections = Node("collections", parent=high_bond_root,url="/collections")
questionnaires = Node("questionnaires", parent=collections,url="/questionnaires")
analyses = Node("analyses", parent=collections,url="/analyses")
table = Node("table", parent=analyses,url="/tables")

# Asset type is the main resource
asset_types = Node("asset_types",parent=high_bond_root,url="/asset_types")
assets = Node("assets", parent=asset_types,url="/assets")


# events is the main resource at HB
events = Node("events",parent=high_bond_root,url="/events")

# attribute_types is the main resource at HB
attribute_types = Node("attribute_types",parent=high_bond_root,url="/attribute_types")

# Roles is the main resource at HB
roles = Node("roles",parent=high_bond_root,url="/roles")

# handlers is the main resource at HB
handlers = Node("handlers",parent=high_bond_root,url="/handlers")



# Asset Record typse is the main resource at HB
asset_record_types= Node("record_types",parent=high_bond_root,url="/record_types")

# records are the child of record -type
#records = Node("records", parent=asset_record_types,url="statuses")
#asset_record_types = Node("asset_record_types",url="/statuses")


#Project type is the main resource at HB
project_type= Node("project_types",parent=high_bond_root,url="/project_types")

#custom_attributes is the child resource of project
custom_attributes= Node("custom_attributes", parent=project_type, url='/custom_attributes')

#workflows is the child resource of HB
workflows= Node("workflows",parent=high_bond_root,url="/workflows")

#workflow_status is the child resource of workflow
workflow_status= Node("workflow_status", parent=workflows,url="?include=statuses")

#workflow_status_events is the child resource of workflow
workflow_status_events= Node("workflow_status_events", parent=workflows,url="?include=statuses.events")


# printing the tree structre at the console
[print(node.name,node.parent,node.url) for node in PreOrderIter(high_bond_root)]

#print(RenderTree(high_bond_root))







