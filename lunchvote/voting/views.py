from datetime import date
from django.db.models import Count
from rest_framework import mixins, viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import RestaurantSerializer, MenuSerializer, VoteSerializer
from .models import Restaurant, Menu, Vote


class RestaurantViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [IsAuthenticated]


class MenuViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        menu = self.get_object()

        # Check if the user has already voted today
        if Vote.objects.filter(user=request.user, menu=menu, vote_time__date=date.today()).exists():
            return Response({"error": "You have already voted today."}, status=status.HTTP_400_BAD_REQUEST)

        # Attempt to create the vote
        vote = Vote.objects.create(user=request.user, menu=menu)
        return Response({"status": "Vote cast successfully"}, status=status.HTTP_201_CREATED)


class CurrentDayMenuView(mixins.ListModelMixin,
                         generics.GenericAPIView):
    serializer_class = MenuSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.filter(date=date.today())

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class CurrentDayResultsView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        today = date.today()
        results = Vote.objects.filter(menu__date=today).\
            values("menu__restaurant__name").\
            annotate(vote_count=Count("id")).order_by("-vote_count")
        return Response(results)


class VersionedAPIView(APIView):
    def get(self, request, *args, **kwargs):
        version = request.headers.get('build-version')
        if version == '1.0':
            # Return response for version 1.0
            return Response({"message": "Version 1.0 response"})
        elif version == '2.0':
            # Return response for version 2.0
            return Response({"message": "Version 2.0 response"})
        else:
            return Response({"error": "Unsupported version"}, status=400)
