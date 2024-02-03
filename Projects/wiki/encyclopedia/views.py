from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    if page is None:
        return render(request, "encyclopedia\error.html", {
            "error": "Requested page was not found"
        })
    else:
        return render(request, "encyclopedia\entry.html", {
            "title": title,
            "page_content": markdown2.markdown(page)
        })

def search(request):
    query = request.GET.get('q')
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

def new_page(request):
    if request.method == "POST":
        title = request.POST.get('new_page_title')
        content = request.POST.get('new_page_content')
        entries = util.list_entries()
        
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia\error.html", {
                    "error": "Page title already exists"
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia\entry.html", {
            "title": title,
            "page_content": markdown2.markdown(content)
        })
    else:
        return render(request, "encyclopedia\\new_page.html")

def edit(request, page_title):
    if request.method == "POST":
        content = request.POST.get('new_page_content')
        util.save_entry(page_title, content)
        return render(request, "encyclopedia\entry.html", {
            "title": page_title,
            "page_content": markdown2.markdown(content)
        })
    else:
        page_content = util.get_entry(page_title)
        return render(request, "encyclopedia\edit.html", {
            "page_content": page_content,
            "page_title": page_title
        })

def random_page(request):
    entries = util.list_entries()
    n = random.randint(0, len(entries) - 1)
    title = entries[n]
    content = util.get_entry(title)
    return render(request, "encyclopedia\entry.html", {
            "title": title,
            "page_content": markdown2.markdown(content)
        })