from django.urls import path
from .views import DashboardView, UsersView, UserDetail, AttendenseCreateView

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('users-list/', UsersView.as_view(), name='users_list'),
    path('user/<int:id>/', UserDetail.as_view(), name='user_detail'),
    path('api/attendense/', AttendenseCreateView.as_view(), name='attendense-create'),
]