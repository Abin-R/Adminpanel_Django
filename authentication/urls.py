


from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.home ,name='home' ),
    path('signup/',views.signup ,name='signup' ),
    path('signin/',views.signin ,name='signin' ),
    path('signout/',views.signout ,name='signout' ),
    path('admins/',views.admins ,name='admins' ),
    # path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('edit_user/<int:user_id>/', views.edit_user , name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_user/',views.add_user ,name='add_user' ),
    path('forgot_password/',views.forgot_password ,name='forgot_password' ),
    path('reset_password/',views.reset_password ,name='reset_password' ),
    path('email_confirmation/',views.email_confirmation ,name='email_confirmation' ),
    
    
]
