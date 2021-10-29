import xml.etree.ElementTree as ET


def check_ids(owl_file_path):
    tree = ET.parse(owl_file_path)
    root = tree.getroot()
    classes_with_no_id = []
    classes_id = []
    duplicate_ids = []

    # get all ids and classes with no id
    for child in root: # some data (class etc.)
        if child.tag == '{http://www.w3.org/2002/07/owl#}Class':
            class_name = list(child.attrib.values()) # get class name
            class_name = class_name[0].replace('https://www.iam.kit.edu/cms/download/TriboDataFAIR_Ontology.owl#', '') # beautify class name
            id_in_child = False # determinate if class has id
            for element in child: # elements in data( comment, ID )
                if element.tag == '{https://www.iam.kit.edu/cms/download/TriboDataFAIR_Ontology.owl#}persistentID':  # if data has id
                    identifier = element.text # get id
                    classes_id.append([class_name, identifier]) # push classname and id in list
                    id_in_child = True # set bool that id is found
            if not id_in_child: # if in child no id is found push classname in list
                classes_with_no_id.append(class_name)

    # get duplicate ids
    for i in range(len(classes_id)): # foreach class do
        element = classes_id.pop(0) # get element and remove it from mother list
        ids = list(map(lambda item: item[1], classes_id)) # convert 2 dim. List to just 1 dim TDO-id-list
        if element[1] in ids: # if current id is also in leftover ids, than id is a duplicate one
            duplicate_ids.append((classes_id[i][0], element[1])) # if id is duplicate, save class name and id in list duplicate_ids

    return [duplicate_ids, classes_with_no_id]
