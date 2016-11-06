__author__ = 'Bertrand'
from django.db import models
import django
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.match_report import TeamReport
from django.db.models import Sum
from league_manager.models.player_report import PlayerReport
from league_manager.models.ref_skills import Ref_Skills
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# table associatif xp : nombre d'upgrade
upgrade_table = [
    6,
    16,
    31,
    51,
    76,
    176
]

class Player(models.Model):
    name = django.db.models.CharField(max_length=50,null=True,blank=True)
    miss_next_game = django.db.models.BooleanField(default=False)
    ref_roster_line = django.db.models.ForeignKey("ref_roster_line",related_name="players")
    team = django.db.models.ForeignKey("team",related_name="players")
    num = django.db.models.SmallIntegerField()
    total_xp = django.db.models.SmallIntegerField(default=0)
    need_upgrade = django.db.models.BooleanField(default=False)
    is_journeyman = django.db.models.BooleanField(default=False)
    M = models.PositiveSmallIntegerField(null=True,)
    F = models.PositiveSmallIntegerField(null=True,)
    Ag = models.PositiveSmallIntegerField(null=True,)
    Ar = models.PositiveSmallIntegerField(null=True,)
    skills = models.ManyToManyField("ref_skills",null=True,)
    niggling_injuries = models.PositiveSmallIntegerField(default=0)

    def init_datas(self):
        # on met à jour les caracs
        self.update_stats()

        # on met à jour les skills
        self.update_skills()

        self.save()
    """
     On met a jour les données du joueur, à partir des données de base auxquelle on vient appliquer les upgrade
    """
    def update_datas(self):

        # on met à jour les caracs
        self.update_stats()

        # on met à jour les skills
        self.update_skills()

        # on met à jour le "total Xp"
        self.update_Xp()

        # on met à jour le "need_upgrade"
        self.update_need_upgrade()

        # on met à jour le "miss_next_game"
        self.update_mng()

    """
     on met à jour les stats en fonction des upgrade et des stats de base
    """
    def update_stats(self):

        # on choppe les stats de base
        M = self.ref_roster_line.M
        F = self.ref_roster_line.F
        Ag = self.ref_roster_line.Ag
        Ar = self.ref_roster_line.Ar

        # on choppe les upgrades, en maxant à 2 par carac
        upgrade_M = PlayerUpgrade.objects.filter(status=1,value=2,player=self).count()
        if upgrade_M > 2:
            upgrade_M = 2
        upgrade_F = PlayerUpgrade.objects.filter(status=1,value=3,player=self).count()
        if upgrade_F > 2:
            upgrade_F = 2
        upgrade_Ag = PlayerUpgrade.objects.filter(status=1,value=4,player=self).count()
        if upgrade_Ag > 2:
            upgrade_Ag = 2
        upgrade_Ar = PlayerUpgrade.objects.filter(status=1,value=5,player=self).count()
        if upgrade_Ar > 2:
            upgrade_Ar = 2

        # on choppe les downgrades en minant à -2 par carac
        downgrade_M = PlayerReport.objects.filter(player=self,injury_type=3).count()
        if downgrade_M > 2:
            downgrade_M = 2
        downgrade_F = PlayerReport.objects.filter(player=self,injury_type=6).count()
        if downgrade_F > 2:
            downgrade_F = 2
        downgrade_Ag = PlayerReport.objects.filter(player=self,injury_type=5).count()
        if downgrade_Ag > 2:
            downgrade_Ag = 2
        downgrade_Ar = PlayerReport.objects.filter(player=self,injury_type=4).count()
        if downgrade_Ar > 2:
            downgrade_Ar = 2

        # on affecte les stats
        self.M = M + upgrade_M - downgrade_M
        self.F = F + upgrade_F - downgrade_F
        self.Ag = Ag + upgrade_Ag - downgrade_Ag
        self.Ar = Ar + upgrade_Ar - downgrade_Ar

        self.save()

    """
     on met à jour les skills en fonction des skills de base et des upgrades
    """
    def update_skills(self):
        self.skills.clear()

        # on ajoute les compétences de base
        for skill in self.ref_roster_line.base_skills.all():
            self.skills.add(skill)

        # on prend toutes les competences qui sont référencés par un upgrade de ce joueur
        upgrade_skill = Ref_Skills.objects.filter(upgrade__status=1,upgrade__player=self).filter(Q(upgrade__value=0)|Q(upgrade__value=1))
        # on ajoute les compétences d'upgrade
        for skill in upgrade_skill:
            try:
                self.skills.get(id=skill.id)
            except ObjectDoesNotExist:
                # on ne fait l'ajout que si la compétence n'est pas déjà présente
                self.skills.add(skill)

        self.save()

    """
     On prend le dernier rapport de match de l'équipe de ce joueur,
     et si le joueur a été blessé, alors il manquera le match.
     Au passage on met à jour le compteur de blessures persistantes, si besoin.
     Sinon, il jouera.
    """
    def update_mng(self):
        latest_tr = TeamReport.objects.filter(team = self.team).last()
        try:
            pr = PlayerReport.objects.get(team_report=latest_tr,player=self)
        except ObjectDoesNotExist:
            # le joueur n'a pas été concerné par le match, par conséquent, il jouera forcément le suivant
            self.miss_next_game = False
            self.save()
            return

        if pr.injury_type is None:
            self.miss_next_game = False

        # si le joueur est mort, on le supprime
        elif pr.injury_type == 7 :
                self.delete()
                return

        elif pr.injury_type > 0:
                self.miss_next_game = True
                #on met à jour les blessures persistantes
                if pr.injury_type == 2:
                    self.niggling_injuries = self.niggling_injuries + 1
        elif pr.injury_type == 0:
                self.miss_next_game = False

        self.save()



    """
     On met à jour le nombre total de xp du joueur,
     ainsi que le statut need upgrade
    """
    def update_Xp(self):
        # on calcule le nombre total de Xp
        ret = PlayerReport.objects.filter(player=self).aggregate(totalXP = Sum('earned_xp'))
        if (ret['totalXP'] is None):
            self.total_xp = 0
        else:
            self.total_xp = ret['totalXP']

        self.save()

    """
     Permet de savoir si un joueur doit monter de niveau ou pas
    """
    def update_need_upgrade(self):
        # on compte le nombre d'upgrade, autre que ceux de base
        upgrade_cpt = PlayerUpgrade.objects.filter(player=self.id).count()

        # en fonction des xp gagnés, on compte le nombre d'upgrade théorique
        needed_upgrade = 0
        for val in upgrade_table:
            if self.total_xp >= val:
                needed_upgrade += 1
            else:
                break

        # si on a plus d'upgrade que nécessaire, on supprime le dernier upgrade pour ce joueur
        if upgrade_cpt > needed_upgrade:
            self.need_upgrade = False
            for up in range(needed_upgrade,upgrade_cpt):
                PlayerUpgrade.objects.filter(player=self.id,type=1).last().delete()

        # si on devrait avoir plus d'upgrade que la réalité, alors, on doit upgrader
        if needed_upgrade > upgrade_cpt:
            self.need_upgrade = True
            # on crée un upgrade à faire, de type expérience
            for up in range(upgrade_cpt,needed_upgrade):
                PlayerUpgrade.objects.create(player=self,status=0,type=1)

        if needed_upgrade == upgrade_cpt:
            self.need_upgrade = False

        self.save()





