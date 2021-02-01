from django.urls import path

from . import views

urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('search/', views.Search.as_view(), name='search'),
    path('filter/', views.FilterMovieList.as_view(), name='filter_list'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesViews.as_view(), name='json_filter'),
    path('actor/', views.ActorList.as_view(), name='actor_list'),
    path('<slug:slug>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>', views.ActorView.as_view(), name='actor_detail'),
]