from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from lib.models import Book, Borrower, Transaction
from lib.forms import BookForm, BorrowerForm,TransactionForm
from django.db.models import Q
from datetime import date
 


# Create your views here.
@login_required(login_url='login')
def homePage(request):
    return render(request,'lib/home.html')

def loginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password is incorrect.')
    return render(request,'lib/login.html')

def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1!=password2:
            return HttpResponse('Please match password 1 and password 2')
        else:
            my_user = User.objects.create_user(username,email,password1)
            my_user.save()
            return redirect('login')
    return render(request,'lib/signup.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def aboutPage(request):
    return render(request,'lib/about.html')




# Book-related views
@login_required(login_url='login')
def book_list(request):
    books = Book.objects.all()
    return render(request, 'lib/book_list.html', {'books':books})

@login_required(login_url='login')
def book_detail(request):
    book_id = request.GET.get('book_id')
    error_message = None
    if book_id:
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            book = None
            error_message = 'No Match Found'
    else:
        book = None
    return render(request, 'lib/book_detail.html', {'book': book, 'error_message': error_message})

@login_required(login_url='login')
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'lib/book_add.html', {'form': form})


@login_required(login_url='login')
def edit_book(request):
    if request.method == 'POST':
        if 'fetch_book' in request.POST:
            book_id = request.POST.get('book_id')
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                book = None
                error_message = "No Match Found"
            else:
                error_message = None
                
            return render(request, 'lib/book_edit.html', {'book': book, 'error_message': error_message})
        elif 'update_book' in request.POST:
            book_id = request.POST.get('book_id')
            isbn = request.POST.get('isbn')
            title = request.POST.get('title')
            author = request.POST.get('author')
            genre = request.POST.get('genre')
            availability = request.POST.get('availability')
            publication_date = request.POST.get('publication_date')

            try:
                book = Book.objects.get(id=book_id)
                book.isbn = isbn
                book.title = title
                book.author = author
                book.genre = genre
                book.availability = availability
                book.publication_date = publication_date
                book.save()
                return redirect('book_edit')
            except Book.DoesNotExist:
                return redirect('book_edit')

    return render(request, 'lib/book_edit.html')

@login_required(login_url='login')
def delete_book(request):
    books = Book.objects.all()
    
    if request.method == 'POST':
        book_id = request.POST['book_id']
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return redirect('book_list')  # Redirect to the book list page after deletion
        except Book.DoesNotExist:
            pass

    return render(request, 'lib/book_delete.html', {'books': books})

#Borrower-related views:

@login_required(login_url='login')
def borrower_list(request):
    borrowers = Borrower.objects.all()
    return render(request, 'lib/borrower_list.html', {'borrowers': borrowers})

@login_required(login_url='login')
def borrower_detail(request):
    borrower_id = request.GET.get('borrower_id')
    error_message = None  # Initialize the error message

    if borrower_id:
        try:
            borrower = Borrower.objects.get(id=borrower_id)
        except Borrower.DoesNotExist:
            borrower = None
            error_message = "Borrower not found."  # Set the error message if borrower is not found
    else:
        borrower = None
    return render(request, 'lib/borrower_detail.html', {'borrower': borrower, 'error_message': error_message})

@login_required(login_url='login')
def borrower_add(request):
    if request.method == 'POST':
        form = BorrowerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('borrower_list')
    else:
        form = BorrowerForm()
    return render(request, 'lib/borrower_add.html', {'form': form})

@login_required(login_url='login')
def borrower_edit(request):
    if request.method == 'POST':
        if 'fetch_borrower' in request.POST:
            borrower_id = request.POST.get('borrower_id')
            error_message = None  # Define the error_message variable
            try:
                borrower = Borrower.objects.get(id=borrower_id)
            except Borrower.DoesNotExist:
                borrower = None
                error_message = "Borrower not found."
            return render(request, 'lib/borrower_edit.html', {'borrower': borrower, 'error_message': error_message})
        elif 'update_borrower' in request.POST:
            borrower_id = request.POST.get('borrower_id')
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')

            try:
                borrower = Borrower.objects.get(id=borrower_id)
                borrower.name = name
                borrower.email = email
                borrower.address = address
                borrower.phone_number = phone_number
                borrower.save()
                return redirect('borrower_list')
            except Borrower.DoesNotExist:
                return redirect('borrower_edit')

    return render(request, 'lib/borrower_edit.html')

@login_required(login_url='login')
def borrower_delete(request):
    borrowers = Borrower.objects.all()
    
    if request.method == 'POST':
        borrower_id = request.POST['borrower_id']
        try:
            borrower = Borrower.objects.get(id=borrower_id)
            borrower.delete()
            return redirect('borrower_list')  # Redirect to the borrower list page after deletion
        except Borrower.DoesNotExist:
            pass

    return render(request, 'lib/borrower_delete.html', {'borrowers': borrowers})





#Transaction-related views:
@login_required(login_url='login')
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'lib/transaction_list.html', {'transactions': transactions})

@login_required(login_url='login')
def transaction_detail(request):
    transaction = None

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        borrower_name = request.POST.get('borrower_name')

        if transaction_id:
            transaction = get_object_or_404(Transaction, id=transaction_id)
        elif borrower_name:
            transaction = get_object_or_404(Transaction, Q(borrower__name__iexact=borrower_name))

    return render(request, 'lib/transaction_detail.html', {'transaction': transaction})



@login_required(login_url='login')
def transaction_add(request):
    borrowers = Borrower.objects.all()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            book = transaction.book
            book.availability = False
            book.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    # Exclude books with availability=False from the queryset
    available_books = Book.objects.filter(availability=True)

    return render(request, 'lib/transaction_add.html', {'form': form, 'books': available_books, 'borrowers': borrowers})


# @login_required(login_url='login')
# def transaction_delete(request):
#     transactions = Transaction.objects.all()
    
#     if request.method == 'POST':
#         transaction_id = request.POST['transaction_id']
#         try:
#             transaction = Transaction.objects.get(id=transaction_id)
#             book = transaction.book
#             book.availability = True  # Update the availability to True
#             book.save()  # Save the changes
            
#             transaction.delete()
#             return redirect('transaction_list')  
#         except Transaction.DoesNotExist:
#             pass

#     return render(request, 'lib/transaction_delete.html', {'transactions': transactions})


@login_required(login_url='login')
def pay_fine(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        book = transaction.book
        fine = transaction.fine
        if request.method == 'POST':
            # Delete the transaction upon payment
            transaction.delete()
            # Set book availability to True
            book.availability = True
            book.save()
            return redirect('transaction_list')
        return render(request, 'lib/pay_fine.html', {'fine': fine})
    except Transaction.DoesNotExist:
        pass

    return redirect('transaction_list')


@login_required(login_url='login')
def transaction_delete(request):
    transactions = Transaction.objects.all()

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            book = transaction.book

            if date.today() > transaction.return_date:
                # If system date is greater than return date, redirect to pay_fine.html
                return redirect('pay_fine', transaction_id=transaction.id)
            else:
                # If system date is within return date, delete the transaction
                book.availability = True
                book.save()
                transaction.delete()
                return redirect('transaction_list')

        except Transaction.DoesNotExist:
            pass

    return render(request, 'lib/transaction_delete.html', {'transactions': transactions})



