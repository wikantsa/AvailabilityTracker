from .models import Activity, Availability, Profile
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from .forms import AvailabilityForm, UserForm, LoginForm, ActivityForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
import datetime
import calendar


@login_required
def index(request):
    # get Sunday
    today = datetime.date.today()
    days_past = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(days=days_past)

    # construct week data
    week_data = []
    for i in range(0, 7):
        day_data = []
        day_data.append((sun + datetime.timedelta(days=i)).strftime("%A"))
        day_data.append(calendar.month_name[int((sun + datetime.timedelta(days=i)).strftime("%m"))])
        day_data.append((sun + datetime.timedelta(days=i)).strftime("%d"))
        week_data.append(day_data)

    # get availabilities
    start_datetime = datetime.datetime.combine(sun, datetime.datetime.min.time())
    end_datetime = datetime.datetime.combine(sun + datetime.timedelta(days=6), datetime.datetime.max.time())
    availabilities = Availability.objects.filter(start__range=[start_datetime, end_datetime], person__user__username=request.user.username)
    availabilities_by_day = []
    for i in range(0, 7):
        availabilities_by_day.append(availabilities.filter(start__day=sun.day + i))

    # get ratios
    ratios_by_day = []
    for i in range(0, 7):
        ratios = []
        for availability in availabilities_by_day[i]:
            ratio = 100*((availability.start.hour * 60 + availability.start.minute)/1440)
            ratios.append(ratio)
        ratios_by_day.append(ratios)

    # get lengths
    lengths_by_day = []
    for i in range(0, 7):
        lengths = []
        for availability in availabilities_by_day[i]:
            length = 100 * (((availability.end.hour * 60 + availability.end.minute) / 1440) - ((availability.start.hour * 60 + availability.start.minute) / 1440))
            lengths.append(length)
        lengths_by_day.append(lengths)

    # zip the availabilities, ratios and lengths into tuples
    final_availabilities = []
    for i in range(0, 7):
        availabilities = availabilities_by_day[i]
        ratios = ratios_by_day[i]
        lengths = lengths_by_day[i]
        final_availabilities.append(zip(availabilities, ratios, lengths))

    return render(request, 'index.html', {'week_data': week_data, 'periods': final_availabilities})


class AvailabilityCreate(CreateView):
    template_name = 'availability_form.html'
    model = Availability
    form_class = AvailabilityForm

    def form_valid(self, form):
        availability = form.save(commit=False)
        availability.person = Profile.objects.get(user=self.request.user)
        availability.save()
        return super(AvailabilityCreate, self).form_valid(form)

    def form_invalid(self, form):
        print('INVALID')
        return super(AvailabilityCreate, self).form_invalid(form)


class ActivityCreate(CreateView):
    template_name = 'activity_form.html'
    model = Activity
    form_class = ActivityForm

    def form_valid(self, form):
        print('VALID')
        return super(ActivityCreate, self).form_valid(form)

    def form_invalid(self, form):
        print('INVALID')
        return super(ActivityCreate, self).form_invalid(form)


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    template_name = 'login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            print(form.cleaned_data['username'])
            print(form.cleaned_data['password'])
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if self.request.GET.get('next') is not None:
                    return redirect(self.request.GET.get('next'))
                else:
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


@login_required
def schedule(request):
    return render(request, 'schedule.html')


@login_required
def matches(request):
    return render(request, 'matches.html')
