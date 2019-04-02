from django.contrib import admin

from .models import *

admin.site.register([Jedi, Planet, Trial])
