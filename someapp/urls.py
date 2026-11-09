from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import index_view, configurator_view, login_view, register_view , logout_view

from .views import (
    RegisterView, ProfileView, CategoryViewSet, ProductViewSet, BuildViewSet,
    OrderViewSet, ReviewViewSet, index_view, configurator_view  
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('builds', BuildViewSet, basename='build')
router.register('orders', OrderViewSet, basename='order')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [

    path('', index_view, name='index'),
    path('configurator/', configurator_view, name='configurator'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', ProfileView.as_view(), name='profile'),


    path('api/', include(router.urls)),
]