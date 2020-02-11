import contextlib

from functools import wraps, partial


@contextlib.contextmanager
def override_serializer(view, serializer):
    orig_serializer_class = view.serializer_class
    view.serializer_class = serializer
    yield serializer
    view.serializer_class = orig_serializer_class


def as_tuple(function=None, *, remove_nulls=False):
    if function is None:
        return partial(as_tuple, remove_nulls=remove_nulls)

    @wraps(function)
    def _decorator(*args, **kwargs):
        return list(function(*args, **kwargs))

    return _decorator
