from owlready2 import *
import re
from operator import itemgetter

property_restrictions = ['some', 'only', 'min', 'max', 'exactly', 'value', 'has_self'] # Comment by Nick: So that we know it's not a superclass
special_restrictions = [['hasTimeStamp', 'dateTimeStamp']]
OWL_master_name = 'TriboDataFAIR_v0.4.'
data_input_types = ['float', 'string', 'decimal', 'dateTimeStamp', 'boolean', 'PlainLiteral', 'integer', 'dateTimeStamp']
TriboDataFAIR = get_ontology('SurfTheOWL/TriboDataFAIR_v0.4.owl').load()
namespace = TriboDataFAIR.get_namespace('SurfTheOWL/TriboDataFAIR_v0.4.owl')

# reference to other Objects -------------------------------------------------------------------------------------------------
other_objects_properties = list(TriboDataFAIR.involves.subclasses())  # get all involves properties which refer to a other object

for property in other_objects_properties:  # get children of involves properties # Comment by Nick: Links to between objects and processes
    other_objects_properties += list(property.subclasses())  # add children to same property list

other_objects_properties = list(str(i).removeprefix(OWL_master_name)for i in other_objects_properties)  # convert list elements to string and remove master sufix

#----------------------------------------------------------------------------------------------------------------------

def get_all_classes_as_list(class_list):
    list_class_names = []
    for element in class_list:
        element_string = str(element).split('.')
        list_class_names.append(element_string[-1])  # Nick Edited
    return list_class_names
# Comment by Nick: Makes sure that the main_search is in the code
all_owl_classes = get_all_classes_as_list(TriboDataFAIR.classes())  # all owl things as list

# start define  searchable objects -----------------------------------------
def get_searchable_classes_from_list(classes_list):  # converts a list of classes in a list as pair with friendly name [[className, friendlyName], ....]
    searchable_classes_name_pair = []
    for element in classes_list:  # get friendly class Name
        searchable_classes_name_pair.append([element, className_to_friendlyName(element)])
    searchable_classes_name_pair = sorted(searchable_classes_name_pair, key=itemgetter(1)) # sort list after friendly name alphabetic order
    return searchable_classes_name_pair

# Comment by Nick: This is to get all the names in the drop-down search menu in the html
# executed ad end of file
Kadi4Mate_objects = str(TriboDataFAIR.Kadi4MatRecord.is_a[2])  # get properties of object Kadi4MateRecord, list element 3 contains Kadi4Mate objects and convert to string to enable manipulation
Kadi4Mate_objects = Kadi4Mate_objects.removeprefix('TriboDataFAIR_v0.4.documentsDescriptionOf.some(')  # remove main restriction
Kadi4Mate_objects = Kadi4Mate_objects.removesuffix(')') # remove leftofer
Kadi4Mate_objects = Kadi4Mate_objects.split(' | ') # convert to list of strings by spliting string on seperator
Kadi4Mate_objects = list(str(i).removeprefix(OWL_master_name)for i in Kadi4Mate_objects)  # for each string remove owl master name (TriboData.....)
#---------------------------------------------------------------------------------------------------------------------

def check_for_special_restriction(restriction):
    global special_restrictions
    for special_restriction in special_restrictions:
        if special_restriction[0] in restriction:
            return '<class \''+special_restriction[1]+'\'>'
    return False


def check_for_object_refer(restriction):
    global other_objects_properties, property_restrictions
    for other_object_property in other_objects_properties:
        if other_object_property in restriction:
            other_object = restriction.split(other_object_property)[1]
            for restriction in property_restrictions:
                if restriction in other_object:
                    other_object = other_object.removeprefix('.'+restriction)
                    other_object = other_object.removeprefix('('+OWL_master_name).removesuffix(')')
                    return '<object '+other_object+','+other_object_property+'>'  # <object 'refered_object, 'property_restriction'>
    return False


def property_restiction_in_string(string):
    global property_restrictions, special_restrictions, other_objects_properties
    for restriction in property_restrictions:
        if restriction in string:
            if check_for_special_restriction(string):
                return check_for_special_restriction(string)
            elif check_for_object_refer(string):
                return check_for_object_refer(string)
            else:
                prop = string.split(restriction)
                if ',' in prop[1]:
                    prop = prop[1].split(', ')

                    return prop[1]
                else:

                    return prop[1]

    return False

def bad_letter_in_string(string):
    bad_letter_elements = ['-', '.']
    for letter in bad_letter_elements:
        if letter in string or string[0].isdigit():
            return True

    return False


def get_data_instances(something):  # gets the instances of a Unit owl class
    friendly_name_instance_list = []
    if not is_class_datatype(something):
        string = 'TriboDataFAIR.'+something+'.instances()'
        instance_list = eval(string)

        if instance_list:  # returns true if list is not empty
            for i in range(len(instance_list)):
                instance_string = str(instance_list[i]).removeprefix(OWL_master_name)
                if not bad_letter_in_string(instance_string):
                    friendly_name_instance = eval('TriboDataFAIR.'+instance_string+'.friendlyName')
                    if friendly_name_instance:
                        friendly_name_instance_list.append(friendly_name_instance[0])
                    else:
                        friendly_name_instance_list.append(instance_string)

                else:
                    friendly_name_instance_list.append(instance_string)
        
        return friendly_name_instance_list





def search_class(className): # search all properties of a given class
    global OWL_master_name
    classes_list = []
    super_class = []
    search_string = 'TriboDataFAIR.'+className+'.is_a'
    property_list = eval(search_string)
    for property in property_list:
        property_string = property_restiction_in_string(str(property))

        if property_string:
            property_string = str(property_string).removeprefix('(').removesuffix(')')

            if OWL_master_name in property_string:
                classes_list.append(str(property_string).removeprefix(OWL_master_name))

            elif '<class 'in property_string:
                classes_list.append(str(property_string).removeprefix('<class \'').removesuffix('\'>'))

            elif '<object ' in property_string:
                classes_list.append(property_string)

        else:
            super_class.append(str(property).removeprefix(OWL_master_name))
    return classes_list


def is_class_datatype(className):  # if data type return True
    global data_input_types
    for input_type in data_input_types:
        if className in input_type:
            return True
    return False


def is_class_refer_other_object(className):  # if other object return True
    if '<object' in className:
        return True
    else:
        return False



def end_of_entries(className):  # returns if the end of the Tree Branch
    if is_class_datatype(className):
        return True
    elif is_class_refer_other_object(className):
        return True

    elif not search_class(className):
        return True

    else:
        return False

def is_class_a_thing(class_name):  # returns True or False if the Class is a OWL Thing
    global all_owl_classes
    for thing in all_owl_classes:
        if class_name == thing:
            return True
    return False

def className_to_friendlyName(class_name):  # returns the friendly name

    if is_class_a_thing(class_name): # is the class name a owl thing ?
        friendly_name_list = eval('TriboDataFAIR.'+class_name+'.friendlyName')# get friendly name from Class, delivers list with one item
        if friendly_name_list:
            friendly_name = friendly_name_list[0]

        else:
            friendly_name = class_name+" problem with friendly name"

    else:  # if not leave it as it is
        friendly_name = class_name

    return friendly_name


# end define searchable objects -----------------------------------------

def children(key):
    children_classes_dict = {}
    children_keys = []
    placeholder_keys = []
    friendly_names_dict = {}
    other_object_refer_pair = [] #[({object: property},{friendly object: property}),(...),...]
    if not end_of_entries(key):
        children_classes_dict = dict.fromkeys(search_class(key))
        placeholder_keys = list(children_classes_dict.keys())

    else:
        children_classes_dict = get_data_instances(key)
        friendly_names_dict = children_classes_dict  # if data assign to friendly names

    for i in range(len(placeholder_keys)):
        if is_class_datatype(placeholder_keys[i]):
            children_classes_dict['InputValueType'] = placeholder_keys[i]
            del children_classes_dict[placeholder_keys[i]]
            friendly_names_dict['Input Value Type'] = placeholder_keys[i]  # assign data type to friendly name

        elif is_class_refer_other_object(placeholder_keys[i]):
            referred_object_and_property = placeholder_keys[i].removeprefix('<object ').removesuffix('>').split(',')
            referred_object = referred_object_and_property[0]
            object_property = referred_object_and_property[1]
            children_classes_dict[referred_object] = object_property
            del children_classes_dict[placeholder_keys[i]]
            friendly_names_dict[className_to_friendlyName(referred_object)] = object_property  # assign object to friendly name
            other_object_refer_pair.append(({referred_object: object_property},{className_to_friendlyName(referred_object):object_property})) # list of refer objects, to manipulate existing list
        else:
            children_keys.append(placeholder_keys[i])
            friendly_names_dict[className_to_friendlyName(placeholder_keys[i])] = children_classes_dict[placeholder_keys[i]]  # assign dict data to friendly name

    return [children_classes_dict, children_keys, friendly_names_dict, other_object_refer_pair]


def main_search(className):
    if className in all_owl_classes:
        classes_dict = {className: []}
        friendly_class_name_list = eval('TriboDataFAIR.'+className+'.friendlyName')
        friendly_class_name = friendly_class_name_list[0]
        friendly_classes_dict = {friendly_class_name: []}

        def find_classes_layers_via_recursion(layer, keys, friendly_layer, depth=0): # keys are separate because some keys are a none owl thing

            if depth == 10:  # search depth
                return layer, friendly_layer
            else:

                for key in keys:
                    output = children(key)
                    layer[key] = output[0]  # class names
                    friendly_layer[className_to_friendlyName(key)] = output[2]  # friendly class names
                    next_layer_keys = output[1]  # needed because not every key is searchable, therefore the function children delivers all keys which a wanted keys

                    find_classes_layers_via_recursion(layer[key], next_layer_keys, friendly_layer[className_to_friendlyName(key)], depth + 1)

        find_classes_layers_via_recursion(classes_dict, [className], friendly_classes_dict)

        """placeholder list of refer objects for comparison an separation in existing list. prefer way because in further it might be necessary to get all objects"""
        object_refer_pair = children(className)[3] # at current state only possible to separate other objects referral in first layer

        # separate other objects for different appearance. prefer because further maybe complete datatree necessary -------------------------------
        # delete objects from class list ------------------
        if isinstance(classes_dict[className], dict):
            keys_p = list(classes_dict[className].keys())
            length = len(keys_p)
            i = 0
            while i < length: #delet other object refer from class list
                for item in object_refer_pair:
                    if keys_p[i] == list(item[0].keys())[0]:
                        if keys_p[i] in classes_dict[className]:
                            del classes_dict[className][keys_p[i]]
                            length -= 1
                i += 1

        # delete objects from friendly name list ----------------
        if isinstance(friendly_classes_dict[friendly_class_name], dict):
            keys_p_f = list(friendly_classes_dict[friendly_class_name].keys())
            length_f = len(keys_p)
            j = 0
            while j < length_f: #delet other object refer from class list (friendly name dict )
                for item in object_refer_pair:
                    if keys_p_f[j] == list(item[1].keys())[0]:
                        if keys_p_f[j] in friendly_classes_dict[friendly_class_name]:
                            del friendly_classes_dict[friendly_class_name][keys_p_f[j]]
                            length -= 1
                j += 1
            # generate object list with friendly name ----------------
            special_objects_friendly = [] # Structure = [[friendly object name, property ], [...], ...] list because possible overwrite as dict when tow keys are the same
            for item in object_refer_pair: # Structure= [({object: property},{friendly object: property}),(...),...]
                special_objects_friendly.append([list(item[1].keys())[0], item[1][list(item[1].keys())[0]]])
        else:
            special_objects_friendly = []
        # -------------------------------------------------------------------------------------------------------------------------------------------

        return [friendly_classes_dict, special_objects_friendly, classes_dict]

#search_string = "TribologicalExperiment"  # wanted OWL thing
#search_output = main_search(search_string)
#print(search_output[2])  # print dict with normal class names
#print(search_output)  # print dict with friendly names
searchable_owl_classes = get_searchable_classes_from_list(Kadi4Mate_objects) # all owl classes under Procedure which get the searchable classes in frontend

