from django.urls import path, include

from . import views

urlpatterns = [
    path('landlords/', include(([
            path('register/', views.register_landlord, name="registration"),
            path('all/', views.LandlordsListView.as_view(), name="all"),
            path('<int:landlord_id>/dashboard/', views.landlord_dashboard, name="dashboard")
        ], 'tms'), namespace='landlords')),
]
