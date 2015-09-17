from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import CourtAdminProfile


admin.site.unregister(User)

class UserProfileAdmin(admin.StackedInline):
    model = CourtAdminProfile
    max_num = 1
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileAdmin, ]

admin.site.register(User, UserAdmin)
