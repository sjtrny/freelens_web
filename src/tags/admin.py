from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tag._meta.get_fields()]
    readonly_fields = [field.name for field in Tag._meta.fields if not field.editable]


admin.site.register(Tag, TagAdmin)
