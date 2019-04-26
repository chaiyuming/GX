from django.urls import path
from . import views

app_name='culture'
urlpatterns = [
    path('introduce/',views.CompanyIntroduceView.as_view(),name='introduce'),
    path('culture/',views.CompanyCultureView.as_view(),name='culture'),

]