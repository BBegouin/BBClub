from django.contrib import admin

# Register your models here.
from bbc_content.models import like

admin.site.register(like.Like)
