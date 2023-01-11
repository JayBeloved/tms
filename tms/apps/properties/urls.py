from django.urls import path, include

from . import views

urlpatterns = [
    path('properties/', include(([
        path('register/', views.register_property, name="registration"),
        path('all/', views.PropertiesListView.as_view(), name="all"),
        path('view/<int:property_id>/', views.view_property, name="view"),
    ], 'tms'), namespace='properties')),
]
