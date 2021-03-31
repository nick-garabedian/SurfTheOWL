from django.shortcuts import render
from . import SurfTheOWL
import json

# Create your views here.
def landing(request):  # initial call of the website
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    return render(request, 'SurfTheOWL.html', {'list_of_all_classes': list_of_all_classes})

def search(request): #search call of website
    list_of_all_classes = SurfTheOWL.searchable_owl_classes
    if request.method == 'POST':
        searched_class  =request.POST.get('searched_class')
        data_tree = SurfTheOWL.main_search(searched_class)
        search_result_heading = next(iter(data_tree))
    return render(request, 'SurfTheOWL.html', {'search_result_heading': search_result_heading,
                                               'data_tree': data_tree,
                                               'list_of_all_classes': list_of_all_classes})