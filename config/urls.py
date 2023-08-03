from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from app import views
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", views.RegisterPage, name="register"),
    path("login/", views.LoginPage, name="login"),
    path("logout/", views.LogoutUser, name="logout"),
    path("", views.Home, name="home"),
    path("store/", views.StoreFront, name="store"),
    path("user/", views.UserPage, name="user_page"),
    path("account/", views.AccountSettings, name="account"),
    path("products/", views.ProductsPage, name="products"),
    path("customer/<str:pk>/", views.CustomerPage, name="customer"),
    path("create_order/<str:pk>/", views.CreateOrder, name="create_order"),
    path("update_order/<str:pk>/", views.UpdateOrder, name="update_order"),
    path("delete_order/<str:pk>/", views.DeleteOrder, name="delete_order"),
    path("create_customer/", views.CreateCustomer, name="create_customer"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
