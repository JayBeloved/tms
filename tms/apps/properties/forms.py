from django import forms
from ..core.models import managed_properties, STATES, landlord, STATUS_CHOICES, User

# Country Choices
NGR = "Nigeria"
OTH = "Abroad"
COUNTRY_CHOICES = (
    (NGR, 'Nigeria'),
    (OTH, 'Abroad'),
)

all_landlord = landlord.objects.all()

all_surveyors = User.objects.filter(user_type=2)


# Form for Property Registration
class PropertyRegForm(forms.Form):
    property_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Property Name"
            }
        ))

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Property Address",
            }
        ))

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " City"
            }
        ))

    state = forms.ChoiceField(
        choices=STATES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    description = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Other Details about the property.'
            }
        ))

    landlord = forms.ModelChoiceField(
        queryset=all_landlord,
        to_field_name="landlord_name",
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    property_status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    registered_by = forms.ModelChoiceField(
        queryset=all_surveyors,
        to_field_name="username",
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class meta:
        model = managed_properties
        fields = ('property_name', 'address', 'city', 'state', 'country', 'description',
                  'landlord', 'property_status', 'registered_by')


# Form for Property Update
class PropertyUpdateForm(forms.ModelForm):
    property_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Property Name"
            }
        ))

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Property Address",
            }
        ))

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " City"
            }
        ))

    state = forms.ChoiceField(
        choices=STATES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    description = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Other Details about the property.'
            }
        ))

    landlord = forms.ModelChoiceField(
        queryset=all_landlord,
        to_field_name="landlord_name",
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    property_status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    registered_by = forms.ModelChoiceField(
        queryset=all_surveyors,
        to_field_name="username",
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    def __init__(self, *args, **kwargs):
        my_model_instance = kwargs.pop('sel_property', None)
        super(PropertyUpdateForm, self).__init__(*args, **kwargs)
        if my_model_instance:
            self.fields['landlord'].initial = my_model_instance

    class Meta:
        model = managed_properties
        fields = ('property_name', 'address', 'city', 'state', 'country', 'description',
                  'landlord', 'property_status', 'registered_by')
