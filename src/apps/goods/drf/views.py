from .utils import as_tuple


class ReadWriteSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set read_serializer_class and write_serializer_class attributes on a viewset.
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, \
            ("'%s' should either include a `read_serializer_class` attribute,"
             "or override the `get_read_serializer_class()` method."
             % self.__class__.__name__
             )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, \
            ("'%s' should either include a `write_serializer_class` attribute, "
             "or override the `get_write_serializer_class()` method."
             % self.__class__.__name__
             )
        return self.write_serializer_class


class PermissionViewMixin(object):
    default_mapping = {
        'get': 'retrieve',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
        'options': 'options',
    }
    _header_data = {}
    _objects = {}

    @as_tuple
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        for permcls in self.permission_classes:
            instance = permcls(request=self.request, view=self)
            yield instance

    def get_permission_object(self, request):
        return None

    def check_permissions(self, request, action: str = None, obj=None):
        obj = obj if obj else self.get_permission_object(request)
        if action is None:
            if request.method.lower() in self.action_map:
                action = self.action_map[request.method.lower()]
            else:
                action = self.default_mapping[request.method.lower()]
        for permission in self.get_permissions():
            if not permission.has_permission(action=action, obj=obj):
                self.permission_denied(request)

