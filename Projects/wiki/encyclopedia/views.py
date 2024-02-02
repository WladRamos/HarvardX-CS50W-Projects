from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    if page is None:
        return render(request, "encyclopedia\error.html")
    else:
        return render(request, "encyclopedia\entry.html", {
            "title": title,
            "page_content": markdown2.markdown(page)
        })

def search(request):
    query = request.GET.get('q') #######################################
    entries = util.list_entries()

    matching_entries = []
    for entry in entries:
        if query.lower() in entry.lower():
            matching_entries.append(entry)

    if len(matching_entries) == 1:
        return HttpResponseRedirect(reverse('entry', args=[matching_entries[0]]))
    else:
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": matching_entries
        })