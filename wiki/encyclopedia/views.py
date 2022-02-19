"""docstring"""
from django import forms
from markdown2 import markdown
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse

class CreateNewForm(forms.Form):
    """Forms for creating a new page"""
    # references:
    # https://stackoverflow.com/questions/1080650/removing-the-label-from-djangos-textarea-widget
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-text-area-in-a-Django-form.php
    new_title = forms.CharField(label = "Entry Title")    
    new_article = forms.CharField(label = "", help_text = "", widget=forms.Textarea)  


def index(request):    
    """docstring"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()   # stores list of entries
    })

def entry(request, entry):
    """docstring"""
    content = util.get_entry(entry) # retrieves encyclopedia entry 
    if content is None:   # if no entry then an error page is rendered
        return render(request, "encyclopedia/error.html", {
            "entry": entry 
        })

    return render(request, "encyclopedia/entry.html", {   # if entry exists, then content is displayed
        "content": markdown(content),    # markdown converted to html
        "entry" : entry.capitalize(),    # capitalized the entry name (used in html title)
    })


def search(request):
    """docstring"""
    entry = request.GET.get("q")    #saves query
    entry_name = util.get_entry(entry)    #  retrieves entry of query
    if entry_name:     # if entry exists then user is brought to the page for that entry
        return HttpResponseRedirect(reverse("entry",
            kwargs={"entry" : entry})) 
    else:     #   if no entry exists with that specific name: 
        matches = []   #   a list is made of titles that have the query as a substring
        for title in util.list_entries():
            if entry.lower() in title.lower():
                matches.append(title)
        return render(request, "encyclopedia/match.html", { 
                    "matches": matches   
        })

def create(request):
    """docstring"""
    return render(request, "encyclopedia/create.html", {
        "form": CreateNewForm(),    # refers to class CreateNewForm() 
    })
