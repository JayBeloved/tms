from django import forms
from .models import rentals, PROPERTY_USE, AGREEMENT_CHOICES, QUARTER_CHOICES, User, tenant, \
    managed_properties, payments

# Necessary Queryset for model choice fields
all_agents = User.objects.filter(user_type=2)
all_tenants = tenant.objects.all()
all_properties = managed_properties.objects.all()
all_payments = rentals.objects.all()


# Form for Rentals Registration
class RentalRegForm(forms.Form):
    property = forms.ModelChoiceField(
        queryset=all_properties,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Property ",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    tenant = forms.ModelChoiceField(
        queryset=all_tenants,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Tenant Name",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    proposed_use = forms.ChoiceField(
        required=False,
        choices=PROPERTY_USE,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    agreement_duration = forms.ChoiceField(
        required=False,
        choices=AGREEMENT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    date_started = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-select',
                'placeholder': " Select Start Date",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    date_ending = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                'type': 'date',
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
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class meta:
        model = rentals
        fields = ('property', 'tenant', 'proposed_use', 'agreement_duration',
                  'date_started', 'date_ending', 'rental_amount')


# Form for Rental Update
class RentalUpdateForm(forms.ModelForm):
    property = forms.ModelChoiceField(
        queryset=all_properties,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Property ",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    tenant = forms.ModelChoiceField(
        queryset=all_tenants,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Tenant Name",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    proposed_use = forms.ChoiceField(
        required=False,
        choices=PROPERTY_USE,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    agreement_duration = forms.ChoiceField(
        required=False,
        choices=AGREEMENT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Phone Number",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    date_started = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-select',
                'placeholder': " Select Start Date",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    date_ending = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                'type': 'date',
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
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = {'property': instance.pk}
            kwargs.setdefault('initial', initial)
        super().__init__(*args, **kwargs)

    class Meta:
        model = rentals
        fields = ('property', 'tenant', 'proposed_use', 'agreement_duration',
                  'date_started', 'date_ending', 'rental_amount')


# Form for payment record
class PaymentForm(forms.Form):
    rental = forms.ModelChoiceField(
        queryset=all_payments,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Rental ",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Amount Paid',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    payment_quarter = forms.ChoiceField(
        required=False,
        choices=QUARTER_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Payment Quarter",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class meta:
        model = payments
        fields = ('rental', 'amount', 'payment_quarter')


class PaymentUpdateForm(forms.Form):
    amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Amount Paid',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    payment_quarter = forms.ChoiceField(
        required=False,
        choices=QUARTER_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Payment Quarter",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class meta:
        model = payments
        fields = ('amount', 'payment_quarter')
