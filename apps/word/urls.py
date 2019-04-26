#
from django.urls import path
from . import views

app_name='word'
urlpatterns = [
    path('client_words/',views.ClientWordsView.as_view(),name='client_words'),
]