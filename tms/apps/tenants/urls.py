from django.urls import path, include

from . import views

urlpatterns = [
    path('tenants/', include(([
            path('register/', views.register_tenant, name="registration"),
            path('all/', views.TenantsListView.as_view(), name="all"),
        ], 'tms'), namespace='tenants')),
]
