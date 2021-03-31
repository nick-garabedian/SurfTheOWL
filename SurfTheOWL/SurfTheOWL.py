from owlready2 import *
import re
# Here I am testing the integration of Git and PyCharm

property_restrictions = ['some', 'only', 'min', 'max', 'exactly', 'value', 'has_self']
special_restrictions = [['hasTimeStamp', 'dateTimeStamp']]
OWL_master_name = 'TriboDataFAIR_v0.4.'
data_input_types = ['float', 'string', 'decimal', 'dateTimeStamp', 'boolean', 'PlainLiteral', 'integer', 'dateTimeStamp']

TriboDataFAIR = get_ontology('SurfTheOWL/TriboDataFAIR_v0.4.owl').load()
namespace = TriboDataFAIR.get_namespace('SurfTheOWL/TriboDataFAIR_v0.4.owl')

# reference to other Objects -------------------------------------------------------------------------------------------------
other_objects_properties = list(TriboDataFAIR.involves.subclasses())  # get all involves properties which refer to a other object

for property in other_objects_properties:  # get children of involves properties
    other_objects_properties += list(property.subclasses())  # add children to same property list


#other_objects_properties += list(TriboDataFAIR.hasPart.subclasses())  # get all hasPart properties which refer to a other object
other_objects_properties = list(str(i).removeprefix(OWL_master_name)for i in other_objects_properties)  # convert list elements to string and remove master sufix

# ----------------------------------------------------------------------------------------------------------------------------

def get_all_classes_as_list(class_list):
    list_class_names = []
    for element in class_list:
        element_string = str(element).split('.')
        list_class_names.append(element_string[-1]) # Nick Edited
    return list_class_names
all_owl_classes = get_all_classes_as_list(TriboDataFAIR.classes())  # all owl things as list

def get_searchable_classes_from_list(classes_list):  # converts a list of classes in a list as pair with friendly name [[className, friendlyName], ....]
    friendly_name_list = []
    normal_class_names = get_all_classes_as_list(classes_list) # get class name 

    for element in classes_list:  # get friendly class Name 
        friendly_name_list.append(element.friendlyName)

    searchable_classes_name_pair = []
    for i in range(len(friendly_name_list)):
        if friendly_name_list[i]:  # non searchable classes have no friendly name, so only append if friendly name exists
            searchable_classes_name_pair.append([normal_class_names[i],friendly_name_list[i][0]])
 
    return searchable_classes_name_pair

# all subs of Procedure get defined as searchable ---------------------------------------------------------------------
searchable_owl_classes = get_searchable_classes_from_list(list(TriboDataFAIR.Procedure.descendants())) # all owl classes under Procedure which get the searchable classes in frontend 
#----------------------------------------------------------------------------------------------------------------------


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
                    #print(prop[1])
                    return prop[1]
                else:
                    #print(prop)
                    #print(prop[1])
                    return prop[1]

    return False


def get_data_type(something):  # gets the input data type of an given owl class
    string = str(something).split('.')
    class_string = string[3].startswith(property_restrictions[0])  # is class .... property
    string = string[3].split('(')
    string[1] = string[1].replace(')', '')
    regular_expresion_search = re.search("\'(.+?)\'", string[1])  # get data type from string with regular expresion
    if regular_expresion_search:
        string[1] = regular_expresion_search.group(1)
    return string[1]


def bad_letter_in_string(string):
    bad_letter_elements = ['-', '.']
    for letter in bad_letter_elements:
        if letter in string or string[0].isdigit():
            return True

    return False


def get_data_instances(something):  # gets the instances of a Unit cowl class
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
        friendly_name = friendly_name_list[0]

    else:  # if not leave it as it is
        friendly_name = (class_name)

    return friendly_name


def children(key):
    children_classes_dict = {}
    children_keys = []
    placeholder_keys = []
    friendly_names_dict = {}
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

        else:
            children_keys.append(placeholder_keys[i])
            friendly_names_dict[className_to_friendlyName(placeholder_keys[i])] = children_classes_dict[placeholder_keys[i]]  # assign dict data to friendly name

    return [children_classes_dict, children_keys, friendly_names_dict]


def main_search(className):
    if className in all_owl_classes:
        classes_dic = {className: []}
        friendly_class_name_list = eval('TriboDataFAIR.'+className+'.friendlyName')
        friendly_class_name = friendly_class_name_list[0]
        friendly_classes_dic = {friendly_class_name: []}
        output = children(className)
        classes_dic[className] = output[0]
        first_layer_keys = output[1]
        friendly_classes_dic[friendly_class_name] = output[2]

        for key1 in first_layer_keys:
            #print(key1 + '    -key1')
            output1= children(key1)
            second_layer_keys = output1[1]
            classes_dic[className][key1] = output1[0]
            f_key1 = className_to_friendlyName(key1)
            friendly_classes_dic[friendly_class_name][f_key1] = output1[2]


            for key2 in second_layer_keys:
                #print(key2+'    -key2')
                output2 = children(key2)
                classes_dic[className][key1][key2] = output2[0]
                third_layer_keys = output2[1]
                f_key2 = className_to_friendlyName(key2)
                friendly_classes_dic[friendly_class_name][f_key1][f_key2] = output2[2]

                for key3 in third_layer_keys:
                    #print(key3+'    -key3')
                    output3 = children(key3)
                    classes_dic[className][key1][key2][key3] = output3[0]
                    fourth_layer_keys = output3[1]
                    f_key3 = className_to_friendlyName(key3)
                    friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3] = output3[2]

                    for key4 in fourth_layer_keys:
                        #print(key4+'    -key4')
                        output4 = children(key4)
                        classes_dic[className][key1][key2][key3][key4] = output4[0]
                        fifth_layer_keys = output4[1]
                        f_key4 = className_to_friendlyName(key4)
                        friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4] = output4[2]

                        for key5 in fifth_layer_keys:
                            #print(key5+'    -key5')
                            output5 = children(key5)
                            classes_dic[className][key1][key2][key3][key4][key5] = output5[0]
                            sixth_layer_keys = output5[1]
                            f_key5 = className_to_friendlyName(key5)
                            friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4][f_key5] = output5[2]

                            for key6 in sixth_layer_keys:
                                #print(key6+ '   -key6')
                                output6 = children(key6)
                                classes_dic[className][key1][key2][key3][key4][key5][key6] = output6[0]
                                seventh_layer_keys = output6[1]
                                f_key6 = className_to_friendlyName(key6)
                                friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4][f_key5][f_key6] = output6[2]

                                for key7 in seventh_layer_keys:
                                    #print(key7+ '  -key7')
                                    output7 = children(key7)
                                    classes_dic[className][key1][key2][key3][key4][key5][key6][key7] = output7[0]
                                    eighth_layer_keys = output7[1]
                                    f_key7 = className_to_friendlyName(key7)
                                    friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4][f_key5][f_key6][f_key7] = output7[2]

                                    for key8 in eighth_layer_keys:
                                        #print(key8+'    -key8')
                                        output8 = children(key8)
                                        classes_dic[className][key1][key2][key3][key4][key5][key6][key7][key8] = output8[0]
                                        ninth_layer_keys = output8[1]
                                        f_key8 = className_to_friendlyName(key8)
                                        friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4][f_key5][f_key6][f_key7][f_key8] = output8[2]

                                        for key9 in ninth_layer_keys:
                                            #print(key9+'    -key9')
                                            output9 = children(key9)
                                            classes_dic[className][key1][key2][key3][key4][key5][key6][key7][key8][key9] = output9[0]
                                            tenth_layer_keys = output9[1]
                                            f_key9 = className_to_friendlyName(key9)
                                            friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4][f_key5][f_key6][f_key7][f_key8][f_key9] = output9[2]

                                            for key10 in tenth_layer_keys:
                                                #print(key10+'   -key10')
                                                output10 = children(key10)
                                                classes_dic[className][key1][key2][key3][key4][key5][key6][key7][key8][key9][key10] = output10[0]
                                                eleventh_layer_keys = output10[1]
                                                f_key10 = className_to_friendlyName(key10)
                                                friendly_classes_dic[friendly_class_name][f_key1][f_key2][f_key3][f_key4][f_key5][f_key6][f_key7][f_key8][f_key9][f_key10] = output10[2]


        return friendly_classes_dic

#search_string = "TribologicalExperiment"  # wanted OWL thing
#search_output = main_search(search_string)
#print(search_output[0])  # print dict with normal class names
#print(search_output[1])  # print dict with friendly names

