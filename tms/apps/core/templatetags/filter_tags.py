from django import template
# import payments model
from ..models import payments, landlord, managed_properties, tenant, rentals

register = template.Library()


@register.inclusion_tag("core/includes/pay_table.html")
def get_payments(tenancy):
    # Get all payments in the tenancy
    rent_payments = payments.objects.filter(rental=tenancy)
    count = len(rent_payments)

    return {
        'payments': rent_payments,
        'pay_count': count,
    }


@register.inclusion_tag("landlords/includes/_landlords_table.html")
def get_landlords(request):
    # Return all if user is an admin
    landlords = landlord.objects.all()
    l_count = landlords.__len__()
    if request.user.user_type == 2:
        # Get the landlord of the properties assigned to the surveyor
        landlords = set([p.landlord for p in managed_properties.objects.filter(registered_by=request.user)])
        l_count = landlords.__len__()

    return {
        'landlords': landlords,
        'count': l_count,
    }


@register.inclusion_tag("properties/includes/_properties_table.html")
def get_properties(request):
    # Return all if user is an admin
    properties = managed_properties.objects.all()
    p_count = properties.__len__()
    if request.user.user_type == 2:
        # Get the properties assigned to the surveyor
        properties = managed_properties.objects.filter(registered_by=request.user)
        p_count = properties.__len__()

    return {
        'properties': properties,
        'count': p_count,
    }


@register.inclusion_tag("tenants/includes/_tenants_table.html")
def get_tenants(request):
    # Return all if user is an admin
    tenants = tenant.objects.all()
    t_count = tenants.__len__()
    if request.user.user_type == 2:
        # Get the tenants of the properties assigned to the surveyor
        tenants = set([t for t in tenant.objects.all() if t.current_property in
                       managed_properties.objects.filter(registered_by=request.user)])
        t_count = tenants.__len__()

    return {
        'tenants': tenants,
        'count': t_count,
    }


@register.inclusion_tag("core/includes/_rentals_table.html")
def get_rentals(request):
    # Return all if user is an admin
    tenancy = rentals.objects.all()
    r_count = tenancy.__len__()
    if request.user.user_type == 2:
        # Get the tenancy terriers on the properties assigned to the surveyor
        tenancy = set([r for r in rentals.objects.all() if r.property in
                       managed_properties.objects.filter(registered_by=request.user)])
        r_count = tenancy.__len__()

    return {
        'rentals': tenancy,
        'count': r_count,
    }


@register.inclusion_tag("core/includes/_payments_table.html")
def fetch_payments(request):
    # Return all if user is an admin
    paymentz = payments.objects.all()
    p_count = paymentz.__len__()
    if request.user.user_type == 2:
        # Get the tenancy terriers on the properties assigned to the surveyor
        tenancy = set([r for r in rentals.objects.all() if r.property in
                       managed_properties.objects.filter(registered_by=request.user)])
        # Get the payments on the properties assigned to the surveyor
        paymentz = set([p for p in payments.objects.all() if p.rental in
                       tenancy])
        p_count = tenancy.__len__()

    return {
        'payments': paymentz,
        'count': p_count,
    }
