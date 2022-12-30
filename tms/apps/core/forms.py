from django import forms
from .models import rentals, PROPERTY_USE, AGREEMENT_CHOICES, User, tenant, managed_properties, TENANCY_CHOICES

# Necessary Queryset for model choice fields
all_agents = User.objects.filter(usert_ype=2)
all_tenants = tenant.objects.all()
all_properties = managed_properties.objects.all()


# Form for Rentals Registration
class RentalRegForm(forms.Form):
    property = forms.TypedChoiceField(
        choices=all_properties,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Landlord Name"
            }
        ))

    tenant = forms.TypedChoiceField(
        choices=all_tenants,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Tenant Name"
            }
        ))

    proposed_use = forms.ChoiceField(
        choices=PROPERTY_USE,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number"
            }
        ))

    agreement_duration = forms.ChoiceField(
        choices=AGREEMENT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number"
            }
        ))

    status = forms.ChoiceField(
        choices=TENANCY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number"
            }
        ))

    date_started = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={
                'class': 'form-control form-control-select',
                'placeholder': " Select Start Date",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    date_ending = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={
                'class': 'form-control form-control-select',
                'placeholder': " Select End Date",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    rental_amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Rent Amount',
            }
        ))

    class meta:
        model = rentals
        fields = ('property', 'tenant', 'proposed_use', 'agreement_duration',
                  'status', 'date_started', 'date_ending', 'rental_amount')

