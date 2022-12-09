from django.urls import path, include

from . import views

urlpatterns = [
    path('properties/', include(([
            path('register/', views.register_property, name="registration"),
            path('all/', views.PropertiesListView.as_view(), name="all"),
        ], 'tms'), namespace='properties')),
]
