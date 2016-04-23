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



#author_extra_fieldsets = ((None, {"fields": ("dob",)}),)

#class BookInline(admin.TabularInline):
#    model = Book.Book
#
#class AuthorAdmin(PageAdmin):
#    inlines = (BookInline,)
#    fieldsets = deepcopy(PageAdmin.fieldsets) + author_extra_fieldsets
#
#admin.site.register(Author.Author, AuthorAdmin)