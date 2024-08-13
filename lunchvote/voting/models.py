from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=255, null=True)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.restaurant.name} - {self.date} - {self.menu_name}"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote_time = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "menu", "vote_time")

    def __str__(self):
        return f"{self.user.username} voted for {self.menu.restaurant.name} on {self.vote_time}"
