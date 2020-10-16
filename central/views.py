from django.shortcuts import render

from .models import Station, Train, Ticket, Coach
from .forms import StationForm, TrainForm, TicketForm


def home_view(request):
    return render(request, "home.html", {})

def add_station_view(request):
    form = StationForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = StationForm()

    context = {
        'form': form
    }

    return render(request, "add_station.html", context)

def add_train_view(request):
    form = TrainForm(request.POST or None)
    if form.is_valid():
        form.save()
        train = Train.objects.get(train_no__exact=form.cleaned_data['train_no'])
        train.initialize_coaches()
        form = TrainForm()

    context = {
        'form': form
    }

    return render(request, "add_train.html", context)


def book_ticket_view(request, id):
    train = Train.objects.get(train_no__exact=id)
    initial_data = {
        'train_no': train
    }
    form = TicketForm(initial=initial_data)

    context = {
        'form': form
    }

    return render(request, "ticket.html", context)


def post_booking_view(request, id):
    train = Train.objects.get(train_no__exact=id)
    context = {}

    form = TicketForm(request.POST or None)
    if form.is_valid():
        form.save()
        rel_train = form.cleaned_data['train_no']
        rel_train.passengers += 1
        if form.cleaned_data['had_covid_before']:
            rel_train.safe_passengers += 1
        if form.cleaned_data['age'] > 60:
            rel_train.senior_passengers += 1
        rel_train.save()
        
        rel_station = Station.objects.get(name__exact=rel_train.source)
        rel_station.count += 1
        rel_station.save()

        coach = assign_coach(rel_train, form.cleaned_data['age'], form.cleaned_data['had_covid_before'])
        context = {
            'coach': coach
        }

    return render(request, "postbooking.html", context)


def assign_coach(train, age, had_covid_before):
    coaches = train.coaches.all()
    if age > 60:
        target_coach = coaches[0]                 # coach[0] = senior coach
        target_coach.passengers += 1
        target_coach.save()  
        return target_coach
    else:
        coaches = coaches[1:]                     # don't use senior coach for young passengers

        if had_covid_before:
            lookup = {}
            for coach in coaches:
                lookup[coach] = coach.safe_passengers/coach.passengers if coach.passengers != 0 else 0

            # sort according to percentage of safe_passengers
            lookup = {k: v for k, v in sorted(lookup.items(), key=lambda item: item[1])}
            target_coach = list(lookup.keys())[0]
            target_coach.passengers += 1
            target_coach.safe_passengers += 1
            target_coach.save()
            return target_coach
        else:
            lookup = {}
            for coach in coaches:
                lookup[coach] = coach.passengers

            # sort according to number of passengers
            lookup = {k: v for k, v in sorted(lookup.items(), key=lambda item: item[1])}
            target_coach = list(lookup.keys())[0]
            target_coach.passengers += 1
            target_coach.save()
            return target_coach


def manager_view(request):
    queryset_stn   = Station.objects.all()
    queryset_train = Train.objects.all()

    context = {
        'station_list': queryset_stn,
        'train_list': queryset_train
    }

    return render(request, "managing.html", context)


def passenger_view(request):
    source = request.GET['source'] if 'source' in request.GET else ''
    destination = request.GET['destination'] if 'destination' in request.GET else ''

    context = {}
    if source:
        try:
            station = Station.objects.get(name__exact=source)
        except:
            context = {}
        else:
            relevant_trains = []
            for train in Train.objects.all():
                if str(train.source) == source and (destination == '' or str(train.destination) == destination):
                    relevant_trains.append(train)

            context = {
                'train_list': relevant_trains,
                'station': station,
            }

    return render(request, "booking.html", context)
