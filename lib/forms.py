from django import forms
from lib.models import Book, Borrower, Transaction


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'genre', 'publication_date', 'availability']

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['name', 'email', 'address', 'phone_number']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'borrower', 'borrow_date', 'return_date', 'fine']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'borrower': forms.Select(attrs={'class': 'form-control'}),
            'borrow_date': forms.DateInput(attrs={'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control'}),
            'fine': forms.NumberInput(attrs={'class': 'form-control'}),
        }
