__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views.rest_views import users

from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt

from league_manager.views.roster import RosterList
from league_manager.views.team import TeamCreate,TeamList,TeamDetail
from league_manager.views.skills import SkillList
from league_manager.views.player_evolution import AddBaseEvolutionView, PlayerEvolutionListView
from league_manager.views.players import PlayerList,PlayerDetail, PlayerTeam, PlayerAdditionalSkills

urlpatterns = [

    # user services
    # cette création utilisateur semble complètement merdique !!! url(r'^api/user/$', users.create_user),

    # check_email and user name
    url(r'^api/user/check/email/(?P<email>.+)/$', csrf_exempt(users.check_email)),
    url(r'^api/user/check/(?P<username>.+)/$', users.check_username),

    # show all rosters
    url(r'^rosters/$', RosterList.as_view()),

    # create a team
    url(r'^team/create/$', csrf_exempt(TeamCreate.as_view())),
    url(r'^team/$', TeamList.as_view()),
    url(r'^team/(?P<pk>.+)/$', TeamDetail.as_view()),

    # skills
    url(r'^skills/(?P<skill_cat>.+)/$', csrf_exempt(SkillList.as_view())),

    # player evolution
    url(r'^evolution/addbaseskills/$', csrf_exempt(AddBaseEvolutionView.as_view())),
    url(r'^evolution/', csrf_exempt(PlayerEvolutionListView.as_view())),

    # player
    url(r'^player/$', csrf_exempt(PlayerList.as_view())),
    url(r'^player/(?P<pk>.+)/team/$', csrf_exempt(PlayerTeam.as_view())),
    url(r'^player/(?P<pk>.+)/skills/$', csrf_exempt(PlayerAdditionalSkills.as_view())),
    url(r'^player/(?P<pk>.+)/$', csrf_exempt(PlayerDetail.as_view())),


]

urlpatterns = format_suffix_patterns(urlpatterns)
