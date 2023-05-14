from django.urls import path

from api.views import ads

urlpatterns = [
    path('ad/', ads.AdsListView.as_view()),
    path('ad/<int:pk>/', ads.AdDetailView.as_view()),
    path('ad/create/', ads.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', ads.AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', ads.AdDeleteView.as_view()),
]
