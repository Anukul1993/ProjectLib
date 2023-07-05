from django.contrib import admin
from django.urls import path
from lib import views
from lib.forms import TransactionForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.homePage, name='home'),
    path('', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutPage, name='logout'),
    path('about/',views.aboutPage, name='about'),

    path('book/add/', views.book_add, name='book_add'),
    path('book/list/', views.book_list, name='book_list'),
    path('book/detail/', views.book_detail, name='book_detail'),
    path('book/edit/', views.edit_book, name='book_edit'),
    path('delete/', views.delete_book, name='delete_book'),

    
    path('pay_fine/<int:transaction_id>/', views.pay_fine, name='pay_fine'),

    
    path('borrower/list/', views.borrower_list, name='borrower_list'),
    path('borrower/add/', views.borrower_add, name='borrower_add'),
    path('borrower/detail/', views.borrower_detail, name='borrower_detail'),
    path('borrower_edit/', views.borrower_edit, name='borrower_edit'),
    path('borrower_delete/', views.borrower_delete, name='borrower_delete'),

    path('transaction/list/', views.transaction_list, name='transaction_list'),
    path('transaction/add/', views.transaction_add, name='transaction_add'),
    path('transaction_detail/', views.transaction_detail, name='transaction_detail'),
    path('transaction_delete/', views.transaction_delete, name='transaction_delete'),
]
