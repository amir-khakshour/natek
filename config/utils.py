import six
from operator import itemgetter


def build_component_list(base, custom):
    """Compose a component list based on a custom and base dict of components
    (typically middlewares or extensions), unless custom is already a list, in
    which case it's returned.
    """
    if isinstance(custom, (list, tuple)):
        return custom
    compdict = base.copy()
    compdict.update(custom)
    items = (x for x in six.iteritems(compdict) if x[1] is not None)
    return [x[0] for x in sorted(items, key=itemgetter(1))]

