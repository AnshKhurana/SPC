from django.urls import path, include
from rest_framework.routers import DefaultRouter
from filedatabase import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="SPC API")

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'filedatabase', views.FileViewSet, base_name='filerecord')
router.register(r'users', views.UserViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
    path('signup/', views.SignUp.as_view(), name='signup'),
    # path('useronly/, views.')
]