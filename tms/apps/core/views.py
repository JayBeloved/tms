import datetime

from django.db.models.aggregates import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from .models import landlord, tenant, rentals, User, managed_properties


@login_required()
def admin_index(request):
    # User defined functions

    # Structure Counter
    all_agents = User.objects.filter(user_type=2)
    all_landlords = landlord.objects.all()
    all_tenants = tenant.objects.all()
    all_properties = managed_properties.objects.all()
    all_rentals = rentals.objects.all()

    property_count = all_properties.count()
    agents_count = all_agents.count()
    landlords_count = all_landlords.count()
    tenants_count = all_tenants.count()

    context = {
        'tenants_count': tenants_count,
        'agents_count': agents_count,
        'landlords_count': landlords_count,
        'property_count': property_count,
        'rentals': all_rentals,
    }
    return render(request, "dashboards/index.html", context)


