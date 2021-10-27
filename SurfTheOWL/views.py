from django.shortcuts import render
from . import SurfTheOWL
from django.http import FileResponse
import json


# Comment by Nick: This code is written by Manfred to implement html into Django
search_output = {} # contains the return of maine_search()
html_code = "" # contains the data_tree in html code
context_type = ""
# Create your views here.
def welcome(request): # initial call of the website, after timeout redirected to landing
    return render(request, 'Welcome.html', {'OWL_file_name': SurfTheOWL.OWL_master_name})

def landing(request):  # landing after welcome
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    return render(request, 'SurfTheOWL.html', {'list_of_all_classes': list_of_all_classes})

def search(request): #search call of website
    global html_code
    html_code = ""
    global search_output
    search_output = {}
    global context_type
    context_type = ""
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    if request.method == 'POST':
        searched_class  =request.POST.get('searched_class')
        data = SurfTheOWL.main_search(searched_class) # Comment by Nick: Executes our main code
        search_output = data # save return of main_search as global variable to serve it in download
        data_tree = data[0]
        id_dict = data[3]
        comment_dict = data[4]
        context_type = data[5]
        instance_comment_dict = data[6]
        search_result_heading = next(iter(data_tree))

        def string_to_html_conform_string(string):
            string = string.replace('\'', '´')
            string = string.replace('\"', '´')
            return string

        def just_odd_layer_seperation(layer):
            if layer % 2 == 0:
                return "layer_just_div"
            else:
                return "layer_odd_div"

        def generate_html_form_dict_via_recursion(complete_dict, depth=0):
            global html_code
            if isinstance(complete_dict, dict):  # complete dict is dict and no list
                if len(complete_dict.keys()) == 2 and (complete_dict[list(complete_dict.keys())[1]] == 'float' or complete_dict[list(complete_dict.keys())[1]] == 'int') : # if is magnitude, consists always of two keys, the input value type is a float or a int
                    value_type = complete_dict[list(complete_dict.keys())[1]]
                    html_code += "<div class=\"list\"><table class=\"magnitude\">"
                    for element in complete_dict[list(complete_dict.keys())[0]]:
                        if element in instance_comment_dict.keys(): # if instance comment exist
                            html_code += "<tr><td class=\"magnitude_value\"><span class=\"bullet\"> &bull;  </span><span class=\"value_type\">"+str(value_type)+" </span>\
                            </td><td class=\"magnitude_unit\"><span class=\"tree_option tooltip\"><b>" + str(element) + "</b><span class=\"tooltiptext\">" + str(instance_comment_dict[element]) + "</span></span> \
                            <button onclick='copy_to_clipboard(\""+str(element)+"\")'>\
                            <img src='https://img.icons8.com/ios/10/000000/copy.png'/></button></td></tr>"
                        else:
                            html_code += "<tr><td class=\"magnitude_value\"><span class=\"bullet\"> &bull;  </span><span class=\"value_type\">"+str(value_type)+"</span>\
                            </td><td class=\"magnitude_unit\"><span class=\"tree_option\"> " + str(element) + "</span> \
                            <button onclick='copy_to_clipboard(\""+str(element)+"\")'>\
                            <img src='https://img.icons8.com/ios/10/000000/copy.png'/></button></td></tr>"
                    html_code += "</table></div>"
                else:
                    for key in complete_dict.keys(): # for each key
                        html_code += "<div class=" +just_odd_layer_seperation(depth) + "><hr class=\"limb_root\"><span class=\"bulletpoint\"> &#9660; </span>" \


                        if key in id_dict.keys() and key in comment_dict.keys():
                            html_code += "<div class=\"tooltip\"><b>" + key + " </b>" \
                                          "<span class=\"tooltiptext\"><b>ID: </b>"+id_dict[key]+"<br><b>Comment: </b><br>"+comment_dict[key]+"</span></div>"
                        else:
                            html_code += "<span><b>" + key + " </b></span> "
                        html_code += " <button onclick=\'copy_to_clipboard(\""+string_to_html_conform_string(key)+"\")\'>" \
                                    "<img src='https://img.icons8.com/ios/10/000000/copy.png'/></button>" \
                                    "<span><b> : </b></span>"

                        if isinstance(complete_dict[key], str) or isinstance(complete_dict[key], list): # if dict key(value) is no dict
                            if isinstance(complete_dict[key], list):  # if value is list, magnitudes a seperated before
                                html_code += "<div class=\"list\"><table>"
                                for element in complete_dict[key]: # for each element in list
                                    if element in instance_comment_dict.keys(): # if comment exist on instance
                                        html_code += "<tr><td><span class=\"bullet\"> &bull;  </span><span class=\"tree_option tooltip\"><b>" + str(element) + "</b><span class=\"tooltiptext\">" + str(instance_comment_dict[element]) + "</span></span> <button onclick='copy_to_clipboard(\""+str(element)+"\")'><img src='https://img.icons8.com/ios/10/000000/copy.png'/></button></td></tr>"
                                    else:
                                        html_code += "<tr><td><span class=\"bullet\"> &bull;  </span><span class=\"tree_option\">" + str(element) + "</span> <button onclick='copy_to_clipboard(\""+str(element)+"\")'><img src='https://img.icons8.com/ios/10/000000/copy.png'/></button></td></tr>" # insert each value
                                html_code += "</table></div></div>"

                            else: # if value is str
                                html_code += "<span class=\"tree_value\"> " + complete_dict[
                                    key] + "</span></div>" # insert str close main div
                                pass
                        else: # if value is child dict
                            if len(complete_dict[key].keys()) == 2 and (complete_dict[key][list(complete_dict[key].keys())[1]] == 'float' or complete_dict[key][list(complete_dict[key].keys())[1]] == 'int'):  # if child layer is  a magnitude  classified by float or int input value type dont add a html-break
                                pass # do nothing
                            else:
                                html_code += "<br>"
                            generate_html_form_dict_via_recursion(complete_dict[key], depth + 1) # call function again for child dict
                            html_code += "</div>" # close main div
            elif isinstance(complete_dict, list):  # if complete_dict is only a single list, in deep Objects possible
                html_code += "<div class=\"list\"><table>"#"<div class=\"list\">"
                for element in complete_dict:  # for each element in list
                    html_code += "<tr><td>" + element + "</td></tr>"  # insert each value
                html_code += "</table></div>"



        generate_html_form_dict_via_recursion(data_tree[list(data_tree.keys())[0]]) # call recursive function
        return render(request, 'SurfTheOWL.html', {'search_result_heading': [search_result_heading, id_dict[search_result_heading], comment_dict[search_result_heading], context_type],
                                                    'data_objects': data[1],
                                                    'list_of_all_classes': list_of_all_classes,
                                                   'html_code': html_code,
                                                   'ID_dict': id_dict,
                                                   'comment_dict': comment_dict,
                                                   })

def download_search_result_json(request): # function to serve a downloadable JSON to request
    global search_output
    global context_type
    searched_class = next(iter(search_output[0]))
    downloadable_json = {searched_class: {"Contextual Type": context_type,  "normal_Objects": search_output[0][searched_class]}}
    # beautify existing JSON by input the special objects and normal Objects separately
    downloadable_json[searched_class]["special_Objects"] = []
    for i in range(len(search_output[1])):
        downloadable_json[searched_class]["special_Objects"].append({search_output[1][i][0]:search_output[1][i][1]})


    json_file = json.dumps(downloadable_json, indent=2, sort_keys=True)  # make a json file
    response = FileResponse(json_file, charset='utf-8')  # setup response as File
    response['Content-Disposition'] = 'attachment; filename=' + str(searched_class)+ '.json' # name JSON file
    response['Content-Type'] = 'application/json' # specific file type

    return response