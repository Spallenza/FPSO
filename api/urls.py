from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet, EquipmentViewSet, VesselViewSet
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'equipments', EquipmentViewSet)
router.register(r'vessels', VesselViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]