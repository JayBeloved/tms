import datetime
import random
import string
from django.utils import timezone
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

########################

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *

from ..core.models import landlord, managed_properties, rentals
from ..core.views import alert


@login_required()
def register_landlord(request):
    form = LandlordRegForm(request.POST or None)

    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            landlord_email = form.cleaned_data.get("landlord_email")
            landlord_name = form.cleaned_data.get("landlord_name")
            mobile_number = form.cleaned_data.get("mobile_number")
            state_of_origin = form.cleaned_data.get("state_of_origin")
            date_registered = timezone.now()

            #############################
            # Generate Unique Landlord Code
            # Randomly Choose Letters for adding to code
            def gencode():
                char1 = random.choice(string.ascii_uppercase)
                char2 = random.choice(string.ascii_lowercase)
                char3 = random.choice(string.ascii_letters)
                char4 = random.choice('1234567890')
                char5 = random.choice(string.ascii_uppercase)
                char6 = random.choice(string.ascii_lowercase)
                char7 = random.choice(string.ascii_letters)

                return f"lnd/{char1}{char2}{char3}-{char4}{char5}/{char6}{char7}"

            #############################
            lnd = gencode()
            landlord_code = lnd
            while landlord.objects.filter(landlord_code=lnd):
                lnd = gencode()
                if not landlord.objects.filter(landlord_code=gencode):
                    landlord_code = gencode

            ld = landlord.objects.create(landlord_name=landlord_name.casefold(),
                                         landlord_email=landlord_email.casefold(),
                                         mobile_number=mobile_number, landlord_code=landlord_code,
                                         state_of_origin=state_of_origin, date_registered=date_registered)
            ld.save()
            messages.success(request, f'Landlord Registered Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("landlords:registration"))

    context = {
        'form': form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }

    return render(request, 'landlords/dashboards/landlord_register.html', context)


class LandlordsListView(ListView):
    model = landlord
    template_name = "landlords/dashboards/landlords_list.html"
    context_object_name = "landlords"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 2:
            # Get the landlords on the properties assigned to the surveyor
            queryset = list(set([p.landlord for p in managed_properties.objects.filter(registered_by=self.request.user)]))
        return queryset

    extra_context = {
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }
    ordering = ['id']
    paginate_by = 10


def landlord_dashboard(request, landlord_id):
    if landlord_id is None:
        messages.error(request, 'No Landlord Selected')
        return HttpResponseRedirect(reverse("landlords:all"))
    else:
        try:
            sel_landlord = landlord.objects.get(id=landlord_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("landlords:all"))

        # Get all the properties owned to the landlord
        landlord_properties = managed_properties.objects.filter(landlord=sel_landlord)

        # Get all rentals associated to the landlord's properties
        landlord_rentals = rentals.objects.all()

    context = {
        'properties': landlord_properties,
        'prop_count': len(landlord_properties),
        'landlord': sel_landlord,
        'rentals': landlord_rentals,
        'dbrentals': rentals,
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }

    return render(request, 'landlords/dashboards/landlord_dashboard.html', context)


@login_required()
def update_landlord(request, landlord_id):
    if landlord_id is None:
        messages.error(request, 'No Landlord Selected')
        return HttpResponseRedirect(reverse("landlords:all"))
    else:
        try:
            sel_landlord = landlord.objects.get(id=landlord_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("landlords:all"))

        # Check for POST request
        if request.POST:
            u_form = LandlordUpdateForm(request.POST, instance=sel_landlord)

            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Landlord Details Updated Successfully.')
                return redirect('landlords:dashboard', landlord_id)
            else:
                messages.error(request, 'Something Went Wrong, Unable to update Landlord Details.')
        else:
            u_form = LandlordUpdateForm(instance=sel_landlord)
    return render(request, 'landlords/dashboards/landlord_update.html', {'form': u_form, 'landlord': sel_landlord,
                                                                         'alertCount': alert()[1], 'alerts': alert()[0]})


