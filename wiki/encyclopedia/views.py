"""views.py file for wiki encyclopedia"""
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
    new_title = forms.CharField(label=" Entry Title ")
    new_article = forms.CharField(label="", help_text="", widget=forms.Textarea)



def index(request):
    """function renders index.html and provides a list of entries"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()   # stores list of entries
    })

def entry(request, entry):
    """Function for displaying entry"""
    content = util.get_entry(entry) # retrieves encyclopedia entry
    if content is None:   # if no entry then an error page is rendered
        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })
    # if entry exists, then content is displayed
    return render(request, "encyclopedia/entry.html", {
        "content": markdown(content),    # markdown converted to html
        "entry" : entry,
    })

def search(request):
    """Functionality for Wiki search form"""
    entry = request.GET.get("q")    #saves query
    entry_name = util.get_entry(entry)    #  retrieves entry of query
    if entry_name:     # if entry exists then user is brought to the page for that entry
        return HttpResponseRedirect(reverse("entry",
            kwargs={"entry" : entry}))   # reference: https://stackoverflow.com/questions/26197545/django-cant-pass-parameter-in-httpresponseredirect
    else:     #   if no entry exists with that specific name:
        matches = []   #   a list is made of titles that have the query as a substring
        for title in util.list_entries():
            if entry.lower() in title.lower():
                matches.append(title)
        return render(request, "encyclopedia/match.html", {
                    "matches": matches
        })

def create(request):
    """Functionality for creating a new Wiki article"""
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
            return HttpResponseRedirect(reverse("entry",
            kwargs={"entry" : new_title}))


    return render(request, "encyclopedia/create.html", {
        "form": CreateNewForm(),    # refers to class CreateNewForm()

    })

def edit(request, entry):
    """Functionality for editing Wiki entries"""
    content = util.get_entry(entry)   # retrieves entry to later prepopulate textarea

    # I had trouble changing the "initial" value when this form was outside of the function.
    # Though not ideal, I was able to change the value by including the class inside the edit function.
    class EditForm(forms.Form):
        """Form for editing a page"""
        # references:
        # https://stackoverflow.com/questions/1080650/removing-the-label-from-djangos-textarea-widget
        # http://www.learningaboutelectronics.com/Articles/How-to-create-a-text-area-in-a-Django-form.php
        edit_text = forms.CharField(initial = content, label="", help_text="", widget=forms.Textarea)

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            edit_text = form.cleaned_data["edit_text"]    
            util.save_entry(entry, edit_text)   # saves edited entry
            return HttpResponseRedirect(reverse("entry",
            kwargs={"entry" : entry}))

    return render(request, "encyclopedia/edit.html", {
        "form2": EditForm(),
        "entry" : entry,
        "content": content
    })

def random_page(request):
    """Chooses a random entry and redirects to the entry page"""
    random_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry",
            kwargs = {"entry" : random_entry}))
