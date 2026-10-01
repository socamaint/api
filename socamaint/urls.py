from django.contrib import admin
from django.urls import path
from django.urls import path, include
from Ressources.views import register_user, forgot_password, update_password, DetailUser, DeleteUser, ListUser, ListNewUser
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from Entreprises.views import EseViews, ImportEnginView, VehiculeViewSet
from Compteurs.views import CompteurCreate
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()

router.register("region", EseViews, basename="region")
router.register("engins", VehiculeViewSet, basename="engins")
engin_router = routers.NestedSimpleRouter(router, "engins", lookup='engin')


engin_router.register("compteur", CompteurCreate, basename='engin-compteur')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user.as_view(), name='register-user'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('update-password/<str:token>/<str:uid>/', update_password, name='update_password'),

    path('detail/<str:pk>', DetailUser.as_view(), name='detail'),
    path('liste/', ListUser.as_view(), name='liste'),
    path('supprimer/<str:pk>', DeleteUser.as_view(), name='supprimer'),
    path('liste-user', ListNewUser.as_view(), name='liste-user'),

    path('import-engins', ImportEnginView.as_view(), name="import-engins"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


]+router.urls + engin_router.urls