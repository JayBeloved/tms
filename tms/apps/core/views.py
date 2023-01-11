import datetime
import random
import string
import pandas as pd
import numpy as np

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from django.utils.decorators import method_decorator

from .models import landlord, tenant, rentals, User, managed_properties, payments
from .forms import RentalRegForm, PaymentForm


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
    }
    return render(request, "dashboards/index.html", context)


def management_index(request):
    # Get all Rentals
    all_rentals = rentals.objects.all()
    # Create DataFrame of all Rental Agreements
    df_rentals = pd.DataFrame.from_records(all_rentals.values())

    # Convert date ending and date started to datetime datatype
    df_rentals[['date_started']] = df_rentals[['date_started']].apply(pd.to_datetime)
    df_rentals[['date_ending']] = df_rentals[['date_ending']].apply(pd.to_datetime)

    # Add a new column today that will store the value of today's date
    d_year  = int(datetime.datetime.now().strftime('%Y'))
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
    df_one_month = df_rentals[df_rentals['days_left'] <= 30]
    count_one_month = df_one_month.shape[0]

    # 3 Months or less
    df_three_months = df_rentals[df_rentals['days_left'] <= 90]
    count_three_months = df_three_months.shape[0]

    # 6 Months or  Less
    df_six_months = df_rentals[df_rentals['days_left'] <= 180]
    count_six_months = df_six_months.shape[0]

    # Greater than 6 months
    df_greater = df_rentals[df_rentals['days_left'] > 180]
    count_greater = df_greater.shape[0]

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
        'fully_paid': count_fully_paid,
        'count_greater': count_greater,
        'count_eighty': count_eighty,
        'count_fifty': count_fifty,
        'count_lower': count_lower,
    }

    return render(request, 'core/dashboards/mgt_index.html', context)


@login_required()
def one_month(request):
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
    df_one_month = df_rentals[df_rentals['days_left'] <= 30]
    count_one_month = df_one_month.shape[0]

    context = {
        'rentals': df_one_month.values,
        'count': count_one_month,
    }

    return render(request, 'core/dashboards/one_month.html', context)


@login_required()
def three_months(request):
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
    df_three_months = df_rentals[df_rentals['days_left'] <= 90]
    count_three_months = df_three_months.shape[0]

    context = {
        'rentals': df_three_months.values,
        'count': count_three_months,
    }

    return render(request, 'core/dashboards/three_months.html', context)


@login_required()
def six_months(request):
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
    df_six_months = df_rentals[df_rentals['days_left'] <= 180]
    count_six_months = df_six_months.shape[0]

    context = {
        'rentals': df_six_months.values,
        'count': count_six_months,
    }

    return render(request, 'core/dashboards/six_months.html', context)


@login_required()
def greater_than_six_month(request):
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
    df_greater = df_rentals[df_rentals['days_left'] > 180]
    count_greater = df_greater.shape[0]

    context = {
        'rentals': df_greater.values,
        'count': count_greater,
    }

    return render(request, 'core/dashboards/greater_than_six_months.html', context)


@login_required()
def fully_paid(request):
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
    df_fully_paid = df_rentals[df_rentals['balance'] <= 0]
    count_fully_paid = df_fully_paid.shape[0]

    context = {
        'rentals': df_fully_paid.values,
        'count': count_fully_paid,
    }

    return render(request, 'core/dashboards/fully_paid.html', context)


@login_required()
def eighty_percent(request):
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
    df_eighty = df_rentals[df_rentals['percentage_paid'] >= 80]
    count_eighty = df_eighty.shape[0]

    context = {
        'rentals': df_eighty.values,
        'count': count_eighty,
    }

    return render(request, 'core/dashboards/eighty_percent.html', context)


@login_required()
def fifty_percent(request):
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
    df_fifty = df_rentals[df_rentals['percentage_paid'] >= 50]
    count_fifty = df_fifty.shape[0]

    context = {
        'rentals': df_fifty.values,
        'count': count_fifty,
    }

    return render(request, 'core/dashboards/fifty_percent.html', context)


@login_required()
def less_than_fifty_percent(request):
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
    df_lower = df_rentals[df_rentals['percentage_paid'] < 50]
    count_lower = df_lower.shape[0]

    context = {
        'rentals': df_lower.values,
        'count': count_lower,
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
            remarks = "Fresh Tenancy"
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
    }

    return render(request, 'core/dashboards/rental_register.html', context)


class RentalsListView(ListView):
    model = rentals
    template_name = "core/dashboards/rentals_list.html"
    context_object_name = "rentals"
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
    }

    return render(request, 'core/dashboards/record_payment.html', context)


class PaymentsListView(ListView):
    model = payments
    template_name = "core/dashboards/payments_list.html"
    context_object_name = "payments"
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
    }

    return render(request, 'core/dashboards/view_rental.html', context)
