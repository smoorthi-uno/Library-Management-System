from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    street_address = models.CharField(max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=30, blank=True, null=True, default='')
    state = models.CharField(max_length=30, blank=True, null=True, default='')
    zip = models.CharField('Zip Code', max_length=5, blank=True, null=True, default='')
    mobile_num = models.CharField('Mobile Number', max_length=15, blank=True, null=True)
    email = models.EmailField(null=False, unique=True,
                              error_messages={'unique': 'A user with that email already exists.'})
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)


class Member(User):
    work_phone = models.CharField(max_length=15, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    is_member = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Member"

    def __str__(self):
        return self.username


class Librarian(User):
    work_phone = models.CharField(max_length=15, null=True)
    is_librarian = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Librarian"

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Author(models.Model):
    name = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # date_of_birth = models.DateTimeField(null=True, blank=True)
    # died = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, default='', blank=True, null=True)
    genre_name = models.ForeignKey(Genre, on_delete=models.CASCADE, default='', blank=True, null=True)
    available_copies = models.CharField(max_length=100)
    # Summary =
    # image =

    def __str__(self):
        return str(self.title)


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default='', blank=True, null=True)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, default='', blank=True, null=True)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, default='', blank=True, null=True)
    genre_name = models.ForeignKey(Genre, on_delete=models.CASCADE, default='', blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.member)
