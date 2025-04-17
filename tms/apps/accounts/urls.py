
from django.urls import path, include
from django.contrib.auth.views import LogoutView as logout_view
from . import views

urlpatterns = [
    path('', views.login_redirect, name="landing"),

    path('login/', views.login_view, name="login"),

    path('logout/', logout_view.as_view(), name="logout"),

    path('agents/', include(([
            path('register/', views.register_agent, name="registration"),
            path('all/', views.AgentsListView.as_view(), name="all"),
            path('id/<int:agent_id>/view/', views.agent_info, name="agent_info")
        ], 'tms'), namespace='agents')),

    path('user/', include(([
                path('profile/', views.my_profile, name="profile"),
                path('profile/update/', views.profile_update, name="profile_update")
            ], 'tms'), namespace='accounts')),
]
