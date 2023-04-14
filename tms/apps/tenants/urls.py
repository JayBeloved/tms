from django.urls import path, include

from . import views

urlpatterns = [
    path('tenants/', include(([
            path('register/', views.register_tenant, name="registration"),
            path('all/', views.TenantsListView.as_view(), name="all"),
            path('<int:tenant_id>/info/', views.tenant_info, name="info"),
            path('<int:tenant_id>/update/', views.update_tenant, name="update"),
        ], 'tms'), namespace='tenants')),
]
