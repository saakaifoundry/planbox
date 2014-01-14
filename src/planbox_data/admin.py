from django.contrib import admin
from genericadmin.admin import GenericAdminModelAdmin
from planbox_data.models import User, Organization, Project, Event


class UserAdmin (admin.ModelAdmin):
    filter_horizontal = ('organizations',)
    raw_id_fields = ('auth',)


class OrganizationAdmin (admin.ModelAdmin):
    pass


class ProjectAdmin (GenericAdminModelAdmin):
    list_display = ('__unicode__', 'owner', 'slug', 'status')
    list_filter = ('status',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Project, ProjectAdmin)
