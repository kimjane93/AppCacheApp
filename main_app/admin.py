from django.contrib import admin
from .models import Profile, Technologie, App, Note, BuildLink

# Register your models here.
admin.site.register(Profile)
admin.site.register(Technologie)
admin.site.register(App)
admin.site.register(Note)
admin.site.register(BuildLink)