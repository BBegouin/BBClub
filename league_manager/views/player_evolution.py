__author__ = 'Bertrand'
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from league_manager.views.serializers.player_evolution_serializer import CreatePlayerSerializer
from league_manager.models.player_evolution import PlayerEvolution

class PlayerEvolutionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreatePlayerSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(PlayerEvolutionView, self).get_serializer(*args, **kwargs)

class PlayerEvolutionListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreatePlayerSerializer
    queryset = PlayerEvolution.objects.all()