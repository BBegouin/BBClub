__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views.rest_views import users

from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt

from league_manager.views.roster import RosterList
from league_manager.views.team_view_set import TeamViewSet
from league_manager.views.player_upgrade_view_set import PlayerUpgradeViewSet
from league_manager.views.match_report_view_set import MatchReportViewSet
from league_manager.views.team_report_view_set import TeamReportViewSet
from league_manager.views.skills import SkillList
from league_manager.views.player_evolution import AddBaseEvolutionView, PlayerEvolutionListView
from league_manager.views.players import PlayerList,PlayerDetail, PlayerTeam, PlayerAdditionalSkills
from league_manager.views.team_publish_view import TeamPublishView
from league_manager.views.team_unpublish_view import TeamUnPublishView
from league_manager.views.match_report_publish_view import MatchReportPublishView
from league_manager.views.match_report_unpublish_view import MatchReportUnPublishView
from league_manager.views.player_upgrade_publish_view import PlayerUpgradePublishView
from league_manager.views.player_upgrade_bulk_publish_view import PlayerUpgradeBulkPublishView
from league_manager.views.player_base_upgrade_bulk_publish_view import PlayerBaseUpgradeBulkPublishView
from league_manager.views.ranking_view import RankingView

from league_manager.views.team_purchase_view import TeamPurchaseView
from rest_framework import routers
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'team', TeamViewSet)
router.register(r'player_upgrade', PlayerUpgradeViewSet)
router.register(r'match_report', MatchReportViewSet)
router.register(r'team_report', TeamReportViewSet)

urlpatterns = [

    # user services
    # cette création utilisateur semble complètement merdique !!! url(r'^api/user/$', users.create_user),

    # check_email and user name
    url(r'^api/user/check/email/(?P<email>.+)/$', csrf_exempt(users.check_email)),
    url(r'^api/user/check/(?P<username>.+)/$', users.check_username),

    # show all rosters
    url(r'^rosters/$', RosterList.as_view()),

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

    # Publish a team
    url(r'^team/(?P<pk>.+)/publish/$', csrf_exempt(TeamPublishView.as_view())),
    url(r'^team/(?P<pk>.+)/unpublish/$', csrf_exempt(TeamUnPublishView.as_view())),
    # team purchases
    url(r'^team/(?P<pk>.+)/purchase/$', csrf_exempt(TeamPurchaseView.as_view())),

    # Publish a match report
    url(r'^match_report/(?P<pk>.+)/publish/$', csrf_exempt(MatchReportPublishView.as_view())),
    url(r'^match_report/(?P<pk>.+)/unpublish/$', csrf_exempt(MatchReportUnPublishView.as_view())),

    # Publish player upgrade
    url(r'^player_upgrade/(?P<pk>.+)/publish/$', csrf_exempt(PlayerUpgradePublishView.as_view())),
    # Publish player upgrade : bulk
    url(r'^player_upgrade/publish/$', csrf_exempt(PlayerUpgradeBulkPublishView.as_view())),
    # Publish player base upgrade : bulk
    url(r'^player_base_upgrade/publish/$', csrf_exempt(PlayerBaseUpgradeBulkPublishView.as_view())),

    url(r'^ranking/$', csrf_exempt(RankingView.as_view())),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
