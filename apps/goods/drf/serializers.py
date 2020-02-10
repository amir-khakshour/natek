from rest_framework import serializers


class VersionableHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the versionized URL that hyperlinks to the object.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value, 'version': self.context['request'].version}
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
