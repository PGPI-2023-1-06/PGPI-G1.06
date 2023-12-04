from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(authentication_form=EmailAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard'), name='logout'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

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

    #administration listar urls
    path('administration/admin_product_list/', views.admin_product_list, name='admin_product_list'),
    path('administration/admin_category_list/', views.admin_category_list, name='admin_category_list'),
    path('administration/admin_subject_list/', views.admin_subject_list, name='admin_subject_list'),
    path('administration/admin_professor_list/', views.admin_professor_list, name='admin_professor_list'),

    #administration create urls
    path('administration/product/', views.product_form, name='product'),
    path('administration/product/post', views.product_post, name='product_form'),
    path('administration/category/', views.category_form, name='category'),
    path('administration/category/post', views.category_post, name='category_form'),
    path('administration/professor/', views.professor_form, name='professor'),
    path('administration/professor/post', views.professor_post, name='professor_form'),
    path('administration/subject/', views.subject_form, name='subject'),
    path('administration/subject/post', views.subject_post, name='subject_form'),

    #administration delete urls
    path('administration/delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('administration/delete_category/<int:category_id>', views.delete_category, name='delete_category'),
    path('administration/delete_subject/<int:subject_id>', views.delete_subject, name='delete_subject'),
    path('administration/delete_professor/<int:professor_id>', views.delete_professor, name='delete_professor'),

    #administration update urls
    path('administration/update_product/<int:id>', views.update_product_form, name='update_product'),
    path('administration/update_product/post/', views.update_product_post, name='update_product_form'),
    path('administration/update_category/<int:id>', views.update_category_form, name='update_category'),
    path('administration/update_category/post/', views.update_category_post, name='category_update_form'),
    path('administration/update_subject/<int:id>', views.update_subject_form, name='update_subject'),
    path('administration/update_subject/post/', views.update_subject_post, name='subject_update_form'),
    path('administration/update_professor/<int:id>', views.update_professor_form, name='update_professor'),
    path('administration/update_professor/post/', views.update_professor_post, name='professor_update_form'),

    #reclamations urls
    path('administration/reclamation/', views.reclamations_list, name='reclamation'),
    path('administration/reclamation/close/<int:id>', views.close_reclamation, name='reclamation_close'),

    #sales_management urls
    path('administration/sales_management/', views.sales_management, name='sales_management'),
    path('administration/users_management/', views.users_management, name='users_management'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('administration/class_history/', views.class_history, name='class_history'),
    path('administration/sales_report/', views.sales_report, name='sales_report'),

]