from django.urls import path
from .views import Login, LoginReturnPage, SessionView, MusicRequestView, Home
urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('spotify_return/', LoginReturnPage.as_view(), name="login_return"),
    path('session/<str:session_id>/', SessionView.as_view(), name="session"),
    path('request/', MusicRequestView.as_view(), name="music_request"),
    path('', Home.as_view(), name="home")
]