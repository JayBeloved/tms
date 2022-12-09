from django.urls import path, include

from . import views

urlpatterns = [
    path('landlords/', include(([
            path('register/', views.register_landlord, name="registration"),
            path('all/', views.LandlordsListView.as_view(), name="all"),
        ], 'tms'), namespace='landlords')),
]
