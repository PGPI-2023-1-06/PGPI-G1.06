from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(authentication_form=EmailAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),

    # reset password urls
    path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),

    #administration urls
    path('administration/product/', views.product_form, name='product'),
    path('administration/product/post', views.product_post, name='product_form'),
    path('administration/category/', views.category_form, name='category'),
    path('administration/category/post', views.category_post, name='category_form'),
    path('administration/subject/', views.subject_form, name='subject'),
    path('administration/subject/post', views.subject_post, name='subject_form'),
    path('administration/professor/', views.professor_form, name='professor'),
    path('administration/professor/post', views.professor_post, name='professor_form'),
    #reclamations urls
    path('administration/reclamation/', views.reclamations_list, name='reclamation'),
    path('administration/reclamation/close/<int:id>', views.close_reclamation, name='reclamation_close'),

    #sales_management urls
    path('administration/sales_management/', views.sales_management, name='sales_management'),
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

]