from django.shortcuts import render
from . import SurfTheOWL
from django.http import FileResponse
import json


# Comment by Nick: This code is written by Manfred to implement html into Django
search_output = {} # contains the return of maine_search()
html_code = "" # contains the data_tree in html code
# Create your views here.
def landing(request):  # initial call of the website
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    return render(request, 'SurfTheOWL.html', {'list_of_all_classes': list_of_all_classes})

def search(request): #search call of website
    global html_code
    html_code = ""
    global search_output
    search_output = {}
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    if request.method == 'POST':
        searched_class  =request.POST.get('searched_class')
        data = SurfTheOWL.main_search(searched_class) # Comment by Nick: Executes our main code
        search_output = data # save return of main_search as global variable to serve it in download
        data_tree = data[0]
        search_result_heading = next(iter(data_tree))
        def just_odd_layer_seperation(layer):
            if layer%2 == 0:
                return "layer_just_div"
            else:
                return "layer_odd_div"


        def generate_html_form_dict_via_recusion(complete_dict, depth=0):
            global html_code
            if isinstance(complete_dict, dict):  # complete dict is dict and no list
                for key in complete_dict.keys(): # for each key
                    html_code += "<div class=" +just_odd_layer_seperation(depth) + "><hr class=\"limb_root\"><span class=\"bulletpoint\"> &#9660; </span><span class=\"layer"+ str(depth + 2) +"\"><b>" + key + " :</b></span>"
                    if isinstance(complete_dict[key], str) or isinstance(complete_dict[key], list): # if dict key(value) is no dict
                        if isinstance(complete_dict[key], list): # if value is list
                            html_code += "<div class=\"list\"><table>"#"<div class=\"list\">"
                            for element in complete_dict[key]: # for each element in list
                                html_code += "<tr><td>" + str(element) + "</td></tr>" # insert each value
                            html_code += "</table></div></div>"
                        else: # if value is str
                            html_code += "<span class=\"layer" + str(depth + 2) + "_value\"> " + complete_dict[
                                key] + "</span></div><br>" # insert str
                            pass
                    else: # if value is child dict
                        html_code += "<br>"
                        generate_html_form_dict_via_recusion(complete_dict[key], depth + 1) # call function again for child dict
                        html_code += "</div>"
            elif isinstance(complete_dict, list):  # complete_dict is only a single list, in deep Objects possible
                html_code += "<div class=\"list\"><table>"#"<div class=\"list\">"
                for element in complete_dict:  # for each element in list
                    html_code += "<tr><td>" + element + "</td></tr>"  # insert each value
                html_code += "</table></div>"


        generate_html_form_dict_via_recusion(data_tree[list(data_tree.keys())[0]]) # call recursive function
        return render(request, 'SurfTheOWL.html', {'search_result_heading': search_result_heading,
                                                    'data_objects': data[1],
                                                    'list_of_all_classes': list_of_all_classes,
                                                   'html_code': html_code,
                                                   })

def download_search_result_json(request):
    global search_output
    searched_class = next(iter(search_output[0]))
    downloadable_json = {searched_class:{"special_Objects":[]}}
    for i in range(len(search_output[1])):
        downloadable_json[searched_class]["special_Objects"].append({search_output[1][i][0]:search_output[1][i][1]})
    downloadable_json[searched_class]["normal_objects"] = search_output[0][searched_class]

    json_file = json.dumps(downloadable_json, indent=2, sort_keys=True)
    response = FileResponse(json_file, charset='utf-8')
    response['Content-Disposition'] = 'attachment; filename=' + str(searched_class)+ '_json_file'
    response['Content-Type'] = 'application/json'

    return response