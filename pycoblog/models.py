from djazz.posts.models import Post, PostManager, PostVar


class BlogManager(PostManager):
    def get_query_set(self):
        q = super(BlogManager, self).get_query_set()
        return q.filter(type='blogpost')
    
    def get_published(self):
        q = self.get_query_set()
        return q.filter(status='published')
    
    def get_draft(self):
        q = self.get_query_set()
        return q.filter(status='draft')
    
    def get_deleted(self):
        q = self.get_query_set()
        return q.filter(status='deleted')


class BlogPost(Post):
    
    STATUS_PUBLISHED = 'published'
    STATUS_DRAFT = 'draft'
    STATUS_DELETED = 'deleted'
    
    TYPE = 'blogpost'
    objects = BlogManager()
    
    class Meta:
        proxy = True
    
    def set_published(self):
        self.status = self.STATUS_PUBLISHED
        return self
    
    def set_draft(self):
        self.status = self.STATUS_DRAFT
        return self
    
    def set_deleted(self):
        self.status = self.STATUS_DELETED
        return self

class BlogVar(PostVar):
    class Meta:
        proxy = True
