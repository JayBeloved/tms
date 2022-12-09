from django.urls import path, include
from . import views

urlpatterns = [
    path('adm/', include(([
        path('dashboard/', views.admin_index, name="dashboard"),
    ], 'tms'), namespace='my_admin')),

]
