from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='base.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="base.html",
        email_template_name='password_reset_email.html', 
        subject_template_name='password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done_with_message')
    ), name='password_reset'),
    path('password_reset/done_with_message/', views.password_reset_done_with_message, name='password_reset_done_with_message'),
]
