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
     - on vérifie la cohérence des données envoyées
     - on met à jour les stats du joueur
     - on met à jour les skills du joueur
     - on met à jour le coût de l'upgrade
     - on met à jour le TV de l'équipe
    """
    def publish(self,upgrade_data):

        # si on ne précise pas la valeur de l'upgrade, pas la peine d'aller plus loin
        if 'value' not in upgrade_data:
            raise NotAcceptable("La valeur de l'upgrade n'est pas précisée")

        if upgrade_data['value'] < 0 or upgrade_data['value'] > 5 :
            raise NotAcceptable("La valeur de l'upgrade n'est pas valide")

        self.check_skill(upgrade_data)

        self.check_stats(upgrade_data)

        # si on arrive, là toutes les vérifications sont OK, donc on entame la publication.
        self.perform_upgrade(upgrade_data)




    """
     On vérifie que l'augmentation de skill est compatible des possibilités du joueurs,
     On vérifie également que l'ajout de cette compétence ne ferait pas doublon
    """
    def check_skill(self,upgrade_data):

        # si nous ne sommes pas dans le cas d'un upgrade de skill, on sort
        if upgrade_data['value'] !=0 and upgrade_data['value'] !=1 :
            return

        if 'skill' not in upgrade_data:
            raise NotAcceptable("La compétence n'est pas précisée")

        skill_id = upgrade_data['skill']
        # on construit la chaine de selection des familles, pour vérifier que la skill est valide
        cat_string = ''
        if upgrade_data['value'] == 0: #skill simples
            cat_string = self.player.ref_roster_line.normal_skills
        elif upgrade_data['value'] == 1: #skill simples et double
            cat_string = self.player.ref_roster_line.normal_skills + self.player.ref_roster_line.double_skills

        # on construit la liste des skills qui correspond à l'update demandé, et
        # on essaye de chopper la skill demandée dans cette liste. et on renvoie une exception en cas d'echec
        try:
            Ref_Skills.objects.filter(reduce(lambda x, y: x | y, [Q(family=cat) for cat in cat_string])).get(pk=skill_id)
        except ObjectDoesNotExist:
            raise NotAcceptable("La compétence demandée n'est pas acceptable")

        # on vérifie que la skill ne fait pas doublon avec une compétence déjà attribuée
        try:
            self.player.skills.get(pk=skill_id)
            raise NotAcceptable("La compétence demandée est un doublon")
        except ObjectDoesNotExist:
            #si l'exception claque, c'est que l'ajout est valide, donc on coninue
            pass

    """
     On vérifie que l'upgrade ne viendrait pas upgrader une stat de plus de deux points
    """
    def check_stats(self,upgrade_data):

        # si c'est une upgrade de stats, on sort
        if upgrade_data['value'] < 2  :
            return

        # on cherche si il y a déjà deux upgrade validés sur ce joueur et sur cette stat, pour la même stats.
        up_cpt = PlayerUpgrade.objects.filter(player=self.player,value=upgrade_data['value'],).count()
        if up_cpt >= 2:
            raise NotAcceptable("La stat a déjà été upgradé deux fois, l'upgrade est invalide")

    """
     Méthode de réalisation de l'upgrade
    """
    def perform_upgrade(self,upgrade_data):

        self.value = upgrade_data['value']

        # on met à jour la skill si besoin
        if self.value == 0 or  self.value == 1 :
            self.skill = Ref_Skills.objects.get(pk=upgrade_data['skill'])

        self.status = 1

        # on met à jour le coût de l'upgrade
        if self.value == 0 :
            self.cost = 20
        elif self.value == 1 or self.value == 2 or self.value == 3:
            self.cost = 30
        elif self.value == 4:
            self.cost = 40
        elif self.value == 5:
            self.cost = 50

        self.save()

        if self.value == 0 or self.value == 1:
            self.player.update_skills()
        elif self.value >= 2 and self.value <= 5:
            self.player.update_stats()

        self.player.team.update_TV()

        #on compte les upgrades liées à la team, à laquelle cet upgrade vient  si on en a 3, on publie la team
        baseupgrade_cpt = PlayerUpgrade.objects.filter(player__team = self.player.team,type =0).count()

        if baseupgrade_cpt == 3:
            self.player.team.publish()




