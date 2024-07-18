from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from tournaments.views import TournamentViewSet
from matches.views import MatchViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"tournaments", TournamentViewSet)
router.register(r"matches", MatchViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Chess Tournament API",
        default_version="v1",
        description="API for managing chess tournaments",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@chesstournament.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
