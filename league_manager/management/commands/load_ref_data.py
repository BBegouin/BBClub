__author__ = 'Bertrand'

from django.core.management.base import BaseCommand, CommandError
from league_manager.models.ref_skills import Ref_Skills
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.league import League
from league_manager.models.starting_rules import StartingRules
from django.contrib.auth.models import User
from django.conf import settings

import csv

data_dir = getattr(settings, "PROJECT_ROOT", None)+'/datas'

class Command(BaseCommand):
    help = 'load lrb6 base datas'

    def handle(self, *args, **options):
        self.init_user()
        self.init_league()
        self.init_ref_skills()
        self.init_ref_rosters()
        self.init_rosters_lines()
        self.init_rosters_journeymens()

    def init_user(self):
        bbe = user = User.objects.create_user('Bagouze', 'bertrand.begouin@gmail.com', 'ignakO75')
        bbe.save()

    def init_league(self):
        startingRules = StartingRules(  max_budget = 1150,
                                        max_simple_skills = 3,
                                        max_double_skills = 1,)
        startingRules.save()

        newLeague = League(name="la compagnie du Valdemor",starting_rules = startingRules)
        newLeague.save()

    def init_ref_skills(self):

        with open(data_dir+'/skills.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                new_skill = Ref_Skills(
                    name = row[1].strip(),
                    family=row[2].strip(),
                    desc = ""
                )
                new_skill.save();
                print(row[1] + " inserted !")

    def init_ref_rosters(self):

        with open(data_dir+'/rosters.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                new_roster = Ref_Roster(
                    name = row[0].strip(),
                    reroll_price=row[1].strip(),
                    apo_available=row[2]
                )
                new_roster.save();
                print(row[0] + " inserted !")

    #
    #
    #
    def init_rosters_lines(self):

        with open(data_dir+'/rosters_lines.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:

                print(row)

                linked_roster = Ref_Roster.objects.get(name = row[0])

                new_line = Ref_Roster_Line (
                    roster = linked_roster,
                    max = row[1],
                    position = row[2],
                    cost = row[3],
                    M = row[4],
                    F = row[5],
                    Ag = row[6],
                    Ar = row[7],
                    normal_skills = row[9],
                    double_skills = row[10],
                )

                new_line.save()

                print(linked_roster)
                if row[8] == '':
                    continue

                skill_list = row[8].split(",")

                for skill in skill_list:
                    skill = skill.strip(" ")
                    print(skill)
                    linked_skill = Ref_Skills.objects.get(name = skill)
                    new_line.base_skills.add(linked_skill);

                print (new_line.roster.name + " " + new_line.position + " Inserted !")


        # vérifier que tous les rosters du fichiers, sont bien dans la table roster ref
        # vérifier que toutes les compétences du fichier sont bien dans la table ref_skill


    def init_rosters_journeymens(self):

        with open(data_dir+'/rosters.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                roster = Ref_Roster.objects.get(name=row[0])
                roster.journeyman = Ref_Roster_Line.objects.get(pk=row[3])
                roster.save();