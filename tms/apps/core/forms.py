from django import forms
from .models import rentals, PROPERTY_USE, AGREEMENT_CHOICES, User, tenant, managed_properties

# Necessary Queryset for model choice fields
all_agents = User.objects.filter(usert_ype=2)
all_tenants = tenant.objects.all()
all_properties = managed_properties.objects.all()


# Form for Rentals Registration
class RentalRegForm(forms.Form):
    property = forms.ModelChoiceField(
        queryset=all_properties,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Landlord Name"
            }
        ))

    landlord_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Enter An Active Email Address",
            }
        ))

    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number"
            }
        ))

    state_of_origin = forms.ChoiceField(
        choices=STATES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'placeholder': " Select Select",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class meta:
        model = landlord
        fields = ('landlord_name', 'landlord_email', 'mobile_number', 'state_of_origin')

