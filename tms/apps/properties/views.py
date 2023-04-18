import datetime
import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

########################

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *

from ..core.models import managed_properties, tenant, rentals, payments
from ..core.views import alert


@login_required()
def register_property(request):
    form = PropertyRegForm(request.POST or None)

    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            property_name = form.cleaned_data.get("property_name")
            address = form.cleaned_data.get("address")
            city = form.cleaned_data.get("city")
            state = form.cleaned_data.get("state")
            country = form.cleaned_data.get("country")
            description = form.cleaned_data.get("description")
            landlord_code = form.cleaned_data.get("landlord")
            property_status = form.cleaned_data.get("property_status")
            date_registered = datetime.datetime.now()
            registered_by = form.cleaned_data.get("registered_by")

            #############################
            # Generate Unique Property Code
            # Randomly Choose Letters for adding to code
            def gencode():
                char1 = random.choice(string.ascii_uppercase)
                char2 = random.choice(string.ascii_lowercase)
                char3 = random.choice(string.ascii_letters)
                char4 = random.choice('1234567890')
                char5 = random.choice(string.ascii_uppercase)
                char6 = random.choice(string.ascii_lowercase)
                char7 = random.choice(string.ascii_letters)

                return f"prop/{char1}{char2}{char3}-{char4}{char5}/{char6}{char7}"

            #############################
            pty = gencode()
            property_code = pty
            while managed_properties.objects.filter(property_code=pty):
                pty = gencode()
                if not managed_properties.objects.filter(property_code=gencode):
                    property_code = gencode

            pt = managed_properties.objects.create(property_name=property_name.casefold(), address=address.casefold(),
                                                   city=city.casefold(), landlord=landlord_code,
                                                   state=state, country=country, description=description.casefold(),
                                                   date_registered=date_registered, property_status=property_status,
                                                   property_code=property_code, registered_by=registered_by)
            pt.save()
            messages.success(request, f'Property Registered Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("properties:registration"))

    context = {
        'form': form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }

    return render(request, 'properties/dashboards/property_register.html', context)


class PropertiesListView(ListView):
    model = managed_properties
    template_name = "properties/dashboards/properties_list.html"
    context_object_name = "properties"
    extra_context = {
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }
    ordering = ['id']
    paginate_by = 10
    group_by = "landlord"


@login_required()
def view_property(request, property_id):
    if property_id is None:
        messages.error(request, 'No Property Selected')
        return HttpResponseRedirect(reverse("properties:all"))
    else:
        try:
            sel_property = managed_properties.objects.get(id=property_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("properties:all"))

        # Get Tenants in property
        property_tenants = tenant.objects.filter(current_property=sel_property)
        count_tenants = len(property_tenants)

        # Get Rentals attached to the property
        property_tenancy = rentals.objects.filter(property=sel_property)
        count_tenancies = len(property_tenancy)

        # Get all payments
        rental_payments = payments.objects.all()

    context = {
        'property': sel_property,
        'tenants': property_tenants,
        'count': count_tenants,
        'tenancies': property_tenancy,
        'tenancy_count': count_tenancies,
        'all_payments': rental_payments,
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }

    return render(request, 'properties/dashboards/view_property.html', context)


@login_required()
def update_property(request, property_id):
    if property_id is None:
        messages.error(request, 'No Rental Selected')
        return HttpResponseRedirect(reverse("properties:all"))
    else:
        try:
            sel_property = managed_properties.objects.get(id=property_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("properties:all"))

        # Check for POST request
        if request.POST:
            u_form = PropertyUpdateForm(request.POST, instance=sel_property)

            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Property Details Updated Successfully.')
                return redirect('properties:view', property_id)
            else:
                messages.error(request, 'Something Went Wrong, Unable to update Property Details.')
        else:
            u_form = PropertyUpdateForm(instance=sel_property)
    return render(request, 'properties/dashboards/property_update.html', {'form': u_form, 'property': sel_property,
                                                                          'alertCount': alert()[1], 'alerts': alert()[0]})

