"""docstring"""
from markdown2 import markdown
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse




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
    entry = request.GET.get("q")
    entry_name = util.get_entry(entry)
    if entry_name:
        return HttpResponseRedirect(reverse("entry",
            kwargs={"entry" : entry})) 
    else: 
        matches = []
        for title in util.list_entries():
            if entry.lower() in title.lower():
                matches.append(title)
        return render(request, "encyclopedia/match.html", {
                    "matches": matches
        })




