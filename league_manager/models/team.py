__author__ = 'Bertrand'
from django.db import models
from django.db.models import FileField
from django.contrib.auth.models import User
from mezzanine.utils.models import AdminThumbMixin, upload_to
from league_manager.models.league import League
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.player import Player
from django.db.models import Sum,Count

class Team(models.Model):
    name = models.CharField(max_length=50)
    ref_roster = models.ForeignKey("ref_roster",related_name="roster")
    league = models.ForeignKey("league")
    treasury = models.PositiveSmallIntegerField()
    nb_rerolls = models.PositiveSmallIntegerField()
    pop = models.PositiveSmallIntegerField()
    assistants = models.PositiveSmallIntegerField()
    cheerleaders = models.PositiveSmallIntegerField()
    apo = models.BooleanField()
    user = models.ForeignKey(User, verbose_name="Coach")
    icon_file_path = models.CharField(max_length=500,blank=True,null=True)
    DungeonBowl = models.BooleanField()
    # status value :
    # 0 : draft - base skills needs to be chosen
    # 1 : published : ready to play
    # 2 : level up : need to affect levels up
    # 3 : after match : need to buy some players or retire some others
    status = models.PositiveSmallIntegerField(blank=False,null=False)


    """
    Vérifie que la team est compatible des règles de la ligue auquelle elle est inscrite
    """
    def get_team_price(self):
        budget = self.ref_roster.reroll_price * self.nb_rerolls
        budget += self.get_base_player_price()

        if self.apo is True:
            budget+=50

        budget += self.pop *10
        budget += self.cheerleaders *10
        budget += self.assistants *10
        return budget

    """
    Vérifie que la team est compatible des règles de la ligue auquelle elle est inscrite
    """
    def check_team_price(self):
        # on récupère la ligue dans laquelle est crée l'équipe
        max_budget = self.league.starting_rules.max_budget
        budget = self.get_team_price()

        return max_budget > budget

    """
    retourne le prix des joueurs de base
    """
    def get_base_player_price(self):
        cost = Ref_Roster_Line.objects.filter(players__team__pk=self.id).aggregate(player_cost=Sum('cost'))
        return cost["player_cost"]

    """
    Permet de vérifier que l'équipe est dans un état compatible d'une mise à jour
    """
    def isUpdateAllowed(self):
        if self.status == 0 or self.status == 3:
            return True

        return False

    #
    # Automate permettant le changement de status de l'équipe
    # status value :
    # 0 : draft - base skills needs to be chosen
    # 1 : published : ready to play
    # 2 : level up : need to affect levels up
    # 3 : after match : need to buy some players or retire some others
    #
    def updateStatus(self):
        # si l'équipe est en créations alors son status est 0
        # si le status est 0, alors sont nouveau status est 1
        if self.status == 0:
            self.status = 1;

        # les statuts 2 et 3 ne sont pas accessible par une mise à jour de l'équipe,
        # seule la création d'un rapport permet de modifier le statut de l'équipe

        # si le status est 3, alors la mise à jour de l'équipe est finie, on repasse en état standard
        elif self.status == 3 :
            self.status = 1









