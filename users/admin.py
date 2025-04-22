from django.contrib import admin
from .models import User,UserProfile



admin.site.register(User)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'date_of_birth')
    search_fields = ('user__username', 'language')
    list_filter = ('language',)

