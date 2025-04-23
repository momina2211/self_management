from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageSizePagination(PageNumberPagination):
    """
    A pagination class that allows setting the `page_size` dynamically.

    This pagination class extends the `PageNumberPagination` class provided by Django REST Framework.
    It retrieves the `page_size` from the request query parameters and uses it for pagination.

    If the `page_size` parameter is not provided or cannot be converted to an integer,
    the default `page_size` defined in the pagination class will be used.

    Usage:
    - Set this class as the `pagination_class` attribute in your view.

    Example:
        class MyListView(ListAPIView):
            pagination_class = CustomPageSizePagination
            ...

    Query Parameters:
    - page_size: The number of items to include in each page.
                 If not provided or invalid, the default `page_size` will be used.

    """

    page_size = 10

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size is not None:
            try:
                return int(page_size)
            except ValueError:
                pass
        return self.page_size

    def get_paginated_response(self, data):
        """
        Overwriting method get_paginated_response to add page, start and end to pagination output style.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'start': self.page.start_index(),
            'end': self.page.end_index(),
            'results': data
        })
