from django.contrib import admin
from .models import User, Attendense, WorkTypes, Position, Late
from django.contrib.auth.models import User as Us, Group

admin.site.register(User)
admin.site.register(Attendense)
admin.site.register(WorkTypes)
admin.site.register(Position)
admin.site.register(Late)

admin.site.unregister(Us)
admin.site.unregister(Group)