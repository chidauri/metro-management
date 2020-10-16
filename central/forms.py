from django import forms

from .models import Station, Train, Ticket


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = [
            'name',
            'capacity'
        ]


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = [
            'train_no',
            'capacity',
            'source',
            'destination'
        ]

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'name',
            'age',
            'train_no',
            'had_covid_before',
        ]