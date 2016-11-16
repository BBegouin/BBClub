__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView
from league_manager.models.player import Player
from rest_framework.response import Response
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.ref_skills import Ref_Skills
from league_manager.models.team import Team
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.team_serializers import TeamDetailSerializer
from django.core.exceptions import ObjectDoesNotExist

class PlayerBaseUpgradeBulkPublishView(CreateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = TeamDetailSerializer

    """
     Permet de publier plusieurs upgrade de joueurs
    """
    def post(self, request, *args, **kwargs):

        user = request.user

        # vérification des datas
        self.check_datas(request.data, user)

        # si on a passé la vérification, toutes les données sont OK, on peut lancer la création et la publication
        for up_data in request.data:

            # on crée un upgrade qui reste à faire, et de type upgrade de base
            up = PlayerUpgrade( player=Player.objects.get(pk=up_data['player_id']),
                                status=0,
                                type=0, )

            up.publish(up_data)
            up.save()

        #on choppe la team à laquelle appartient le premier
        team = Team.objects.get(players__id = request.data[0]['player_id'])
        serializer = TeamDetailSerializer(team)

        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")

    """
     On vérifie que les données contiennent les données utiles et que les règles
     des upgrades de base sont respectées.
     les upgrades de base doivent valider les règles de la ligue, aujourd'hui en dur :
     - 3 skill max par équipe,
     - au max une seule double par équipe,
     - une seule upgrade de base par joueur.
     - les augmentations de stats sont interdites
    """
    def check_datas(self,base_upgrade_datas,user):

        base_upgrade_team_cpt = {}
        double_upgrade_team_cpt = {}
        player_upgrade_cpt = {}
        #un utilisateur inconnu ne peut pas publier d'upgrade
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas publier d'upgrade de joueur")

        #on va d'abord vérifier que tous les joueurs cible existent, et que les données dont ok dans la requête
        for up_data in base_upgrade_datas:

            #on vérifie que les datas sont bien formattées
            if  'player_id' not in up_data or\
                'value' not in up_data or\
                'skill' not in up_data:
                    raise NotAcceptable("Données incomplètes")

            #on choppe l'objet player associé à l'upgrade, pour vérifier qu'il existe
            try:
                pl = Player.objects.get(pk=up_data['player_id'])
            except ObjectDoesNotExist:
                # si l'utilisateur n'existe pas, on sort
                raise NotAcceptable("Le joueur cible de l'upgrade de base est inconnu.")

            # si le joueur n'est pas admin
            if  user.is_superuser is False and pl.team.user != user:
                # on vérifie que l'upgrade porte sur un joueurs appartenant à l'utilisateur connecté
                raise NotAcceptable("Il est interdit de publier une upgrade sur les joueurs d'un autre coach.")

            # si le joueur à déjà une upgrade de base, on sort
            if PlayerUpgrade.objects.filter(player = up_data['player_id'],type=0).count():
                raise NotAcceptable("Le joueur cible de l'upgrade de base a déjà une upgrade de base")

            baseupgrade_cpt = PlayerUpgrade.objects.filter(player__team = pl.team,type =0).count()
            # on choppe toutes les upgrade de base qui sont liés à des joueurs de la même équipe que celui qui est ciblé
            if baseupgrade_cpt == 3:
                raise NotAcceptable("L'équipe ne peut pas accueillir plus de 3 upgrade de base")

            #on stocke les upgrade pour faire les vérifs au sein du tableau
            if pl.team.id not in base_upgrade_team_cpt:
                base_upgrade_team_cpt[pl.team.id] = 1
            else:
                base_upgrade_team_cpt[pl.team.id] += 1

            if base_upgrade_team_cpt[pl.team.id] > 3:
                raise NotAcceptable("L'équipe ne peut pas accueillir plus de 3 upgrade de base")

            if pl.id not in player_upgrade_cpt:
                player_upgrade_cpt[pl.id] = 1
            else:
                player_upgrade_cpt[pl.id] += 1


            if player_upgrade_cpt[pl.id] > 1:
                raise NotAcceptable("Il est interdit de faire deux upgrade de base sur le même joueur")


            # il faut aussi savoir combien d'upgrade dans le tableau visent cette équipe,
            # afin de ne pas authoriser trop d'upgrade

            # on vérifie qu'elle n'a pas déjà une double enregistrée sur un de ses joueurs
            if up_data['value'] == 1:
                double_upgrade_cpt = PlayerUpgrade.objects.filter(player__team = pl.team,type =0,value=1).count()
                if double_upgrade_cpt == 1:
                    raise NotAcceptable("L'équipe ne peut pas accueillir plus de 1 compétence double")

                if pl.team.id not in double_upgrade_team_cpt:
                    double_upgrade_team_cpt[pl.team.id] = 1
                else:
                    double_upgrade_team_cpt[pl.team.id] += 1

                if double_upgrade_team_cpt[pl.team.id] > 1:
                    raise NotAcceptable("L'équipe ne peut pas accueillir plus de 1 compétence double")

            # on vérifie que l'augmentation n'est pas une upgrade de stat
            if up_data['value'] > 1:
                raise NotAcceptable("Les augmentations de stats sont interdites sur les upgrades de base")


