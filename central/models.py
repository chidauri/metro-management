from django.db import models

class Station(models.Model):
    name           = models.CharField(max_length=120, unique=True, blank=False)
    count          = models.IntegerField(default=0)
    capacity       = models.IntegerField(blank=False)
    lastsanitized  = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    train_no              = models.IntegerField(unique=True, blank=False)
    capacity              = models.IntegerField(blank=False)
    passengers            = models.IntegerField(default=0)
    safe_passengers       = models.IntegerField(default=0)
    senior_passengers     = models.IntegerField(default=0)
    lastsanitized         = models.TimeField(null=True, blank=True)
    source                = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='train_source')
    destination           = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='train_destination')

    def initialize_coaches(self, *args, **kwargs):
        for num in range(5):
            self.coaches.create(coach_no=num, senior_coach= (num==0))

    def __str__(self):
        return str(self.train_no)

class Coach(models.Model):
    coach_no           = models.IntegerField()
    senior_coach       = models.BooleanField(default=False)
    passengers         = models.IntegerField(default=0)
    safe_passengers    = models.IntegerField(default=0)
    train_no           = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='coaches')

    def __str__(self):
        return str(self.coach_no)

class Ticket(models.Model):
    name             = models.CharField(max_length=120, blank=False)
    age              = models.IntegerField(blank=False)
    train_no         = models.ForeignKey(Train, on_delete=models.CASCADE)
    had_covid_before = models.BooleanField(blank=False)