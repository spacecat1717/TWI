from django.urls import path
from account.views import (
            login_view,
            logout_view,
            account,
            registration,
        )


app_name = 'account'

urlpatterns  = [
    path('register/',registration, name="register" ),
    path('logout/',logout_view, name="logout" ),
    path('login/',login_view, name="login" ),
    path('profile/',account, name="account" ),
]