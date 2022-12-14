import datetime
import random
import string
from django.utils import timezone
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

########################

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *

from ..core.models import landlord


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

            # Check email
            if landlord.objects.filter(landlord_email=landlord_email):
                messages.error(request, f'Email already in use by another Landlord. Use a unique email address')
            else:
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

                ld = landlord.objects.create(landlord_name=landlord_name, landlord_email=landlord_email,
                                             mobile_number=mobile_number, landlord_code=landlord_code,
                                             state_of_origin=state_of_origin, date_registered=date_registered)
                ld.save()
                messages.success(request, f'Landlord Registered Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("landlords:registration"))

    context = {
        'form': form,
    }

    return render(request, 'landlords/dashboards/landlord_register.html', context)


class LandlordsListView(ListView):
    model = landlord
    template_name = "landlords/dashboards/landlords_list.html"
    context_object_name = "landlords"
    ordering = ['id']
    paginate_by = 5
