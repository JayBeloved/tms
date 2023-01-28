import datetime
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

########################

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from ..core.views import alert
from .models import User, USERTYPE_CHOICES


# Create your views here.


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 1:
                    return redirect("my_admin:dashboard")
                elif user.user_type == 2:
                    messages.success(request, 'Agent SUCCESSFUL LOGIN')
                    # return redirect("agents:dashboard")
                    return redirect("my_admin:dashboard")
                else:
                    msg = 'Something Went Wrong'
                    HttpResponseRedirect('landing')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/pages/login.html", {"form": form, "msg": msg})


def login_redirect(request):
    return HttpResponseRedirect('login')


@login_required()
def register_agent(request):

    form = AgentRegisterForm(request.POST or None)
    if request.method == 'POST':
        # Check if the submitted form is valid
        if form.is_valid():
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            p_word1 = form.cleaned_data.get("password1")
            p_word2 = form.cleaned_data.get("password2")

            #############################
            # Function to generate automatic username
            def gen_usn(fname, lname):
                gen = f"{lname[:4]}{fname[:3]}"
                user_name = gen.lower()

                while User.objects.filter(username=user_name):
                    similar_list = User.objects.filter(username__icontains=user_name).__len__()
                    inc_count = int(similar_list) + 1
                    user_name = f"{user_name}0{inc_count}"

                    if not User.objects.filter(username=user_name):
                        user_name = user_name

                return user_name
            #########################

            #  Check Username or Generate
            if form.cleaned_data.get("username"):
                username = form.cleaned_data.get("username")
            else:
                username = gen_usn(first_name, last_name)
            reg_date = timezone.now()
            is_staff = True
            user_type = 2

            # Check email and password
            if User.objects.filter(email=email):
                messages.error(request, f'Email already in use by another Agent. Use a unique email address')
            else:
                if p_word1 == p_word2:
                    password = make_password(p_word1)

                    #######################
                    # Check for duplicate username entry
                    def check_username(uname):
                        user_name = uname
                        while User.objects.filter(username=user_name):
                            similar_list = User.objects.filter(username__icontains=user_name).__len__()
                            inc_count = int(similar_list) + 1
                            user_name = f"{uname}0{inc_count}"

                            if not User.objects.filter(username=user_name):
                                user_name = user_name

                        return user_name
                    #####################

                    ver_username = check_username(username)

                    usr = User.objects.create(user_type=user_type, first_name=first_name.capitalize(),
                                              last_name=last_name.capitalize(), email=email.casefold(), password=password,
                                              username=ver_username, is_staff=is_staff, date_joined=reg_date)
                    usr.save()

                    messages.success(request, f'Agent Registered Successfully')
                else:
                    form = form
                    messages.error(request, 'The Passwords did not match')

        else:
            messages.error(request, 'Something Went Wrong, Check your entries and try again.')

        return HttpResponseRedirect(reverse("agents:registration"))

    context = {
        'form': form,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }

    return render(request, 'accounts/dashboards/agent_register.html', context)


class AgentsListView(ListView):
    model = User
    queryset = User.objects.filter(user_type=2)
    template_name = "accounts/dashboards/agents_list.html"
    context_object_name = "agents"
    extra_context = {
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }
    ordering = ['id']
    paginate_by = 5


@login_required()
def my_profile(request):
    get_usertype = request.user.user_type
    usertype = 'Error'
    for t in USERTYPE_CHOICES:
        if t[0] == get_usertype:
            usertype = t[1]

    info_form = ProfileInfoForm(instance=request.user)
    return render(request, 'accounts/dashboards/profile.html', {'form': info_form, 'usertype': usertype,
                                                                'alertCount': alert()[1], 'alerts': alert()[0],
                                                                'range': alert()[2]})


@login_required()
def profile_info(request):
    if request.method == 'POST':
        u_form = ProfileInfoUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile:profile_info')
        else:
            messages.error(request, 'Something Went Wrong, Unable to update profile')
    else:
        u_form = ProfileInfoUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_details.html', {'form': u_form, 'alertCount': alert()[1],
                                                             'alerts': alert()[0], 'range': alert()[2]})


@login_required()
def agent_info(request, agent_id):
    if agent_id is None:
        messages.error(request, 'No Agent Selected')
        return HttpResponseRedirect(reverse("agents:all"))
    else:
        try:
            sel_agent = User.objects.get(id=agent_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Something Went Wrong')
            return HttpResponseRedirect(reverse("agents:all"))

    info_form = ProfileInfoForm(instance=sel_agent)

    context = {
        'form': info_form,
        'agent': sel_agent,
        'alertCount': alert()[1],
        'alerts': alert()[0],
        'range': alert()[2],
    }
    return render(request, 'accounts/dashboards/agent_info.html', context)

