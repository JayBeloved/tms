import datetime
from django.db import models
from django.utils import timezone
from ..accounts.models import User
# State of Origin List

STATES = (
    ("Abia", 'Abia'),
    ("Adamawa", 'Adamawa'),
    ("Akwa-Ibom", 'Akwa-Ibom'),
    ("Anambra", 'Anambra'),
    ("Bauchi", 'Bauchi'),
    ("Bayelsa", 'Bayelsa'),
    ("Borno", 'Borno'),
    ("Cross-River", 'Cross-River'),
    ("Delta", 'Delta'),
    ("Ebonyi", 'Ebonyi'),
    ("Edo", 'Edo'),
    ("Ekiti", 'Ekiti'),
    ("Enugu", 'Enugu'),
    ("Gombe", 'Gombe'),
    ("Imo", 'Imo'),
    ("Jigawa", 'Jigawa'),
    ("Kaduna", 'Kaduna'),
    ("Kano", 'Kano'),
    ("Kastina", 'Kastina'),
    ("Kebbi", 'Kebbi'),
    ("Kogi", 'Kogi'),
    ("Kwara", 'Kwara'),
    ("Lagos", 'Lagos'),
    ("Nassarawa", 'Nassarawa'),
    ("Niger", 'Niger'),
    ("Ogun", 'Ogun'),
    ("Ondo", 'Ondo'),
    ("Osun", 'Osun'),
    ("Oyo", 'Oyo'),
    ("Plateau", 'Plateau'),
    ("Sokoto", 'Sokoto'),
    ("Sokoto", 'Sokoto'),
    ("Taraba", 'Taraba'),
    ("Yobe", 'Yobe'),
    ("Zamfara", 'Zamfara'),
    ("FCT", 'FCT'),

)

# Create Gender Choices
M = "Male"
F = "Female"

GENDER_CHOICES = (
    (M, 'Male'),
    (F, 'Female'),
)

# Status Choices
OCC = 1
VAC = 0

STATUS_CHOICES = (
    (OCC, "Occupied"),
    (VAC, "Vacant"),
)

# Marital Status Choices
NLL = "Null"
SNG = "Single"
MRD = "Married"
DVD = "Divorced"

MARITAL_STATUS = (
    (NLL, '_______'),
    (SNG, "Single"),
    (MRD, "Married"),
    (DVD, "Divorced"),
)
# Property Use Choices
RSD = "Residential"
BUZ = "Business"
PROPERTY_USE = (
    (RSD, "Residential Purpose"),
    (BUZ, "Business Purpose"),
)
# Agreement Duration Choices
MNT6 = 1
YR1 = 2
MNT18 = 3
YR2 = 4
YR3 = 5
YR5 = 6
AGREEMENT_CHOICES = (
    (MNT6, "6 Months"),
    (YR1, "1 Year"),
    (MNT18, "18 Months"),
    (YR2, "2 Years"),
    (YR3, "3 Years"),
    (YR5, "5 Years"),
)

# Nationality Choices
NGR = "Nigerian"
OTH = "International"
NATIONALITY_CHOICES = (
    (NGR, 'Nigeria'),
    (OTH, 'International'),
)


# Model for landlords
class landlord(models.Model):
    landlord_name = models.CharField(max_length=100, null=True)
    landlord_email = models.EmailField(null=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    state_of_origin = models.CharField(max_length=15, choices=STATES, default="FCT")
    date_registered = models.DateField('reg_date', default=timezone.now, null=True)
    landlord_code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"Landlord {self.landlord_code} - {self.landlord_name}"


class managed_properties(models.Model):
    property_name = models.CharField(max_length=60)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=15, choices=STATES, default="FCT")
    country = models.CharField(max_length=50)
    description = models.TextField(null=True)
    landlord = models.ForeignKey(landlord, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_registered = models.DateField('reg_date', default=timezone.now, null=True)
    property_status = models.PositiveSmallIntegerField('Property Status', choices=STATUS_CHOICES, default=VAC)
    property_code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.property_code} - {self.property_name}'


class tenant(models.Model):
    # Primary Details
    tenant_name = models.CharField(max_length=60, null=True)
    tenant_email = models.EmailField(null=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    current_property = models.ForeignKey(managed_properties, on_delete=models.CASCADE, to_field='property_code')
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, default=NLL)
    nationality = models.CharField(max_length=50, choices=NATIONALITY_CHOICES, default=NGR)
    tenant_code = models.CharField(max_length=30, unique=True, null=True)
    # Family Details
    next_of_kin = models.CharField(max_length=70, null=True)
    nok_contact = models.CharField(max_length=15, null=True, blank=True)
    # Business and other details
    occupation = models.CharField(max_length=50, null=True)
    industry = models.CharField(max_length=50, null=True)
    office_address = models.TextField(null=True)

    def __str__(self):
        return f"Tenant - {self.tenant_name}"


class rentals(models.Model):
    property = models.ForeignKey(managed_properties, on_delete=models.CASCADE, to_field='property_code')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    proposed_use = models.CharField(max_length=20, choices=PROPERTY_USE, default=RSD)
    date_started = models.DateField('Beginning of Rent', default=timezone.now, null=True)
    agreement_duration = models.PositiveSmallIntegerField('agreement duration', choices=AGREEMENT_CHOICES, default=YR1)
    rental_amount = models.CharField(max_length=30)
    date_ending = models.DateField('End of Rent', null=True)
    agreement_code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"Agreement {self.agreement_code} with {self.tenant}"

    