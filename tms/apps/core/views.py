import datetime
import random
import string

from django.utils import timezone
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from django.utils.decorators import method_decorator

from .models import landlord, tenant, rentals, User, managed_properties
from .forms import RentalRegForm


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


@login_required()
def new_rental(request):
    form = RentalRegForm(request.POST or None)

    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            rent_property = form.cleaned_data.get("property")
            rent_tenant = form.cleaned_data.get("tenant")
            proposed_use = form.cleaned_data.get("proposed_use")
            agreement_duration = form.cleaned_data.get("agreement_duration")
            status = form.cleaned_data.get("status")
            date_started = form.cleaned_data.get("date_started")
            date_ending = form.cleaned_data.get("date_ending")
            rental_amount = form.cleaned_data.get("rental_amount")
            agent = request.user

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

                return f"rnt/{char1}{char2}{char3}-{char4}{char5}/{char6}{char7}"

            #############################
            rnt = gencode()
            agreement_code = rnt
            while rentals.objects.filter(agreement_code=rnt):
                rnt = gencode()
                if not landlord.objects.filter(agreement_code=gencode):
                    agreement_code = gencode

            rt = rentals.objects.create(property=rent_property, tenant=rent_tenant, agent=agent,
                                        proposed_use=proposed_use, agreement_code=agreement_code,
                                        agreement_duration=agreement_duration, date_started=date_started,
                                        date_ending=date_ending, rental_amount=rental_amount, status=status)
            rt.save()
            messages.success(request, f'Tenancy Registered Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("rentals:new"))

    context = {
        'form': form,
    }

    return render(request, 'core/dashboards/rental_register.html', context)


class RentalsListView(ListView):
    model = rentals
    template_name = "core/dashboards/rentals_list.html"
    context_object_name = "rentals"
    ordering = ['id']
    paginate_by = 5
