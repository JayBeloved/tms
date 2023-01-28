import datetime
import random
import string
import pandas as pd
import numpy as np

from django.core.exceptions import ObjectDoesNotExist
# from django.utils import timezone
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import landlord, tenant, rentals, User, managed_properties, payments
from .forms import RentalRegForm, PaymentForm


# User Defined Functions
def alert():
    # Check if there are rentals in the database
    check = len(rentals.objects.all())
    if check > 0:
        # Get all rentals
        allrentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(allrentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # One Month or less
        df_one_month = df_rentals.loc[(df_rentals.days_left <= 30) & (df_rentals.days_left > -1)]
        count_one_month = df_one_month.shape[0]
        rng = range(5)
    else:
        df_one_month = []
        count_one_month = 0
        rng = 0

    return df_one_month, count_one_month, rng


@login_required()
def admin_index(request):
    # User defined functions

    # Structure Counter
    all_agents = User.objects.filter(user_type=2)
    all_landlords = landlord.objects.all()
    all_tenants = tenant.objects.all()
    all_properties = managed_properties.objects.all()
    all_rentals = rentals.objects.all()[:5]

    property_count = all_properties.count()
    agents_count = all_agents.count()
    landlords_count = all_landlords.count()
    tenants_count = all_tenants.count()

    context = {
        'tenants_count': tenants_count,
        'agents_count': agents_count,
        'landlords_count': landlords_count,
        'property_count': property_count,
        'rentals': all_rentals,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }
    return render(request, "dashboards/index.html", context)


def management_index(request):
    # Check if there are rentals in the database
    check = len(rentals.objects.all())
    count_one_month = 0
    count_three_months = 0
    count_six_months = 0
    count_fully_paid = 0
    count_greater = 0
    count_eighty = 0
    count_fifty = 0
    count_lower = 0
    if check > 0:
        # Get all Rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')
        '''
        Split the DataFrame to different dataframes depending on the days left.
        One Month or less, 3 months or less, 6 months or less, Fully paid rentals,
        80% or more paid rentals, 50% or more paid rentals, less than 50% paid rentals, Non paid rentals
        (i.e outstanding rentals.), rentals with court cases.
        '''
        # One Month or less
        df_one_month = df_rentals.loc[(df_rentals.days_left <= 30) & (df_rentals.days_left > -1)]
        count_one_month = df_one_month.shape[0]

        # 3 Months or less
        df_three_months = df_rentals.loc[(df_rentals.days_left <= 90) & (df_rentals.days_left > -1)]
        count_three_months = df_three_months.shape[0]

        # 6 Months or  Less
        df_six_months = df_rentals.loc[(df_rentals.days_left <= 180) & (df_rentals.days_left > -1)]
        count_six_months = df_six_months.shape[0]

        # Greater than 6 months
        df_greater = df_rentals[df_rentals['days_left'] > 180]
        count_greater = df_greater.shape[0]

        # Tenancy that have expired
        df_expired = df_rentals.loc[(df_rentals.days_left < 0)]
        count_expired = df_expired.shape[0]

        # Fully Paid rentals
        df_fully_paid = df_rentals[df_rentals['balance'] <= 0]
        count_fully_paid = df_fully_paid.shape[0]

        # Create a new field that calculates the percentage of payment made
        df_rentals['amount_paid'] = df_rentals['rental_amount'] - df_rentals['balance']
        df_rentals['percentage_paid'] = (df_rentals['amount_paid']/df_rentals['rental_amount']) * 100

        # 80% or more
        df_eighty = df_rentals[df_rentals['percentage_paid'] >= 80]
        count_eighty = df_eighty.shape[0]

        # 50% or more
        df_fifty = df_rentals[df_rentals['percentage_paid'] >= 50]
        count_fifty = df_fifty.shape[0]

        # less than 50%
        df_lower = df_rentals[df_rentals['percentage_paid'] < 50]
        count_lower = df_lower.shape[0]

    # Context data for display
    context = {
        'one_month_count': count_one_month,
        'three_months_count': count_three_months,
        'six_months_count': count_six_months,
        'count_expired': count_expired,
        'fully_paid': count_fully_paid,
        'count_greater': count_greater,
        'count_eighty': count_eighty,
        'count_fifty': count_fifty,
        'count_lower': count_lower,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/mgt_index.html', context)


@login_required()
def one_month(request):
    df_one_month = []
    count_one_month = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # One Month or less
        df_one_month = df_rentals.loc[(df_rentals.days_left <= 30) & (df_rentals.days_left > -1)].values
        count_one_month = df_one_month.shape[0]

    context = {
        'rentals': df_one_month,
        'count': count_one_month,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/one_month.html', context)


@login_required()
def three_months(request):
    df_three_months = []
    count_three_months = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # 3 Months or less
        df_three_months = df_rentals.loc[(df_rentals.days_left <= 90) & (df_rentals.days_left > -1)].values
        count_three_months = df_three_months.shape[0]

    context = {
        'rentals': df_three_months,
        'count': count_three_months,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/three_months.html', context)


@login_required()
def six_months(request):
    df_six_months = []
    count_six_months = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # 6 Months or  Less
        df_six_months = df_rentals.loc[(df_rentals.days_left <= 180) & (df_rentals.days_left > -1)].values
        count_six_months = df_six_months.shape[0]

    context = {
        'rentals': df_six_months,
        'count': count_six_months,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/six_months.html', context)


@login_required()
def greater_than_six_month(request):
    df_greater = []
    count_greater = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # Greater than 6 months
        df_greater = df_rentals.loc[(df_rentals.days_left <= 30) & (df_rentals.days_left > -1)].values
        count_greater = df_greater.shape[0]

    context = {
        'rentals': df_greater,
        'count': count_greater,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/greater_than_six_months.html', context)


@login_required()
def fully_paid(request):
    df_fully_paid = []
    count_fully_paid = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # Fully Paid rentals
        df_fully_paid = df_rentals.loc[(df_rentals['balance'] <= 0) & (df_rentals.days_left > -1)].values
        count_fully_paid = df_fully_paid.shape[0]

    context = {
        'rentals': df_fully_paid,
        'count': count_fully_paid,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/fully_paid.html', context)


@login_required()
def eighty_percent(request):
    df_eighty = []
    count_eighty = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # Create a new field that calculates the percentage of payment made
        df_rentals['amount_paid'] = df_rentals['rental_amount'] - df_rentals['balance']
        df_rentals['percentage_paid'] = (df_rentals['amount_paid'] / df_rentals['rental_amount']) * 100
        df_rentals['percentage_paid'] = round(df_rentals['percentage_paid'], 1)

        # 80% or more
        df_eighty = df_rentals.loc[(df_rentals['percentage_paid'] >= 80) & (df_rentals.days_left > -1)].values
        count_eighty = df_eighty.shape[0]

    context = {
        'rentals': df_eighty,
        'count': count_eighty,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/eighty_percent.html', context)


@login_required()
def fifty_percent(request):
    df_fifty = []
    count_fifty = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # Create a new field that calculates the percentage of payment made
        df_rentals['amount_paid'] = df_rentals['rental_amount'] - df_rentals['balance']
        df_rentals['percentage_paid'] = (df_rentals['amount_paid'] / df_rentals['rental_amount']) * 100
        df_rentals['percentage_paid'] = round(df_rentals['percentage_paid'], 1)

        # 50% or more
        df_fifty = df_rentals.loc[(df_rentals['percentage_paid'] >= 50) & (df_rentals.days_left > -1)].values
        count_fifty = df_fifty.shape[0]

    context = {
        'rentals': df_fifty,
        'count': count_fifty,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/fifty_percent.html', context)


@login_required()
def less_than_fifty_percent(request):
    df_lower = []
    count_lower = 0
    if len(rentals.objects.all()) > 0:
        # Get all rentals
        all_rentals = rentals.objects.all()
        # Create DataFrame of all Rental Agreements
        df_rentals = pd.DataFrame.from_records(all_rentals.values())

        # Convert date ending and date started to datetime datatype
        df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
        df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

        # Add a new column today that will store the value of today's date
        d_year = int(datetime.datetime.now().strftime('%Y'))
        d_month = int(datetime.datetime.now().strftime('%m'))
        d_day = int(datetime.datetime.now().strftime('%d'))

        today = datetime.datetime(d_year, d_month, d_day)

        df_rentals['today'] = np.datetime64(today)

        # Add a new column that counts the number of days left
        df_rentals['days_left'] = df_rentals['date_ending'] - df_rentals['today']
        # Convert to float
        df_rentals['days_left'] = df_rentals['days_left'] / np.timedelta64(1, 'D')

        # Create a new field that calculates the percentage of payment made
        df_rentals['amount_paid'] = df_rentals['rental_amount'] - df_rentals['balance']
        df_rentals['percentage_paid'] = (df_rentals['amount_paid'] / df_rentals['rental_amount']) * 100
        df_rentals['percentage_paid'] = round(df_rentals['percentage_paid'], 1)

        # less than 50%
        df_lower = df_rentals.loc[(df_rentals['percentage_paid'] < 50) & (df_rentals.days_left > -1)].values
        count_lower = df_lower.shape[0]

    context = {
        'rentals': df_lower,
        'count': count_lower,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/less_than_fifty_percent.html', context)


@login_required()
def new_rental(request):
    form = RentalRegForm(request.POST or None)

    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            rent_property = form.cleaned_data.get("property")
            rent_tenant = form.cleaned_data.get("tenant")
            proposed_use = form.cleaned_data.get("proposed_use")
            agreement_duration = form.cleaned_data.get("agreement_duration")
            remarks = "Fresh Tenancy".casefold()
            date_started = form.cleaned_data.get("date_started")
            date_ending = form.cleaned_data.get("date_ending")
            rental_amount = form.cleaned_data.get("rental_amount")
            agent = request.user

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

                return f"rnt/{char1}{char2}{char3}-{char4}{char5}/{char6}{char7}"

            #############################
            rnt = gencode()
            agreement_code = rnt
            while rentals.objects.filter(agreement_code=rnt):
                rnt = gencode()
                if not landlord.objects.filter(agreement_code=gencode):
                    agreement_code = gencode

            rt = rentals.objects.create(property=rent_property, tenant=rent_tenant, agent=agent,
                                        proposed_use=proposed_use, agreement_code=agreement_code,
                                        agreement_duration=agreement_duration, date_started=date_started,
                                        date_ending=date_ending, rental_amount=rental_amount, remarks=remarks,
                                        balance=rental_amount)
            rt.save()
            messages.success(request, f'Tenancy Registered Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("rentals:new"))

    context = {
        'form': form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/rental_register.html', context)


class RentalsListView(ListView):
    model = rentals
    template_name = "core/dashboards/rentals_list.html"
    context_object_name = "rentals"
    extra_context = {
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }
    ordering = ['id']
    paginate_by = 5


@login_required()
def new_payment(request):
    form = PaymentForm(request.POST or None)

    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            rental = form.cleaned_data.get("rental")
            amount = form.cleaned_data.get("amount")
            payment_date = form.cleaned_data.get("payment_date")

            #############################
            # Generate Unique Payment Code
            # Randomly Choose Letters for adding to code
            def gencode():
                char1 = random.choice(string.ascii_uppercase)
                char2 = random.choice(string.ascii_lowercase)
                char3 = random.choice(string.ascii_letters)
                char4 = random.choice('1234567890')
                char5 = random.choice(string.ascii_uppercase)
                char6 = random.choice(string.ascii_lowercase)
                char7 = random.choice(string.ascii_letters)

                return f"pmt/{char1}{char2}{char3}-{char4}{char5}/{char6}{char7}"

            #############################
            pmt = gencode()
            payment_code = pmt
            while payments.objects.filter(payment_code=pmt):
                pmt = gencode()
                if not payments.objects.filter(payment_code=gencode):
                    payment_code = gencode

            pt = payments.objects.create(rental=rental, amount=amount, payment_date=payment_date,
                                         payment_code=payment_code)
            pt.save()

            # Reflect Change in the rentals table
            sel_rental = rentals.objects.get(id=rental.id)
            # Clean and convert currency to integers
            current_balance = float(str(sel_rental.balance).replace(',', ''))
            amount_paid = float(str(amount).replace(',', ''))

            sel_rental.balance = current_balance - amount_paid
            sel_rental.save()

            new_balance = float(str(sel_rental.balance).replace(',', ''))
            # Update Remarks
            if new_balance > 0:
                sel_rental.remarks = f"N {new_balance} rent is outstanding"
                sel_rental.save()
            elif new_balance == 0:
                sel_rental.remarks = f"Tenancy is Running"
                sel_rental.save()

            messages.success(request, f'Payment Recorded Successfully')
        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("payments:new"))

    context = {
        'form': form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/record_payment.html', context)


class PaymentsListView(ListView):
    model = payments
    template_name = "core/dashboards/payments_list.html"
    context_object_name = "payments"
    extra_context = {
        'alertCount': alert()[1],
        'alerts': alert()[0],
    }
    ordering = ['-id']
    paginate_by = 5


@login_required()
def view_rental(request, rental_id):
    if rental_id is None:
        messages.error(request, 'No Rental Selected')
        return HttpResponseRedirect(reverse("rentals:all"))
    else:
        try:
            sel_rental = rentals.objects.get(id=rental_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("rentals:all"))

        # Get Payments related to the rental
        rental_payments = payments.objects.filter(rental=sel_rental)
        count_rental = len(rental_payments)

    context = {
        'rental': sel_rental,
        'payments': rental_payments,
        'count': count_rental,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/view_rental.html', context)


@login_required()
def search_index(request):
    # Default assignment for querysets
    landlords = None
    landlord_count = 0
    properties = None
    property_count = 0
    tenants = None
    tenant_count = 0
    query = None
    count = 0

    if request.method == 'GET':
        query = request.GET.get('q')
        if query is None:
            messages.error(request, 'Empty Search')
            return HttpResponseRedirect(reverse("my_admin:dashboard"))
        else:
            query_clean = query.replace(" ", "+")
            query = query.casefold()
            try:
                # Filter Landlords table to find results
                landlords = landlord.objects.filter(landlord_name__contains=query)
                landlord_count = len(landlords)
                # Filter Properties table to find results
                properties = managed_properties.objects.filter(property_name__contains=query)
                property_count = len(properties)
                # Filter Tenants table to find results
                tenants = tenant.objects.filter(tenant_name__contains=query)
                tenant_count = len(tenants)

                # Total Count
                count = int(landlord_count + property_count + tenant_count)
            except ObjectDoesNotExist:
                messages.error(request, 'Empty Search')
                return HttpResponseRedirect(reverse("my_admin:dashboard"))

    context = {
        'landlords': landlords,
        'landlord_count': landlord_count,
        'properties': properties,
        'property_count': property_count,
        'tenants': tenants,
        'tenant_count': tenant_count,
        'query': query,
        'count': count,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/search_index.html', context)


def search_landlord(request):
    # Default assignment for querysets
    landlords = None
    landlord_count = 0
    query = None
    count = 0

    if request.method == 'GET':
        query = request.GET.get('q')
        if query is None:
            messages.error(request, 'Empty Search')
            return HttpResponseRedirect(reverse("my_admin:dashboard"))
        else:
            query_clean = query.replace(" ", "+")
            query = query.casefold()
            try:
                # Filter Landlords table to find results
                landlords = landlord.objects.filter(landlord_name__contains=query)
                landlord_count = len(landlords)
                # Total Count
                count = int(landlord_count)
            except ObjectDoesNotExist:
                messages.error(request, 'Empty Search')
                return HttpResponseRedirect(reverse("my_admin:search"))

    context = {
        'landlords': landlords,
        'landlord_count': landlord_count,
        'query': query,
        'count': count,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/search_landlord.html', context)


def search_property(request):
    # Default assignment for querysets
    properties = None
    property_count = 0
    query = None
    count = 0

    if request.method == 'GET':
        query = request.GET.get('q')
        if query is None:
            messages.error(request, 'Empty Search')
            return HttpResponseRedirect(reverse("my_admin:dashboard"))
        else:
            query_clean = query.replace(" ", "+")
            query = query.casefold()
            try:
                # Filter Landlords table to find results
                properties = managed_properties.objects.filter(property_name__contains=query)
                property_count = len(properties)
                # Total Count
                count = int(property_count)
            except ObjectDoesNotExist:
                messages.error(request, 'Empty Search')
                return HttpResponseRedirect(reverse("my_admin:search"))

    context = {
        'properties': properties,
        'property_count': property_count,
        'query': query,
        'count': count,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/search_property.html', context)


def search_tenant(request):
    # Default assignment for querysets
    tenants = None
    tenant_count = 0
    query = None
    count = 0

    if request.method == 'GET':
        query = request.GET.get('q')
        if query is None:
            messages.error(request, 'Empty Search')
            return HttpResponseRedirect(reverse("my_admin:dashboard"))
        else:
            query_clean = query.replace(" ", "+")
            query = query.casefold()
            try:
                # Filter Landlords table to find results
                tenants = tenant.objects.filter(tenant_name__contains=query)
                tenant_count = len(tenants)
                # Total Count
                count = int(tenant_count)
            except ObjectDoesNotExist:
                messages.error(request, 'Empty Search')
                return HttpResponseRedirect(reverse("my_admin:search"))

    context = {
        'tenants': tenants,
        'tenant_count': tenant_count,
        'query': query,
        'count': count,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'core/dashboards/search_tenant.html', context)
