from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import random as rn
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def add(request):
    if request.method == "POST":
        form = util.AddWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            # check that there is no other record with the same name
            if title not in util.list_entries():
                util.save_entry(title, form.cleaned_data['content'])
                return HttpResponseRedirect(reverse('wiki:index'))
            else:
                return HttpResponse(f'There is a record with {title} as the Title')
        else:
            return render(request, 'encyclopedia/add.html', {
                "form": util.AddWikiForm()
            })
    else:
        return render(request, "encyclopedia/add.html", {
            'form': util.AddWikiForm()
        })


def edit(request, title):
    if request.method != "POST":
        form = util.EditWikiForm(initial={'title': title, 'content': util.get_entry(title)})
        return render(request, 'encyclopedia/edit.html', {
            'title': title, 'form': form
        })
    elif request.method == 'POST':
        form = util.EditWikiForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']
            if form.has_changed():
                if title != new_title:
                    util.delete_entry(title)
                    util.save_entry(new_title, new_content)
                    return HttpResponseRedirect(reverse('wiki:index'))

                else:
                    util.save_entry(new_title, new_content)
                    return HttpResponseRedirect(reverse('wiki:index'))
            else:
                return HttpResponse("The entry has not been altered")
        else:
            return render(request, "encyclopedia/edit", {
                'form': util.EditWikiForm(initial={'title': title, 'content': util.get_entry(title)})
            })


def search(request):
    if request.method == "POST":
        try:
            s_form = util.SearchWikiForm(request.POST)
            s_form.is_valid()
            s_query = s_form.cleaned_data['q']
            s_query = s_query.lower()
            results_in_titles = set()
            for entry in util.list_entries():
                if s_query in entry.lower() or s_query in util.get_entry(entry).lower():
                    results_in_titles.add(entry)
                else:
                    continue
            return render(request, 'encyclopedia/search.html', {
                'results_in_titles': results_in_titles,
                'query': s_query
            })
        except:
            raise Exception


def random(request):
    entries = util.list_entries()
    rand = rn.randint(0, len(entries) - 1)
    return wiki(request, entries[rand])


def wiki(request, title):
    record_not_found = "Sorry, The Entry does not Exist"
    if title in util.list_entries():
        return render(request, "encyclopedia/wiki.html", {
            "title": title, "content": markdown2.markdown(util.get_entry(title))
        })
    else:
        return render(request, 'encyclopedia/error.html', {
            "err_message": record_not_found
        })
