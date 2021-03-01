from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from library.forms import *
from library.models import *


def home(request):
    return render(request, 'library/home.html', {'library': home})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/signup.html", {"form": form})


# def register(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect("/home")
#     else:
#         form = SignUpForm()
#
#     return render(request, "registration/signup.html", {"form": form})


def signup_member(request):
    if request.method == 'POST':
        u = request.POST.get('first_name', '').lower() + "." + request.POST.get('last_name', '').lower()
        e = request.POST.get('email')
        p = User.objects.make_random_password(length=8)
        form = MemberCreationForm(request.POST)

        if form.is_valid():
            form.save(uname=u, pword=p)
            form.save_m2m()
            sendEmail_signup(e, p, u)
            return render(request, 'registration/signup_email.html')

        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = MemberCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# method for sending email after member registration
def sendEmail_signup(email, pwd, username):
    subject = "Welcome to Library Management System"
    content = {'pwd': pwd, 'uname': username, 'lms_site_name': 'Library Management System'}
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    with open("library/templates/registration/email_review_signup.txt") as f:
        signup_message = f.read()
    message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email,
                                     to=[to_email], )
    html_template = get_template("registration/signup_email_body.html").render(context=content)
    message.attach_alternative(html_template, "text/html")
    message.send()


@login_required
def member_list(request):
    member = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': member})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        # update
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.created_date = timezone.now()
            member.save()
            member = Member.objects.all()
            return render(request, 'library/member_list.html', {'members': member})
    else:
        # edit
        form = MemberForm(instance=member)
    return render(request, 'library/member_edit.html', {'form': form})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('library:member_list')


@login_required
def member_new(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            members = Member.objects.all()
            return render(request, 'library/member_list.html', {'members': members})
    else:
        form = MemberForm()
    return render(request, 'library/member_new.html', {'form': form})


@login_required
def borrow_list(request):
    borrows = Borrow.objects.all()
    return render(request, 'library/borrow_list.html', {'borrows': borrows})


@login_required
def borrow_new(request):
    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.save()
            borrows = Borrow.objects.all()
            return render(request, 'library/borrow_list.html', {'borrows': borrows})
    else:
        form = BorrowForm()
    return render(request, 'library/borrow_new.html', {'form': form})


@login_required
def borrow_edit(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    if request.method == "POST":
        form = BorrowForm(request.POST, instance=borrow)
        if form.is_valid():
            borrow = form.save()
            borrow.updated_date = timezone.now()
            borrow.save()
            borrows = Borrow.objects.all()
            return render(request, 'library/borrow_list.html', {'borrows': borrows})
    else:
        form = BorrowForm(instance=borrow)
    return render(request, 'library/borrow_edit.html', {'form': form})


@login_required
def borrow_delete(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    borrow.delete()
    return redirect('library:borrow_list')


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


@login_required
def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            # book.created_date = timezone.now()
            book.save()
            books = Book.objects.all()
            return render(request, 'library/book_list.html', {'books': books})
    else:
        form = BookForm()
    return render(request, 'library/book_new.html', {'form': form})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            book.updated_date = timezone.now()
            book.save()
            books = Book.objects.all()
            return render(request, 'library/book_list.html', {'books': books})
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_edit.html', {'form': form})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('library:book_list')


@login_required
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})


@login_required
def author_new(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            authors = Author.objects.all()
            return render(request, 'library/author_list.html', {'authors': authors})
    else:
        form = AuthorForm()
    return render(request, 'library/author_new.html', {'form': form})


@login_required
def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            author.save()
            authors = Author.objects.all()
            return render(request, 'library/author_list.html', {'authors': authors})
    else:
        form = AuthorForm(instance=author)
    return render(request, 'library/author_edit.html', {'form': form})


@login_required
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect('library:author_list')


@login_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'library/genre_list.html', {'genres': genres})


@login_required
def genre_new(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.save()
            genres = Genre.objects.all()
            return render(request, 'library/genre_list.html', {'genres': genres})
    else:
        form = GenreForm()
    return render(request, 'library/genre_new.html', {'form': form})


@login_required
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            genre = form.save()
            genre.save()
            genres = Genre.objects.all()
            return render(request, 'library/genre_list.html', {'genres': genres})
    else:
        form = GenreForm(instance=genre)
    return render(request, 'library/genre_edit.html', {'form': form})


@login_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    genre.delete()
    return redirect('library:genre_list')


from django.http import HttpResponse
from django.views.generic import View
from library.utils import render_to_pdf
from django.template.loader import get_template


def borrow_summary_pdf(request):
    borrows = Borrow.objects.all()
    context = {'borrows': borrows, }
    template = get_template('library/borrow_summary_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('library/borrow_summary_pdf.html', context)
    return pdf
