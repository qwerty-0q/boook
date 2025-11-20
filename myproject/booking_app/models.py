from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    country_image = models.ImageField(upload_to='country_images/')
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.country_image}, {self.country_name}'


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(80)],
                                           null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    RoleChoices = (
    ('client', 'client'),
    ('owner', 'owner'))
    status = models.CharField(max_length=32, choices=RoleChoices, default='client')
    user_image = models.ImageField(upload_to='user_photo/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city_image = models.ImageField(upload_to='city_photo/')
    city_name = models.CharField(max_length=32)

    def __str__(self):
        return self.city_name


class Services(models.Model):
    service_image = models.ImageField(upload_to='service_image/')
    service_name = models.CharField(max_length=64)

    def __str__(self):
        return self.service_name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities')
    street = models.CharField(max_length=100)
    postal_code = models.PositiveSmallIntegerField()
    hotel_stars = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1,6)])
    description = models.TextField()
    hotel_services = models.ManyToManyField(Services)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.hotel_name


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f'{self.hotel}, {self.hotel_image}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_rooms')
    room_number = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()
    RoomTypeChoices = (
    ('Люкс', 'Люкс'),
    ('Полулюкс', 'Полулюкс'),
    ('Семейный', 'Семейный'),
    ('Эконом', 'Эконом'),
    ('Одноместный', 'Одноместный'))
    room_type = models.CharField(max_length=32, choices=RoomTypeChoices)
    RoomStatusChoices = (
    ('Занят', 'Занят'),
    ('Забронирован', 'Забронирован'),
    ('Свабоден', 'Свабоден'))
    room_status = models.CharField(max_length=32, choices=RoomStatusChoices)
    description = models.TextField()

    def __str__(self):
        return f'{self.hotel}, {self.room_number}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_photos')
    room_image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f'{self.room}, {self.room_image}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1,11)])
    comment = models.TextField()
    created_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.hotel}'


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.hotel}, {self.room}'