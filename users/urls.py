from django.urls import path, include
from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register(r'location', views.LocationViewSet, basename='location')

urlpatterns = [
    path('user/', views.UserListView.as_view()),
    path('user/create/', views.UserCreateView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view()),
    path('', include(router.urls)),
]
