from rest_framework.pagination import PageNumberPagination


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


def search_result(request, queryset):
    data = request.query_params
    if len(list(data.keys())) > 0 and 'search' in list(data.keys()):
        value = data['search']
        fields = data.getlist('search_fields')
        search_dict = {}
        for field in fields:
            if value in ['True', 'False']:
                search_dict[field] = eval(value)
                continue
            search_dict[field + '__icontains'] = value
        return queryset.filter(**search_dict)
    return queryset
