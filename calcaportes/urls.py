from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('empleado/', views.aportes_empleado, name='empleado'),
    path('historico/', views.historico, name='historico'),
    path('exportar_csv/', views.exportar_a_csv, name='exportar'),
] 