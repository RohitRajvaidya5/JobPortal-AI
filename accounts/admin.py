from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, CandidateProfile, RecruiterProfile, Job, Resume, Application

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Job)
admin.site.register(Resume)
admin.site.register(Application)
