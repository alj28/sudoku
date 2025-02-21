from django.contrib import admin

from score.models import ScoreModel, SessionModel

# Register your models here.
admin.site.register(ScoreModel)
admin.site.register(SessionModel)