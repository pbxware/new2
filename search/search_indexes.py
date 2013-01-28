# coding=utf-8
from haystack import indexes
from cms.models.pagemodel import Page


class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    title = indexes.CharField(stored=True, indexed=False, model_attr='get_title')
    url = indexes.CharField(stored=True, indexed=False, model_attr='get_absolute_url')
    pub_date = indexes.DateTimeField(model_attr='publication_date')
    login_required = indexes.BooleanField(model_attr='login_required')

    def get_model(self):
        return Page

    def prepare(self, obj):
        prepared_data = super(PageIndex, self).prepare(obj)
        placeholders = obj.placeholders.all()
        out = []
        for placeholder in placeholders:
            plugins = placeholder.cmsplugin_set.all()
            for plugin in plugins:
                instance, _ = plugin.get_plugin_instance()
                if hasattr(instance, 'search_fields'):
                    out.extend(getattr(instance, field) for field in instance.search_fields)

        prepared_data['text'] = ' '.join(out)
        return prepared_data

    def index_queryset(self):
        return self.get_model().objects.published().distinct()
