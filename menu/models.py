from django.db import models


class Menu(models.Model):
    """Модель меню"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель пункта меню"""
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        blank=True,
        related_name='items',
    )
    url = models.CharField(max_length=200, blank=True, verbose_name="URL")


    def __str__(self):
        return self.name

