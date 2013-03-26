from django.contrib import admin
from pycoblog.models import BlogPost, BlogVar
from django.contrib.sites.models import get_current_site


class BlogVarInline(admin.TabularInline):
    model = BlogVar
    extra = 0

def make_published(modeladmin, request, queryset):
    queryset.update(status=BlogPost.STATUS_PUBLISHED)
make_published.short_description = "Set to 'published'"
def make_draft(modeladmin, request, queryset):
    queryset.update(status=BlogPost.STATUS_DRAFT)
make_draft.short_description = "Set to 'draft'"
def make_deleted(modeladmin, request, queryset):
    queryset.update(status=BlogPost.STATUS_DELETED)
make_deleted.short_description = "Set to 'deleted'"


class BlogAdmin(admin.ModelAdmin):
    actions = [make_published, make_draft, make_deleted]
    exclude = ('author', 'last_editor', 'sites', 'timezone',
               'lang', 'encoding', 'parent', 'type', )
    list_display = ('id', 'title', 'lang', 'status', 'author',
                    'date', 'last_date', )
    list_display_links = ('id', 'title', )
    list_filter = ('status', 'author', )
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
