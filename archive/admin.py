from models import *
from django.contrib import admin

admin.site.register(Issue, IssueAdmin)
admin.site.register(File, FileAdmin)
