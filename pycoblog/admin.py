from django.contrib import admin
from pycoblog.models import BlogPost, BlogVar, BlogConfig
from django.contrib.sites.models import get_current_site
from django import forms

class ConfigAdmin(admin.ModelAdmin):
    exclude = ('section', )
    list_display = ('key', 'value', )
    ordering = ('key',)
    def save_model(self, request, obj, form, change):
        obj.section = 'pycoblog'
        super(ConfigAdmin, self).save_model(request, obj, form, change)

admin.site.register(BlogConfig, ConfigAdmin)

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

class BlogModelForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('deleted', 'Deleted'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = BlogPost

class BlogAdmin(admin.ModelAdmin):
    actions = [make_published, make_draft, make_deleted]
    exclude = ('author', 'last_editor', 'sites', 'lang', 'encoding',
               'parent', 'type', 'date', 'last_date', 'format', )
    list_display = ('id', 'title', 'lang', 'status', 'author',
                    'date', 'last_date', )
    list_display_links = ('id', 'title', )
    list_filter = ('status', 'author', 'lang', )
    inlines = (BlogVarInline, )
    ordering = ('-date',)
    form = BlogModelForm
    
    def save_model(self, request, obj, form, change):
        from django.conf import settings
        from django.utils import timezone
        obj.lang = settings.LANGUAGE_CODE
        obj.last_editor = request.user
        obj.last_date = timezone.now()
        if not change:
            obj.author = request.user
            obj.date = timezone.now()
        obj.format = 'raw'
        super(BlogAdmin, self).save_model(request, obj, form, change)
        
        if not change:
            obj.sites.add(get_current_site(request))
admin.site.register(BlogPost, BlogAdmin)

