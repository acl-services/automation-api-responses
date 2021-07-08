
## Author: R.Nandhini
## Product Owner: John Fitch, Jared
## Reviewers: John Fitch, Diana Hidalgo
## Table of Contents
Title of the project
Background
Tech stack
Set up
Summary

## Title of the project

Windstream special project

### Background

This project has the following requirements:

Build a python script to read the resources list and create the excel tabs based on the API responses for each of the resources in the list. The excel file would be a tool to understnad the relationship between the resources.

### The list of resources were given as part of the intial level discussion with John and Jared:
'collections'

'events'

'workflows'

'handlers'

'roles'

'role_permission_assignments'

'analysis'

'attribute_types'

'workflow_status'

'asset_types'

'project_types'

'custom_attributes'

'workflow_status_events'

'questionnaires'

'tables'

'asset_record_types'

### Input:
API access credentials such as access token, Org_id, base url

API responses from org level resources and also from its nested resources

### Output:
Excel sheet which contain all the resources as tab names and its responses as fields names

The python script has been developed completely based on Highbond API documentation.The relationship between the resources have been cross checked with API documentation and created the treestructure based on the API documentation.

https://docs-apis.highbond-s1.com/public.html

### Software design behind this approach:

In order to understand the API responses, we need to understand the hierarchical structure of the resources from the org level up until leaf node level. I found "any tree" package(refer the link below) from python which would be appropriate for this particular use-case to traverse back and forth to gain the dependencies between the resources. I have created the tree structure of the resources as a first step to understand the flow between the resources and cross verified with API documentation about the nested structure of the resources. As a second step, I have imported this tree into the main python program to traverse from root(High bond) to nested resources. I have used this traversal to form the parent URL for making API endpoint as well as child URL. I loop through all the parent resources until it reaches the last node(leaf node) in its tree structure. Once it hit the leaf node, it traverses back to the parent node and continues the same for the rest of the resources.

### Basic Architecture +  Minutes of the meeting(MoM) with John:

https://whimsical.com/windstream-HoQh2tES1xAnFa8iUqzoS2

### Anytree DOcumentation

https://anytree.readthedocs.io/en/latest/index.html


### Pros:

1. Dependencies between the resources can be completely configurable by the tree structure based on the tool kit use cases

2. Works well for the first level requirements given to me

3. This is basic version. Further edge cases can be improved as and when the requirements are changing 

4. Completely modular

5. Efficient to traverse back and forth in tree

### Cons:

1. Testing has not been completed-In progress

Note: Edge cases has to be given as "special outliers  cases" as part of the requirements. 

### Time taken:

 4 working days

### Tech-stack

1. Python
2. windows
3. Refer requirements.txt for details


## Setup

Run the requirenets.txt to set up the dependencies in your local machine

### Summary: 

This version of code works well with intial requirements given to me on June 29,2021. It took 2 working days to fix the api endpoints bugs from API team. After the intial first level meeting with John on July 6th, few bugs were noted down. The next version fixes all bugs and cross checked with APi responses and captured those responses as rows and columns in excel sheet.


Resources not been covered in API documentation:

'role_permission_assignments'



