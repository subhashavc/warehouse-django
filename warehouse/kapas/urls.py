from django.conf.urls import url,include
from rest_framework import routers
from warehouse.kapas import views
from warehouse.kapas.views import CustomObtainAuthToken, LoginView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tokens', views.TokenViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'graphs',views.DailySiteReadingViewSet)




urlpatterns = [
    url('', include(router.urls)),
    url('auth/', CustomObtainAuthToken.as_view()),
    url('login/', LoginView.as_view())
]