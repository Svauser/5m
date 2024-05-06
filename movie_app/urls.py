from django.urls import path
from . import views
urlpatterns = [
    path('',views.director_list),
    path('<int:id>/', views.director_detail),
    path('', views.movie_list),
    path('<int:id>/', views.movie_detail),
    path('',views.review_list),
    path('<int:id>/', views.review_detail),
    path('reviews/', views.movie_reviews),
    path('count/', views.director_list_with_movies_count),


]