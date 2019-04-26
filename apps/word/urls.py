#
from django.urls import path
from . import views

app_name='word'
urlpatterns = [
    path('words/',views.ClientWordsView.as_view(),name='client_words'),
]