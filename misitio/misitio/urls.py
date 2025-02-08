from django.contrib import admin
from django.urls import path, include
from punto_venta import views
from django.contrib.auth.views import LoginView, LogoutView
from punto_venta.views import register, menu_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('menu/', menu_view, name='menu'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("register/", register, name="register"),
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/edit/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
]
