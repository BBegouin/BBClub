from copy import deepcopy
from django.contrib import admin

from league_manager.models import league
from league_manager.models.club import Club
from league_manager.models.match_report import MatchReport
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.models.ref_skills import Ref_Skills
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.player import Player
from league_manager.models.team import Team
from league_manager.models.xp_roll import Xp_Roll
from league_manager.models.injury_roll import Injury_Roll
from league_manager.models.player_downgrade import PlayerDowngrade

from image_cropping import ImageCroppingMixin

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(league.League)
admin.site.register(Club)
admin.site.register(Ref_Roster)
admin.site.register(Ref_Roster_Line)
admin.site.register(MatchReport)
admin.site.register(TeamReport)
admin.site.register(PlayerReport)
admin.site.register(Ref_Skills)
admin.site.register(PlayerUpgrade)
