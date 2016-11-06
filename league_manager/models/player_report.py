__author__ = 'Bertrand'
from django.db import models

class PlayerReport(models.Model):
    team_report = models.ForeignKey("TeamReport",related_name="player_report")
    player = models.ForeignKey("player",on_delete=models.SET_NULL,null=True)
    nb_pass = models.PositiveSmallIntegerField(default=0)
    nb_td = models.PositiveSmallIntegerField(default=0)
    nb_int = models.PositiveSmallIntegerField(default=0)
    nb_cas = models.PositiveSmallIntegerField(default=0)
    mvp = models.BooleanField(default=False)
    nb_foul = models.PositiveSmallIntegerField(default=0)
    nb_blocks = models.PositiveSmallIntegerField(default=0)
    # 0 Commotion Aucun effet à long terme
    # 1 un match d'arrêt
    # 2 blessure persistante
    # 3 -1 M
    # 4 -1 Ar
    # 5 -1 Ag
    # 6 -1 F
    # 7 Mort
    injury_type = models.PositiveSmallIntegerField(null=True)
    earned_xp = models.PositiveSmallIntegerField(null=True)

    """
      Lors de la sauvegarde d'un player report on met à jour les xp gagnés,
      et on met à jour le nombre total de xp du joueur, ainsi que le status d'upgrade

    def save(self, *args, **kwargs):
        self.compute_earned_xps()
        self.player.updateXp()
        super(PlayerReport, self).save(*args, **kwargs) # Call the "real" save() method.
    """

    """
     si on supprime un rapport de joueur, il faut également mettre à jour les statut
     du joueur concerné
    """
    def delete(self, *args, **kwargs):
        player = self.player
        super(PlayerReport, self).delete(*args, **kwargs) # Call the "real" save() method.
        player.update_Xp()


    """
        méthode utilitaire permettant de calculer les xp gagnés sur ce rapport :
        # 1 sortie = 2 xp
        # 1 interception = 2 xp
        # 1 Td = 3 xp
        # 1 passe = 1 xp
        # 1 JPV = 5 xp
    """
    def update_earned_xps(self):
        earned_xp = self.nb_cas * 2
        earned_xp += self.nb_pass
        earned_xp += self.nb_td *3
        earned_xp += self.nb_int *2
        if self.mvp:
            earned_xp += 5
        self.earned_xp = earned_xp
        self.save()


