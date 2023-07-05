from django.db import models

# Create your models here.

class Book(models.Model):
    isbn = models.IntegerField()
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    availability = models.BooleanField(default=True) 


class Borrower(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)


class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField()
    fine = models.IntegerField()

    class Meta:
        unique_together = ('book', 'borrower')
