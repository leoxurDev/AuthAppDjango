from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dashboard & Profile management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/delete-project/<int:project_id>/', views.delete_portfolio_item, name='delete_project'),
    
    # Public Profile view
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    
    # Custom Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/toggle-status/<int:user_id>/', views.admin_toggle_status, name='admin_toggle_status'),
    path('admin-dashboard/toggle-role/<int:user_id>/', views.admin_toggle_role, name='admin_toggle_role'),
    path('admin-dashboard/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

