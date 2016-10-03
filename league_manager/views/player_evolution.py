__author__ = 'Bertrand'
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from league_manager.views.serializers.player_evolution_serializer import EvolutionSerializer,CreateEvolutionSerializer
from league_manager.models.player_evolution import PlayerEvolution
from league_manager.models.team import Team
from django.http import HttpResponseForbidden

class AddBaseEvolutionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateEvolutionSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(AddBaseEvolutionView, self).get_serializer(*args, **kwargs)

    # need to test if the team is able to receive evolutions
    def post(self, request, *args, **kwargs):

        # pour chaque donnée dans le tableau, on vérifie que l'équipe cible est bien dans l'état 0,
        team = Team.objects.get(players=request.data[0]['player'])
        if team.status != 0:
            return HttpResponseForbidden

        # si c'est le cas on fait le job
        response = self.create(request, *args, **kwargs)

        # et on change les états de la team afin de la finaliser
        team.status = 1;
        team.save()

        return response

class PlayerEvolutionListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EvolutionSerializer
    queryset = PlayerEvolution.objects.all()