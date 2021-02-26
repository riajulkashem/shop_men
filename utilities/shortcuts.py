from django.apps import apps
from django.contrib import admin


def register_all_model_to_admin(app_label, search_list=None, filter_list=None):
    class ListAdminMixin(object):
        def __init__(self, model, admin_site):
            self.list_display = [field.name for field in model._meta.fields]
            if hasattr(model, 'created'):
                self.date_hierarchy = 'created'
            self.list_per_page = 50
            if search_list:
                self.search_fields = search_list
            if filter_list:
                self.list_filter = filter_list
            super(ListAdminMixin, self).__init__(model, admin_site)

    models = apps.all_models[app_label]
    for model in models:
        if '_' in str(model):
            continue
        admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin),
                           {})
        Model = apps.get_model(app_label, model)
        try:
            admin.site.register(Model, admin_class)
        except admin.sites.AlreadyRegistered:
            pass
