from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name= 'accounts'

urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup_step1/', views.signup_step1, name='signup_step1'),
    path('signup_step2/', views.signup_step2, name='signup_step2'),
    path('signup_step3/', views.signup_step3, name='signup_step3'),
    path('signup_step4/', views.signup_step4, name='signup_step4'),
    path('signup_step3_update/', views.signup_step3_update, name='signup_step3_update'),
    path('signup_step4_update/', views.signup_step4_update, name='signup_step4_update'),
    # path('config/', views.stripe_config, name='stripe_config'),
    # path('create-checkout-session/',views.onetime_payment_checkout , name='create-checkout'),
    # path('complete_mail/', views.complete_mail, name='complete_mail'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('signup_login/', views.Signup_Login.as_view(), name='signup_login'),
    path('terms_service/', views.terms_service, name='terms_service'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]