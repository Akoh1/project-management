from django.urls import path
from . import views

app_name = 'account'

# admin.site.login = custom.site.login

urlpatterns = [
    path('', views.home, name='home'),
    path('index/<workplace>', views.index, name='index'),
    path('users/<workplace>', views.manage_users, name='manage_users'),
    path('index/', views.single_user_index, name='single-index'),
    path('account/sent/email', views.sent_mail, name='sent-email'),
    path('account/invite/users/<workplace>', views.invite_users, name='invite-users'),
    path('account/<slug:slug>/<workplace>', views.user_detail, name='user-detail'),
    path('account/signup', views.signup, name='signup'),
    path('account/signup/<workplace>/<email>', views.signup_workplace, name='signup-workplace'),
    path('account/login', views.login_view, name='login'),
    path('account/logout', views.logout_view, name='logout'),
    path('account/activate/view/<email>', views.activate_email, name='activate-email'),
    path('account/activate/test/<email>', views.activate, name='activate'),
]