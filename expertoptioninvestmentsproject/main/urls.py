from django.urls import path
from .views import index, login, logout_view, dashboard, account, register,rules, about, deposit, transaction, Withdrawal

app_name = 'main'

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name='about'),
    path('rules-agreement/', rules, name='rules'),
    path('dashboard/', dashboard, name="dashboard"),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('account/', account, name='account'),
    path('deposit/', deposit, name='deposit'), 
    path('transaction/', transaction, name='transaction'),
    path('withdraw/', Withdrawal, name='withdraw'),
]
