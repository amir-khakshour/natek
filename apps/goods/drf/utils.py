import contextlib


@contextlib.contextmanager
def override_serializer(view, serializer):
    orig_serializer_class = view.serializer_class
    view.serializer_class = serializer
    yield serializer
    view.serializer_class = orig_serializer_class
