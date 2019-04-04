from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('jedi/', views.jedi_list, name='jedi_list'),
    path('jedi/<slug:filter_param>/', views.jedi_list, name='jedi_list'),
    path('jedi/<int:pk>/', views.jedi_choose_padawan, name='jedi_choose_padawan'),
    path('jedi/<int:pk_jedi>/padawan/<int:pk_padawan>/', views.padawan_changing, name='padawan_changing'),
    path('candidate/', views.candidate_create, name='candidate_create'),
    path('candidate/<int:pk>/', views.candidate_testing, name='candidate_testing'),
]
