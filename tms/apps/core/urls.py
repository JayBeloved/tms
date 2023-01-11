from django.urls import path, include
from . import views

urlpatterns = [
    path('adm/', include(([
        path('dashboard/', views.admin_index, name="dashboard"),
        path('admin-center/', views.management_index, name="mgt_index"),
        path('admin-center/tenancy-ending/one-month/', views.one_month, name="end_one_month"),
        path('admin-center/tenancy-ending/three-months/', views.three_months, name="end_three_months"),
        path('admin-center/tenancy-ending/six-months/', views.six_months, name="end_six_months"),
        path('admin-center/tenancy-ending/greater-than-six-months/', views.greater_than_six_month,
             name="end_greater"),
        path('admin-center/payment-percentage/fully-paid/', views.fully_paid,
             name="fully_paid"),
        path('admin-center/payment-percentage/eighty-percent/', views.eighty_percent,
             name="eighty_percent"),
        path('admin-center/payment-percentage/fifty-percent/', views.fifty_percent,
             name="fifty_percent"),
        path('admin-center/payment-percentage/less-than-fifty-percent/', views.less_than_fifty_percent,
             name="less_than_fifty"),
    ], 'tms'), namespace='my_admin')),

    path('rentals/', include(([
        path('new/', views.new_rental, name="new"),
        path('all/', views.RentalsListView.as_view(), name="all"),
        path('view/<int:rental_id>/', views.view_rental, name="view")
    ], 'tms'), namespace='rentals')),

    path('payments/', include(([
        path('new/', views.new_payment, name="new"),
        path('all/', views.PaymentsListView.as_view(), name="all")
    ], 'tms'), namespace='payments')),

]
