from django.contrib import admin
from .models import Certification, Education, Profile, Project, Semester



admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Project)
admin.site.register(Semester)