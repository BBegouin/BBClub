__author__ = 'Bertrand'
from django.db import models
from django.contrib.auth.models import User
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.player import Player
from league_manager.models.ref_skills import Ref_Skills
from django.db.models import Sum
from django.db.models import Max
from django.db.models import Q
from functools import reduce
from rest_framework.exceptions import NotAcceptable

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
    status = models.PositiveSmallIntegerField(blank=False,null=False)
    TV = models.PositiveIntegerField(blank=False,null=False,default=0)
    ranking_points = models.PositiveIntegerField(blank=False,null=False,default=0)
    bonus_point = models.PositiveIntegerField(blank=False,null=False,default=0)


    """
     Renvoi le prix de l'équipe de base, hors Xp.
     Utile uniquement à la création
    """
    def get_team_stuff_cost(self):
        budget = self.ref_roster.reroll_price * self.nb_rerolls

        if self.apo is True:
            budget+=50

        budget += self.pop *10
        budget += self.cheerleaders *10
        budget += self.assistants *10
        return budget


    """
     Vérifie que la team est compatible des règles de la ligue auquelle elle est inscrite
    """
    def check_team_cost(self):
        # on récupère la ligue dans laquelle est crée l'équipe
        max_budget = self.league.starting_rules.max_budget
        budget = self.get_team_stuff_cost()
        budget += self.get_player_cost()


        return max_budget > budget

    """
     Vérifie que l'ensemble des joueurs de cette équipe sont bien dans le roster de référence,
     pour éviter la triche
    """
    def check_players(self):
        players = Player.objects.filter(team=self)
        for player in players:
            if player.ref_roster_line.roster != self.ref_roster:
                return False

        return True


    """
     Retourne le prix des joueurs, qui participent au prochain match
    """
    def get_player_cost(self):
        cost = Ref_Roster_Line.objects.filter(players__team = self,players__miss_next_game = False).aggregate(player_cost=Sum('cost'))
        return cost["player_cost"]

    """
     Permet de vérifier que l'équipe est dans un état compatible d'une mise à jour
    """
    def isUpdateAllowed(self):
        if self.status == 0:
            return True

        return False


    """
     permet de calculer les point de classements de l'équipe
    """
    def update_ranking_point(self):
        nb_win = TeamReport.objects.filter(team=self,result=0).count()
        nb_draw = TeamReport.objects.filter(team=self,result=1).count()
        nb_lose = TeamReport.objects.filter(team=self,result=2).count()
        ranking_point = nb_win * 4 + nb_draw * 2 + nb_lose
        self.ranking_points = ranking_point
        self.save()

    """
     permet de calculer les points de bonus :
        bonus = Nb TD + Nb Sorties
    """
    def update_bonus_point(self):
        res = PlayerReport.objects.filter(team_report__team=self).aggregate(td=Sum('nb_td'),sor=Sum('nb_cas'))

        if res['td'] is None:
            res['td'] = 0
        if res['sor'] is None:
            res['sor'] = 0

        bonus_point = res['td'] + res['sor']
        self.bonus_point = bonus_point
        self.save()

    """
     On calcule le TV d'une équipe en additionnant :
     - le prix de tous les joueurs de base présents pour le prochain match, y compris les journaliers
     ( les joueurs absent ne sont pas comptés )
     - le prix des upgrades
     - le prix des trucs d'équipes (les apo, la pop, les relances et toutes ces conneries )
    """
    def update_TV(self):
        player_cost = self.get_player_cost()
        upgrade_cost = PlayerUpgrade.objects.filter(player__team = self).aggregate(upgrade_cost=Sum('cost'))
        team_stuff_cost = self.get_team_stuff_cost()
        TV = player_cost + team_stuff_cost
        if upgrade_cost['upgrade_cost'] is not None:
            TV += upgrade_cost['upgrade_cost']
        self.TV = TV
        self.save()

    """
     On ajoute ou on supprime des journaliers en fonction du nombre de joueurs valides
     pour le prochain match
     Si il faut supprimer des journeymens, on supprime ceux dont le total de Xp est le moins élevé
     en premier
    """
    def update_Journeymen(self):

        # on compte le nombre de joueurs réguliers valides qui jouent le prochain match
        regular_valid_players_cpt = Player.objects.filter(team=self,miss_next_game=False,is_journeyman=False).count()

        # on compte de le nombre réel de journeymens actuellement dans l'équipe
        journeymens_cpt = Player.objects.filter(team=self,is_journeyman=True).count()

        #si on a au moins 11 joueurs de base dans l'équipe, et qu'on n'a pas de journaliers tout va bien, on sort.
        if regular_valid_players_cpt >= 11 and journeymens_cpt == 0:
            return

        # on compte le nombre théorique de journeymens
        theorical_journeymens = max(regular_valid_players_cpt,11) - (regular_valid_players_cpt + journeymens_cpt)

        # si on a 11 joueurs, avec les journaliers, impeccable, on sort, car on a juste le compte
        if theorical_journeymens == 0:
            return

        # si on arrive là, c'est qu'on a trop ou pas assez de journeymens.

        # si on a besoin de journeymens, on en crée autant que nécessaire
        if theorical_journeymens > 0:

            # on choppe le numero du dernier joueur, pour affecter le numéro de joueur automatiquement
            ag = Player.objects.filter(team=self).aggregate(Max('num'))
            current_max_num = ag['num__max']
            for i in  range(0,theorical_journeymens):
                current_max_num += 1
                jm = Player(team=self,
                            name="journalier_%i"%current_max_num,
                            ref_roster_line=self.ref_roster.journeyman,
                            num = current_max_num,
                            is_journeyman = True
                            )
                s = Ref_Skills.objects.get(name="Solitaire")
                jm.init_datas()
                jm.skills.add(s)
                jm.save()

        # si on a trop de journeymens, on en supprime
        elif theorical_journeymens < 0:

            # si on supprime des journeysmens, on ordonne la requête par nombre de xp croissant afin de supprimer
            # en premier ceux qui sont les moins capés
            journeymens = Player.objects.filter(team=self,is_journeyman=True).order_by('total_xp')

            delete_cpt = 0
            for jm in  journeymens:
                jm.delete()
                delete_cpt -=1
                if delete_cpt == theorical_journeymens:
                    break

    """
     permet de vérifier si les achats sont valides :
      - si ils respectent la trésorerie
      - si les joueurs sont dans le roster
      - si il n'y a pas plus de 16 joueurs après achats
    """
    def check_purchases(self, purchases):

        #on vérifie que les journaliers appartiennent bien à l'équipe
        if 'journeymens' in purchases:
            self.check_journeymens(purchases)

        # On vérifie que les achats sont compatibles de la trésorerie
        cost = self.check_purchases_price(purchases)

        # On vérifie que les joueurs que l'on veut acheter sont compatibles de cette équipe
        if 'players' in purchases:
            self.check_player_compatibility(purchases)
            #on vérifie que les achats ne vont pas nous amener à dépasser 16 joueurs, sinon on refuse
            self.check_players_count(purchases)

        return cost

    """
     On vérifie le prix des achats
    """
    def check_purchases_price(self, purchases):

        total_cost = 0
        # on va vérifier la somme des prix des joueurs
        if 'players' in purchases:
            player_cost = 0
            # on choppe toutes les lignes de roster et on calcule le cost associé
            for player in purchases['players']:
                player_cost += Ref_Roster_Line.objects.get(pk=player['ref_roster_line']).cost

            total_cost += player_cost

        # on ajoute le coût d'un apo
        if 'apo' in purchases and purchases['apo'] == True:
            total_cost += 50

        # on ajoute le coût des rerolls
        if 'reroll' in purchases:
            reroll_price = self.ref_roster.reroll_price * 2
            total_cost += purchases['reroll'] * reroll_price

        if 'assistants' in purchases:
            total_cost += purchases['assistants'] * 10

        if 'cheerleaders' in purchases:
            total_cost += purchases['cheerleaders'] * 10

        if 'journeymens' in purchases:
            jm_cost = Ref_Roster_Line.objects.filter(reduce(lambda x, y: x | y, [Q(players=jm['player_id']) for jm in purchases['journeymens']])
                                           ).aggregate(cost=Sum('cost'))
            if jm_cost == None:
                raise NotAcceptable("Journaliers inconus, impossible de les recruter")

            total_cost += jm_cost['cost']

        # si c'est trop cher, on raise un exception
        if total_cost > self.treasury:
                raise NotAcceptable("trop cher, mon fils")

        return total_cost

    """
     On vérifie que les joueurs que l'on veut acheter sont bien dans le roster
    """
    def check_player_compatibility(self, purchases):
        if 'players' in purchases:
            # on choppe tous les types de ligne de roster présent dans la demande d'achat
            found_lines = self.ref_roster.roster_lines.filter(reduce(lambda x, y: x | y, [Q(pk=player['ref_roster_line']) for player in purchases['players']])
                                           ).count()

        if found_lines != len(set( val for dic in purchases['players'] for val in dic.values())):
            raise NotAcceptable("Un ou plusieurs joueurs à acheter ne font pas partie de ce roster")

    """
     On vérifie que les journeymens appartiennent tous bien à cette équipe
    """
    def check_journeymens(self,purchases):
        found_jm_in_team = self.players.filter(reduce(lambda x, y: x | y, [Q(pk=jm['player_id']) for jm in purchases['journeymens']])).count()

        if found_jm_in_team != len(purchases['journeymens']):
            raise NotAcceptable("Un ou plusieurs journaliers ne font pas partie de cette équipe. Achat impossible.")


    """
     On vérifie que les achats ne vont pas nous amener à dépasser 16 joueurs
    """
    def check_players_count(self,purchases):
        if len(purchases['players']) + self.players.count() > 16:
            raise NotAcceptable("Les achats contiennent trop de nouveau joueurs, on dépasse 16.")


    """
     Méthode de publication des achats. Doit être appelée après check_purchases de ce modèle
    """
    def perform_purchases(self,purchases,cost):

        # on ajoute les joueurs achetés
        if 'players' in purchases:
            # on crée les joueurs de la demande d'achat
            ag = Player.objects.filter(team=self).aggregate(Max('num'))
            current_max_num = ag['num__max']
            for player in purchases['players']:
                jm = Player(team=self,
                            ref_roster_line=Ref_Roster_Line.objects.get(pk=player['ref_roster_line']),
                            num = current_max_num+1)
                jm.init_datas()
                jm.save()

            #si on a acheté des joueurs, on doit mettre à jour le compte des journaliers
            self.update_Journeymen()

        # on ajoute le coût d'un apo
        if 'apo' in purchases and purchases['apo'] == True:
            self.apo = True

        # on ajoute le coût des rerolls
        if 'reroll' in purchases:
            self.nb_rerolls = self.nb_rerolls + purchases['reroll']

        if 'assistants' in purchases:
            self.assistants = self.assistants + purchases['assistants']

        if 'cheerleaders' in purchases:
            self.cheerleaders = self.cheerleaders + purchases['cheerleaders']

        if 'journeymens' in purchases:
            # si on doit recruter les journeymens, alors :
            # pour chaque jm à recruter
            for jm in purchases['journeymens']:
                #on choppe l'objet
                p = Player.objects.get(pk=jm['player_id'])
                # on vire ce statut de journalier
                p.is_journeyman = False
                # on vire la compétence solitaire
                p.skills.remove(name="Solitaire")
                #on save
                p.save()

        #on met à jour la trésorerie
        self.treasury = self.treasury - cost
        #lorsque tous les achats sont ok, on sauve l'instance, et on met à jour ses données
        self.save()
        #on met à jour la valeur d'équipe
        self.update_TV()

    """
     Méthode de publication des achats :
     - d'abord on vérifie les achats
     - ensuite on les publie, si tout est OK
    """
    def publish_purchases(self,purchases):
         # si on est arrivé là, on peut évaluer la validité des achats
        purchases_cost = self.check_purchases(purchases)

        # si tout marche bien navette, on publie les achats
        self.perform_purchases(purchases,purchases_cost)

    # on retourne un dictionnaire :
    # {'win' : 2,
    #  'draw' : 1,
    #  'lose' : 3}
    def get_victories_ratio(self):
        pass










