from django.db import models

# Create your models here
class User_Details(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    points = models.IntegerField(default=0)    

    def __str__(self):
        return self.name

class User_History(models.Model):
    email = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    date = models.DateField()
    food_emsn = models.IntegerField()
    travel_emsn= models.IntegerField()
    energy_emission = models.IntegerField()
    water_emission = models.IntegerField()
    waste_emission = models.IntegerField()
    appliance_emission = models.IntegerField()
    daily_emsn = models.IntegerField()

    def str (self):
        return self.email
    
class User_Goal(models.Model):
    email = models.ForeignKey(User_Details, on_delete=models.CASCADE)

    gl_travel_emsn = models.IntegerField(null=True)
    gl_energy_emsn = models.IntegerField(null=True)
    gl_food_emsn = models.IntegerField(null=True)
    gl_water_emsn = models.IntegerField(null=True)
    gl_waste_emsn = models.IntegerField(null=True)
    gl_appliance_emsn = models.IntegerField(null=True)
    gl_daily_emsn = models.IntegerField(null=True)

    def str (self):
        return self.email
