from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /
    path("", views.index, name="index"),
    
    path("register/", views.register, name="register"),

    # ex: //5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
]