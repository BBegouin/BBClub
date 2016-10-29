__author__ = 'Bertrand'
from django.db import models
import django
from league_manager.models.player_upgrade import PlayerUpgrade
from django.db.models import Sum

# table associatif xp : nombre d'upgrade
upgrade_table = {
    6,
    16,
    31,
    51,
    76,
    176
}

class Player(models.Model):
    name = django.db.models.CharField(max_length=50,null=True,blank=True)
    miss_next_game = django.db.models.BooleanField()
    ref_roster_line = django.db.models.ForeignKey("ref_roster_line",related_name="players")
    team = django.db.models.ForeignKey("team",related_name="players")
    num = django.db.models.SmallIntegerField()
    total_xp = django.db.models.SmallIntegerField()
    need_upgrade = django.db.models.BooleanField()

    # Permet de savoir si un joueur doit monter de niveau ou pas
    def IsUpgradeNeeded(self):
        # on compte le nombre d'upgrade, autre que ceux de base
        upgrade_cpt = PlayerUpgrade.objects.filter(player=self.id,type=1).count()

        # en fonction des xp gagnés, on compte le nombre d'upgrade théorique
        needed_upgrade = 0
        for val in upgrade_table:
            if self.total_xp > val:
                needed_upgrade += 1
            else:
                break

        # si on devrait avoir plus d'upgrade que la réalité, alors, on doit upgrader
        if needed_upgrade > upgrade_cpt:
            return True
        else:
            return False





