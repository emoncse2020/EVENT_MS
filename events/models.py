from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
   
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(Participant, blank=True, related_name='events')

    def __str__(self):
        return self.name