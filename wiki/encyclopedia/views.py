"""docstring"""
import random
from markdown2 import markdown
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


class CreateNewForm(forms.Form):
    """Forms for creating a new page"""
    # references:
    # https://stackoverflow.com/questions/1080650/removing-the-label-from-djangos-textarea-widget
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-text-area-in-a-Django-form.php
    new_title = forms.CharField(label = "Entry Title")   
    new_article = forms.CharField(label = "", help_text = "", widget=forms.Textarea)

class EditForm(forms.Form):
    """Form for editing a page"""
    # references:
    # https://stackoverflow.com/questions/1080650/removing-the-label-from-djangos-textarea-widget
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-text-area-in-a-Django-form.php
    edit_text = forms.CharField(label = "", help_text = "", widget=forms.Textarea)


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
    # if entry exists, then content is displayed
    return render(request, "encyclopedia/entry.html", {  
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
    # converts the list of entries to lowercase
    # reference: https://www.delftstack.com/howto/python/python-lowercase-list/
    lowercase_list = [title.lower() for title in util.list_entries()]   

    if request.method == "POST":
        form = CreateNewForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["new_title"]
            new_article = form.cleaned_data["new_article"]
        if new_title.lower() in lowercase_list:     # checks if the entry title already exists
            return render(request, "encyclopedia/entry_error.html", {     # renders an error page
                "new_title": new_title.capitalize()
            })
        else:
            util.save_entry(new_title, new_article)    # if its a new entry, the entry is saved

    return render(request, "encyclopedia/create.html", {
        "form": CreateNewForm(),    # refers to class CreateNewForm()
    })

def random_page(request):
    """docstring"""
    random_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry",
            kwargs = {"entry" : random_entry}))
