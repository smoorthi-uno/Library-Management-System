from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SignUpForm(UserCreationForm):
    CHOICES = (
        ('Member', 'Member'),
        ('Librarian', 'Librarian'),
    )
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile_num', 'password1', 'password2', 'user_type')

    def save(self):
        user = super().save(commit=False)
        if self.user_type == 'Member':
            user = super().save(commit=False)
            user.is_staff = False
            user.save()
            Member.objects.create(user=user)
        else:
            user = super().save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            Librarian.objects.create(user=user)
        return user


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'mobile_num',
                  'work_phone', 'street_address', 'city', 'state', 'zip', 'interests',)


class MemberCreationForm(UserCreationForm):
    interests = forms.CharField(required=False, label='',
                                widget=forms.Textarea(attrs={'placeholder': 'Additional Information'}))

    class Meta(UserCreationForm):
        model = Member
        fields = ('first_name', 'last_name', 'email', 'mobile_num', 'work_phone', 'street_address', 'city', 'state',
                  'zip', 'interests',)

    def __init__(self, *args, **kwargs):
        super(MemberCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

    def save(self, commit=True, uname="unknown", pword="unknown"):
        self.cleaned_data['password1'] = pword
        member = super(MemberCreationForm, self).save(commit=False)
        member.username = uname
        member.first_name = self.cleaned_data['first_name']
        member.last_name = self.cleaned_data['last_name']

        if commit:
            member.save()
        return member


class LibrarianCreationForm(UserCreationForm):
    work_phone = forms.CharField(required=False, label='',
                                 widget=forms.Textarea(attrs={'placeholder': 'Additional Information'}))

    class Meta(UserCreationForm):
        model = Librarian
        fields = ('first_name', 'last_name', 'email', 'mobile_num', 'work_phone', 'street_address', 'city', 'state',
                  'zip',)

    def __init__(self, *args, **kwargs):
        super(LibrarianCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

    def save(self, commit=True, uname="unknown", pword="unknown"):
        self.cleaned_data['password1'] = pword
        librarian = super(LibrarianCreationForm, self).save(commit=False)
        librarian.username = uname
        librarian.is_staff = True
        librarian.first_name = self.cleaned_data['first_name']
        librarian.last_name = self.cleaned_data['last_name']

        if commit:
            librarian.save()
        return librarian


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ('member', 'book_name', 'author_name', 'genre_name', 'issue_date', 'return_date',)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'author_name', 'genre_name', 'available_copies',)


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'description',)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        # fields = ('first_name', 'last_name', 'date_of_birth', 'died', 'description',)
        fields = ('name', 'description',)
