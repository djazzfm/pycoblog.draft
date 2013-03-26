from django.contrib import admin
from pycoblog.models import BlogPost, BlogVar
from django.contrib.sites.models import get_current_site

class BlogVarInline(admin.TabularInline):
    model = BlogVar
    extra = 0

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lang', 'author', 'last_editor',
                    'date', 'last_date', 'timezone',)
    list_display_links = ('id', 'title', )
    exclude = ('author', 'last_editor', 'sites', 'timezone',
               'lang', 'encoding', 'parent', 'type', )
    inlines = (BlogVarInline,)
    
    def save_model(self, request, obj, form, change):
        from django.conf import settings
        obj.lang = settings.LANGUAGE_CODE
        obj.last_editor = request.user
        if not change:
            obj.author = request.user
        obj.timezone = settings.TIME_ZONE
        super(BlogAdmin, self).save_model(request, obj, form, change)
        
        if not change:
            obj.sites.add(get_current_site(request))


admin.site.register(BlogPost, BlogAdmin)
