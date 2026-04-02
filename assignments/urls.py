from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('assignment/<int:assignment_id>/reject/', views.reject_assignment, name='reject_assignment'),
    path('submission/<int:submission_id>/review/', views.review_submission, name='review_submission'),
    path('assignments/', views.all_assignments, name='all_assignments'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
]
