from django.urls import path

from . import views


urlpatterns = [
    path('recipe/', views.RecipeListView.as_view()),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
]