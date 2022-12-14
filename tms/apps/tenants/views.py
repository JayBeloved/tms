import random
import string
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

########################

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *

from ..core.models import tenant


@login_required()
def register_tenant(request):
    form = TenantRegForm(request.POST or None)

    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            tenant_name = form.cleaned_data.get("tenant_name")
            tenant_email = form.cleaned_data.get("tenant_email")
            mobile_number = form.cleaned_data.get("mobile_number")
            next_of_kin = form.cleaned_data.get("next_of_kin")
            nok_contact = form.cleaned_data.get("nok_contact")
            marital_status = form.cleaned_data.get("marital_status")
            nationality = form.cleaned_data.get("nationality")
            office_address = form.cleaned_data.get("office_address")
            current_property = form.cleaned_data.get("current_property")
            industry = form.cleaned_data.get("industry")
            occupation = form.cleaned_data.get("occupation")

            #############################
            if tenant.objects.filter(tenant_email=tenant_email):
                messages.error(request, f'Email already in use by another Tenant. Use a unique email address')
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

                    return f"tnt/{char1}{char2}{char3}-{char4}{char5}/{char6}{char7}"

                #############################
                tnt = gencode()
                tenant_code = tnt
                while tenant.objects.filter(tenant_code=tnt):
                    tnt = gencode()
                    if not tenant.objects.filter(tenant_code=gencode):
                        tenant_code = gencode

                tn = tenant.objects.create(tenant_name=tenant_name, tenant_email=tenant_email,
                                           mobile_number=mobile_number, next_of_kin=next_of_kin,
                                           nok_contact=nok_contact, marital_status=marital_status,
                                           nationality=nationality, office_address=office_address,
                                           current_property=current_property, tenant_code=tenant_code,
                                           industry=industry, occupation=occupation)
                tn.save()
                messages.success(request, f'Tenant Registered Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("tenants:registration"))

    context = {
        'form': form,
    }

    return render(request, 'tenants/dashboards/tenant_register.html', context)


class TenantsListView(ListView):
    model = tenant
    template_name = "tenants/dashboards/tenants_list.html"
    context_object_name = "tenants"
    ordering = ['id']
    paginate_by = 5
    group_by = "current_property"
