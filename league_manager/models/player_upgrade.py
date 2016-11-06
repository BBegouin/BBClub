__author__ = 'Bertrand'
from django.db import models
from rest_framework.exceptions import NotAcceptable
from league_manager.models.ref_skills import Ref_Skills
from django.db.models import Q
from functools import reduce
from django.core.exceptions import ObjectDoesNotExist

class PlayerUpgrade(models.Model):
    # 0 : simple skill
    # 1 : double skill
    # 2 : stat increase M
    # 3 : stat increase Ar
    # 4 : stat increase Ag
    # 5 : stat increase F
    value = models.PositiveSmallIntegerField(null=True)
    player = models.ForeignKey("player",related_name='upgrade')
    skill = models.ForeignKey("ref_skills", blank=True, null=True,related_name="upgrade")
    # 0 : to be done
    # 1 : done
    status = models.PositiveSmallIntegerField(null=True)
    # 0 : additionnal base skills
    # 1 : Xp
    type = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField(default=0)


    """
     On publie la mise à jour d'un joueur, en conséquence :
     - on met à jour les stats du joueur
     - on met à jour les skills du joueur
     - on met à jour le coût de l'upgrade
     - on met à jour le TV de l'équipe
    """
    def publish(self):

        if self.value == 0 or self.value == 1:
            self.check_skill()
        elif self.value >= 2 and self.value <= 5:
            self.check_stats()
        else:
            raise NotAcceptable("Cette valeur d'ugrade est inconnue")

        # si on arrive, là toutes les vérifications sont OK, donc on entame la validation.

        # on met à jour le coût de l'upgrade
        if self.value == 0 :
            self.cost = 20
        elif self.value == 1 or self.value == 2 or self.value == 3:
            self.cost = 30
        elif self.value == 4:
            self.cost = 40
        elif self.value == 5:
            self.cost = 50

        self.status = 1
        self.save()

        if self.value == 0 or self.value == 1:
            self.player.update_skills()
        elif self.value >= 2 and self.value <= 5:
            self.player.update_stats()

        self.player.team.update_TV()

    """
     On vérifie que l'augmentation de skill est compatible des possibilités du joueurs,
     On vérifie également que l'ajout de cette compétence ne ferait pas doublon
    """
    def check_skill(self):

        # on construit la chaine de selection des familles, pour vérifier que la skill est valide
        cat_string = ''
        if self.value == 0:
            cat_string = self.player.ref_roster_line.normal_skills
        elif self.value == 1:
            cat_string = self.player.ref_roster_line.normal_skills + self.player.ref_roster_line.double_skills

        # on construit la liste des skills qui correspond à l'update demandé, et
        # on essaye de chopper la skill demandée dans cette liste. et on renvoie une exception en cas d'echec
        try:
            Ref_Skills.objects.filter(reduce(lambda x, y: x | y, [Q(family=cat) for cat in cat_string])).get(pk=self.skill.id)
        except ObjectDoesNotExist:
            raise NotAcceptable("La compétence demandée n'est pas acceptable")

        # on vérifie que la skill ne fait pas doublon
        try:
            self.player.skills.get(pk=self.skill.id)
            raise NotAcceptable("La compétence demandée est un doublon")
        except ObjectDoesNotExist:
            #si l'exception claque, c'est que l'ajout est valide, donc on coninue
            pass

    """
     On vérifie que l'upgrade ne viendrait pas upgrader une stat de plus de deux points
    """
    def check_stats(self):
        # on cherche si il y a déjà deux upgrade validés sur ce joueur et sur cette stat, pour la même stats.
        up_cpt = PlayerUpgrade.objects.filter(player=self.player,value=self.value,).count()
        if up_cpt >= 2:
            raise NotAcceptable("La stat a déjà été upgradé deux fois, l'upgrade est invalide")







