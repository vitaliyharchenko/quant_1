from django.db import models

from organizations.models import Company


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'

    def __str__(self):
        return u'{}'.format(self.name)


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    country = models.ForeignKey(Country, verbose_name=u"Страна")

    class Meta:
        verbose_name = 'область'
        verbose_name_plural = 'области'
        unique_together = ('name', 'country')

    def __str__(self):
        return u'{}'.format(self.name)


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название города', unique=True)
    region = models.ForeignKey(Region)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
        unique_together = ('name', 'region')

    def __str__(self):
        return self.name


class Place(models.Model):
    city = models.ForeignKey(City)
    longitude = models.FloatField(verbose_name='Долгота', help_text='Возьмите из Яндекс карт')
    latitude = models.FloatField(verbose_name='Широта', help_text='Возьмите из Яндекс карт')
    fulladdress = models.CharField(max_length=500, verbose_name='Адрес', unique=True, help_text='В формате "ул. Московская, д.9"')

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return u'{}, {}'.format(self.city, self.fulladdress)


class Office(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    place = models.ForeignKey(Place, verbose_name='Место')
    company = models.ForeignKey(Company, verbose_name=u"Компания")

    class Meta:
        verbose_name = 'офис'
        verbose_name_plural = 'офисы'

    def __str__(self):
        return u'{}, {}'.format(self.title, self.place)


class СlassRoom(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    office = models.ForeignKey(Office, verbose_name=u'Офис')

    class Meta:
        verbose_name = 'офис'
        verbose_name_plural = 'офисы'

    def __str__(self):
        return u'{}, {}'.format(self.title, self.office)
