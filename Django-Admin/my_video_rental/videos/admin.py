from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from . import models
from django.utils.html import format_html

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    fields = ['release_year','title','length','font_size']

    search_fields = ['title','length']

    list_filter = ['release_year','title','length','font_size']

    list_display = ['title','release_year','length','font_size_html_display']

    list_editable = ['length']

    change_list_template = 'admin/videos/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fontsize/<int:size>/', self.change_font_size)
        ]
        return custom_urls + urls

    def change_font_size(self, request, size):
        self.model.objects.all().update(font_size=size)
        self.message_user(request, 'font size set successfully')
        return HttpResponseRedirect("../")

    def font_size_html_display(self, obj):
        display_size = obj.font_size if obj.font_size <= 30 else 30
        return format_html(
            f'<span style="font-size: {display_size}px;">{obj.font_size}</span>'
        )


admin.site.register(models.Customer)
admin.site.register(models.Movie,MovieAdmin)
