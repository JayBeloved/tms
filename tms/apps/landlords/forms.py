from django import forms
from ..core.models import landlord, STATES


# Form for Landlord Registration
class LandlordRegForm(forms.Form):
    landlord_name = forms.CharField(
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

