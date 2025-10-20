from rest_framework import status
from rest_framework.response import Response

# Apply this mixin to any view or viewset to get multiple field filtering
# based on a `lookup_fields` attribute, instead of the default single field filtering.
class MultipleFieldLookupMixin:

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter_kwargs[field] = self.kwargs[field]
        obj = queryset.get(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


# Mixin to provide soft delete functionality to viewsets
class SoftDeleteMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
