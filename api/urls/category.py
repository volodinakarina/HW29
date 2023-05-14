from django.urls import path

from api.views import category

urlpatterns = [
    path('cat/', category.CategoryListView.as_view()),
    path('cat/<int:pk>/', category.CategoryDetailView.as_view()),
    path('cat/create/', category.CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', category.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', category.CategoryDeleteView.as_view()),
]
