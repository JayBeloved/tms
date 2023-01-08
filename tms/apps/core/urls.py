from django.urls import path, include
from . import views

urlpatterns = [
    path('adm/', include(([
        path('dashboard/', views.admin_index, name="dashboard"),
    ], 'tms'), namespace='my_admin')),

    path('rentals/', include(([
        path('new/', views.new_rental, name="new"),
        path('all/', views.RentalsListView.as_view(), name="all")
    ], 'tms'), namespace='rentals')),

    path('payments/', include(([
        path('new/', views.new_payment, name="new"),
        path('all/', views.PaymentsListView.as_view(), name="all")
    ], 'tms'), namespace='payments')),

]
