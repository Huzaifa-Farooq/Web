


filename = f"test.md"
with open(filename, 'w') as f:
    f.write(f"#test\n*abc#123")

from ctypes import string_at
from sys import getsizeof
from binascii import hexlify
a = 0x05546DC0
print(hexlify(string_at(id(a), getsizeof(a))))
print(id(a))

filename = "Huzaifa.md"
# open file to get contents
with open(filename, 'r') as f:
    content = f.read()
    print(content)

# getting title by reading only first line
with open(filename, 'r') as f:
    title_file = f.readline()[1:]
    print(title_file)

with open(filename, 'w') as f:
    f.write(f"{content}")

with open(filename, 'r') as f:
    print(f.read())

def create_new_page(request):
    """ adds new wiki entries """
    if request.method == "GET":
        return render(request, "encyclopedia/create_new_page.html")
    else:
        # Reads form data
        title = request.POST['title']
        markdown_content = request.POST['md_content']
        wiki_entries = util.list_entries()
        # Checks if title already exists
        if title in wiki_entries:
            return render(request, "encyclopedia/apology.html", {
                "message": "Another page with same titile already exists"
            })
        else:
            filename = f"entries/{title}.md"

            with open(filename, 'w') as f:
                f.write(f"#{title}\n{markdown_content}")
            return show_entry(request, title)