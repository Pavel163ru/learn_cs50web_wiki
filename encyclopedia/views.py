from django.shortcuts import render
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # get styling mark down text
    entry = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title
    })

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '') 
        entry = util.get_entry(query)
        if entry is not None:
            # return render(request, "encyclopedia/entry.html", {
            #     "entry": entry,
            #     "title": query
            # })
            return HttpResponseRedirect(reverse('entry', kwargs={
                "title": query
            }))
        else:
            entries = util.list_entries()
            entries = filter(lambda e: query in e, entries)
            entries
            return render(request, "encyclopedia/search.html", {
                "entries": entries,
                "query": query
            })
    return HttpResponseRedirect(reverse('index'))

def newpage(request):
    message = None
    if request.method == "POST":
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title != '' and content != '':
            entry = util.get_entry(title)
            if entry is not None:
                message = 'The entry already exist'
                return render(request, "encyclopedia/newpage.html", {
                    'message': message,
                    'title': title,
                    'content': content
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', kwargs={
                    "title": title
                }))
        else:
            message = 'Please fill the form'
    return render(request, "encyclopedia/newpage.html", {
        'message': message
    })

def editpage(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        content = request.POST.get('content', '')        
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', kwargs={
            "title": title
        }))
    return render(request, 'encyclopedia/editpage.html', {
        'title': title,
        'content': content
    })

def randompage(request):
    entries = util.list_entries()
    randompage = random.randrange(len(entries))
    randomtitle = entries[randompage] 
    return HttpResponseRedirect(reverse('entry', kwargs={
        "title": randomtitle
    }))