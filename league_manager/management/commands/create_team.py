__author__ = 'Bertrand'

from django.core.management.base import BaseCommand, CommandError
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.ref_skills import Ref_Skills
from league_manager.models.ref_roster_line import Ref_Roster_Line

class Command(BaseCommand):
    help = 'Show lrb6 roster details'

    def handle(self, *args, **options):
        roster_list = Ref_Roster.objects.all()

        for roster in roster_list:
            print ("=====================================================================")
            print (roster.name)
            print ("Reroll :"+str(roster.reroll_price)+ " pO")
            print ('---------------------------------------------------------------------')
            roster_lines = Ref_Roster_Line.objects.filter(roster=roster)
            for line in roster_lines:
                skills = line.base_skills;
                print()
                print(str(line.max) +" "+line.position+ " "+str(line.cost)+" "+str(line.M)+" "+str(line.F)+" "+str(line.Ag)+" "+str(line.Ar)+" ".join([skill.name for skill in skills.all()])+" "+line.normal_skills+" "+line.double_skills)


        self.stdout.write(self.style.SUCCESS('Et voilà !"'))