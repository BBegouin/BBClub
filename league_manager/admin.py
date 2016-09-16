from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
#from league_manager.models import Author,Book
from league_manager.models import player
from league_manager.models import ref_roster
from league_manager.models import ref_roster_line
from league_manager.models import ref_skills
from league_manager.models import xp_rolls
from league_manager.models import team
from league_manager.models import league
from league_manager.models.coach import Coach
from league_manager.models.club import Club
from league_manager.models.match_report import Match_Report
from league_manager.models.team_report import Team_Report
from league_manager.models.player_report import Player_Report
from league_manager.models.ref_skills import Ref_Skills
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.ref_roster_line import Ref_Roster_Line

from image_cropping import ImageCroppingMixin

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(league.League)
admin.site.register(Coach)
admin.site.register(Club)
admin.site.register(Ref_Roster)
admin.site.register(Ref_Roster_Line)
admin.site.register(Match_Report)
admin.site.register(Team_Report)
admin.site.register(Player_Report)
admin.site.register(Ref_Skills)
