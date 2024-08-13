from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RestaurantViewSet,
                    MenuViewSet,
                    VoteViewSet,
                    CurrentDayMenuView,
                    CurrentDayResultsView)

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet)
router.register(r"menus", MenuViewSet)
router.register(r"votes", VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("menus/today/", CurrentDayMenuView.as_view(), name="current-day-menu"),
    path("menus/today/results/", CurrentDayResultsView.as_view(), name="current-day-results"),
]

app_name = "voting"
