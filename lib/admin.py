from django.contrib import admin
from lib.models import Book, Borrower, Transaction

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['id','isbn','title', 'author', 'genre','publication_date', 'availability']


class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'email', 'address', 'phone_number']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id','book', 'borrower', 'borrow_date', 'return_date', 'fine']



admin.site.register(Book,BookAdmin)
admin.site.register(Borrower,BorrowerAdmin)
admin.site.register(Transaction,TransactionAdmin)
