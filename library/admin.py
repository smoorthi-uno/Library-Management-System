from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.http import HttpResponse
import csv


class MemberExportCsvMixin:
    def export_as_csv(self, request, queryset):
        members = Member.objects.all().only("id", "first_name", "last_name", "email", "mobile_num", "work_phone",
                                            "street_address", "city", "state", "zip", "interests")
        formatted_field_names = ['Member ID', 'Member Name', 'Email', 'Phone',
                                 'Work Phone', 'Address', 'City', 'State', 'ZIP', 'Interests']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Members_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        for member in queryset:
            writer.writerow(
                [member.id, member.first_name + " " + member.last_name, member.email, member.mobile_num,
                 member.work_phone, member.street_address, member.city, member.state, member.zip, member.interests])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class MemberAdmin(admin.ModelAdmin, MemberExportCsvMixin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'work_phone')
    actions = ["export_as_csv"]

    def username(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def work_phone(self, instance):
        try:
            return instance.work_phone
        except ObjectDoesNotExist:
            return 'ERROR!!'


class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'work_phone')
    actions = ["export_as_csv"]

    def username(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def work_phone(self, instance):
        try:
            return instance.work_phone
        except ObjectDoesNotExist:
            return 'ERROR!!'


class GenreList(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


class AuthorList(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name', 'description']


# class AuthorList(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'date_of_birth', 'died']
#     list_filter = ['first_name', 'last_name', 'date_of_birth', 'died']
#     search_fields = ['first_name', 'last_name', 'date_of_birth', 'died']
#     ordering = ['first_name']


class BookList(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'genre_name', 'available_copies')
    list_filter = ('title', 'author_name', 'genre_name', 'available_copies')
    search_fields = ('title', 'author_name', 'genre_name', 'available_copies')
    ordering = ['title']


class BorrowList(admin.ModelAdmin):
    list_display = ('member', 'book_name', 'author_name', 'genre_name', 'issue_date', 'return_date')
    list_filter = ('member', 'book_name', 'author_name', 'genre_name', 'issue_date', 'return_date')
    search_fields = ('member', 'book_name', 'author_name', 'genre_name', 'issue_date', 'return_date')
    ordering = ['member']


admin.site.register(Member, MemberAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Genre, GenreList)
admin.site.register(Author, AuthorList)
admin.site.register(Book, BookList)
admin.site.register(Borrow, BorrowList)
