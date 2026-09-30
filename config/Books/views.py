from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

# READ (all)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# READ (one)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

# CREATE
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()                      # INSERT
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Add Book'})

# UPDATE
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)   # instance => update, not insert
        if form.is_valid():
            form.save()                      # UPDATE
            return redirect('book_list')
    else:
        form = BookForm(instance=book)       # pre-fills the form
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})

# DELETE
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()                        # DELETE
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})