from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Page)
admin.site.register(Selection)
admin.site.register(Transition)