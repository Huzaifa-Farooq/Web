from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from markdown2 import markdown
import re
from django import forms
from . import util
from random import choice



class MyForm(forms.Form):
    title = forms.CharField(label='Title')
    md_content = forms.CharField(widget=forms.Textarea, label="\nMarkdown Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry(request, title):
    # Get entry from of titles
    title = title
    try:
        html = markdown(util.get_entry(title))
        # if title does not exists
    except TypeError:
        return render(request, "encyclopedia/apology.html", {
            "message": "Your requested page was not Found!"
        })
    else:
        return render(request, "encyclopedia/show_entry.html", {
            "text": html, "title": title
        })

def random_page(request):
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    return show_entry(request, random_entry)

# Create your views here.
def edit_page(request, page_title):

    filename = f"entries\\{page_title}.md"
    # open file to get contents
    with open(filename, 'r') as f:
        content = f.read()

    # getting title by reading only first line
    with open(filename, 'r') as f:
        title_file = f.readline()[1:]

    if request.method == "POST":
        # Getting markdown from form
        md_content = request.POST.get('content')


        # Writing content to the file
        with open(filename, 'w') as f:
            f.write(md_content)



        return redirect(f"http://127.0.0.1:8000/wiki/{page_title}")
    # User gets to the page via link or redirect
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "md_content": content, "title": title_file
        })


def search(request):
    """ Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry. """
    q = request.GET['q']
    search_results = []
    search_text = q.title()
    wiki_entries = util.list_entries()
    if search_text in wiki_entries:
        return show_entry(request, title=search_text)
    else:
        for wiki_entry in wiki_entries:
            # if search text is in wiki_entry
            if re.search(search_text, wiki_entry):
                search_results.append(wiki_entry)

        return render(request, "encyclopedia/search_result.html", {
            "search_results": search_results
        })


def create_new_page(request):
    """ adds new wiki entries """

    global title, md_content
    if request.method == "POST":
        form = MyForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            md_content = form.cleaned_data["md_content"]
        wiki_entries = util.list_entries()

        # Checks if title already exists
        if title in wiki_entries:
            return render(request, "encyclopedia/apology.html", {
                "message": "Another page with same title already exists"
            })
        else:
            filename = f"entries/{title}.md"
            with open(filename, 'w') as f:
                f.write(f"#{title}\n{md_content}")
            return show_entry(request, title)
    else:
        return render(request, "encyclopedia/create_new_page.html", {
            "form": MyForm(),
        })
