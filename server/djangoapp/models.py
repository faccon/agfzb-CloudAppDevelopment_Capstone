from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    Name = models.CharField(max_length=10)
    Description = models.CharField(max_length=30)

    def __str__(self):
        return self.Name + " " + self.Description

# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model): 

    Sedan = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'

    CAR_CHOICES = [
        (Sedan, 'Sedan'),
        (SUV,'SUV'),
        (WAGON, 'WAGON'),
    ]

# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
# - Name
    Name = models.CharField(max_length=20)
# - Dealer id, used to refer a dealer created in cloudant database
    DearlerId = models.IntegerField()
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    Type = models.CharField(max_length=10, choices=CAR_CHOICES)
# - Year (DateField)
    Year = models.DateField()
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
    def __str__(self):
        return self.Name + " " + self.DearlerId + " " + self.Type+ " " + self.Year



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
