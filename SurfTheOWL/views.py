from django.shortcuts import render
from . import SurfTheOWL
import json

# Comment by Nick: This code is written by Manfred to implement html into Django

html_code = ""
# Create your views here.
def landing(request):  # initial call of the website
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    return render(request, 'SurfTheOWL.html', {'list_of_all_classes': list_of_all_classes})

def search(request): #search call of website
    global html_code
    html_code = ""
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    if request.method == 'POST':
        searched_class  =request.POST.get('searched_class')
        data = SurfTheOWL.main_search(searched_class) # Comment by Nick: Executes our main code
        data_tree = data[0]
        search_result_heading = next(iter(data_tree))
        def generate_html_form_dict_via_recusion(complete_dict, depth=0):
            global html_code
            for key in complete_dict.keys(): # for each key
                html_code += "<div class=\"layer" + str(depth + 2) + "_div\"><span class=\"bulletpoint\">&#8226; </span><span class=\"layer2\">" + key + " :</span>"
                if isinstance(complete_dict[key], str) or isinstance(complete_dict[key], list): # if dict key(value) is no dict
                    if isinstance(complete_dict[key], list): # if value is list
                        html_code += "<div class=\"list\">"
                        for element in complete_dict[key]: # for each element in list
                            html_code += "<li>" + element + "</li>" # insert each value
                        html_code += "</div></div>"
                    else: # if value is str
                        html_code += "<span class=\"layer" + str(depth + 2) + "_value\"> " + complete_dict[
                            key] + "</span></div><br>" # insert str
                        pass
                else: # if value is child dict
                    html_code += "<br>"
                    generate_html_form_dict_via_recusion(complete_dict[key], depth + 1) # call function again for child dict
                    html_code += "</div>"

        generate_html_form_dict_via_recusion(data_tree[list(data_tree.keys())[0]]) # call recursive function
        return render(request, 'SurfTheOWL.html', {'search_result_heading': search_result_heading,
                                                    'data_objects': data[1],
                                                    'list_of_all_classes': list_of_all_classes,
                                                   'html_code': html_code,
                                                   })
