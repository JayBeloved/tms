from django import forms
from ..core.models import managed_properties, STATES, tenant, STATUS_CHOICES, NATIONALITY_CHOICES, MARITAL_STATUS

# Industry Choices
INDUSTRIES = (
    ("Agric", "Agriculture, forestry, fishing, and hunting "),
    ("Mining", "Mining, quarrying, and oil and gas extraction"),
    ("Utilities", "Utilities"),
    ("Construction", "Construction"),
    ("Manufacturing", "Manufacturing"),
    ("Wholesale", "Wholesale trade"),
    ("Retail", "Retail trade"),
    ("Transport", "Transportation and warehousing"),
    ("Culture", "Information and cultural industries"),
    ("Finance", "Finance and insurance"),
    ("Real estate", "Real estate and rental and leasing"),
    ("Professional", "Professional, scientific and technical services"),
    ("Management", "Management of companies and enterprises"),
    ("Admin", "Administrative and support, waste management, and remediation services"),
    ("Education", "Educational services"),
    ("Health Care", "Health care and social assistance"),
    ("Arts & Ent.", "Arts, entertainment, and recreation"),
    ("Hospitality", "Accommodation and food services"),
    ("Others", "Other services (except public administration)"),
    ("Public Admin", "Public administration"),
)

# Occupation/Job title choice
OCCUPATION = (
    ("Executive", "Executive or Senior Management"),
    ("Middle", "Middle Management"),
    ("First", "First Level Management"),
    ("Senior", "Intermediate or Experienced (Senior Staff)"),
    ("Entry", "Entry Level")
)

all_properties = managed_properties.objects.all()


# Form for Landlord Registration
class TenantRegForm(forms.Form):
    tenant_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Tenant Name"
            }
        ))

    tenant_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': "Tenant Email",
            }
        ))

    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Tenant Mobile Number"
            }
        ))

    next_of_kin = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Next of Kin Full Name"
            }
        ))

    nok_contact = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': " Next of Kin Mobile Number"
            }
        ))

    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    nationality = forms.ChoiceField(
        choices=NATIONALITY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    office_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Office Address (for individuals).'
            }
        ))

    current_property = forms.ModelChoiceField(
        queryset=all_properties,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    industry = forms.ChoiceField(
        choices=INDUSTRIES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    occupation = forms.ChoiceField(
        choices=OCCUPATION,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class meta:
        model = tenant
        fields = ('tenant_name', 'tenant_email', 'mobile_number', 'next_of_kin', 'nok_contact', 'marital_status',
                  'nationality', 'office_address', "current_property", "industry", "occupation")

