import random
import string
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
########################

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *

from ..core.models import tenant, rentals, managed_properties
from ..core.views import alert


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

            tn = tenant.objects.create(tenant_name=tenant_name.casefold(), tenant_email=tenant_email.casefold(),
                                       mobile_number=mobile_number, next_of_kin=next_of_kin.casefold(),
                                       nok_contact=nok_contact, marital_status=marital_status,
                                       nationality=nationality, office_address=office_address.casefold(),
                                       current_property=current_property, tenant_code=tenant_code,
                                       industry=industry, occupation=occupation)
            tn.save()
            messages.success(request, f'Tenant Registered Successfully \n Enter Agreement Details')
            return redirect('rentals:new')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')
            return HttpResponseRedirect(reverse("tenants:registration"))

    context = {
        'form': form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }

    return render(request, 'tenants/dashboards/tenant_register.html', context)


class TenantsListView(ListView):
    model = tenant
    template_name = "tenants/dashboards/tenants_list.html"
    context_object_name = "tenants"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 2:
            # Get the tenants of the properties assigned to the surveyor
            queryset = list(set([t for t in tenant.objects.all() if t.current_property in
                                 managed_properties.objects.filter(registered_by=self.request.user)]))
        return queryset

    extra_context = {
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }
    ordering = ['id']
    paginate_by = 10
    group_by = "current_property"


def tenant_info(request, tenant_id):
    if tenant_id is None:
        messages.error(request, 'No Tenant Selected')
        return HttpResponseRedirect(reverse("agents:all"))
    else:
        try:
            sel_tenant = tenant.objects.get(id=tenant_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("tenants:all"))

    info_form = TenantInfoForm(instance=sel_tenant)

    context = {
        'tenant': sel_tenant,
        'form': info_form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }

    return render(request, 'tenants/dashboards/tenant_info.html', context)


@login_required()
def update_tenant(request, tenant_id):
    if tenant_id is None:
        messages.error(request, 'No Tenant Selected')
        return HttpResponseRedirect(reverse("tenant:all"))
    else:
        try:
            sel_tenant = tenant.objects.get(id=tenant_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("tenants:all"))

        # Check for POST request
        if request.POST:
            u_form = TenantUpdateForm(request.POST, instance=sel_tenant)

            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Tenant Details Updated Successfully.')
                return redirect('tenants:view', tenant_id)
            else:
                messages.error(request, 'Something Went Wrong, Unable to update Tenants Details.')
        else:
            u_form = TenantUpdateForm(instance=sel_tenant)
    return render(request, 'tenants/dashboards/tenant_update.html', {'form': u_form, 'tenant': sel_tenant,
                                                                     'alertCount': alert()[1], 'alerts': alert()[0]})


