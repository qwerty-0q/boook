from .models import (Country, City, Services, Hotel, Room)
from modeltranslation.translator import TranslationOptions,register

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Services)
class ServicesTranslationOptions(TranslationOptions):
    fields = ('service_name',)


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'street', 'description')


@register(Room)
class ProductTranslationOptions(TranslationOptions):
    fields = ('room_type', 'room_status', 'description')