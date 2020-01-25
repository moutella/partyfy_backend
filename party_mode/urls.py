from django.urls import path
from .views import Login, LoginReturnPage
urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('spotify_return/', LoginReturnPage.as_view(), name="login_return")
]