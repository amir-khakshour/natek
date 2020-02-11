# -*- coding: utf-8 -*-
import abc
import inspect

from functools import reduce

from django.utils.translation import ugettext as _


######################################################################
# Base permissiones definition
######################################################################

class ResourcePermission(object):
    """
    Base class for define resource permissions.
    """

    options_perms = None
    enought_perms = None
    global_perms = None
    retrieve_perms = None
    create_perms = None
    update_perms = None
    destroy_perms = None
    list_perms = None

    def __init__(self, request, view):
        self.request = request
        self.view = view

    def has_object_permission(self, request, view, obj):
        """
        Default implementation to check for object permission
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return True

    def has_permission(self, action: str, obj: object = None):
        permset = getattr(self, "{}_perms".format(action), getattr(self, 'global_perms'))
        if isinstance(permset, (list, tuple)):
            permset = reduce(lambda acc, v: acc & v, permset)
        elif permset is None:
            # Use empty operator that always return true with
            # empty components.
            permset = And()
        elif isinstance(permset, PermissionComponent):
            # Do nothing
            pass
        elif inspect.isclass(permset) and issubclass(permset, PermissionComponent):
            permset = permset()
        else:
            raise RuntimeError(_("Invalid permission definition."))

        if self.global_perms:
            permset = (self.global_perms & permset)

        if self.enought_perms:
            permset = (self.enought_perms | permset)
        perm_func = permset.has_object_permission if obj and hasattr(permset, 'has_object_permission') else permset.has_permission
        return perm_func(
            request=self.request,
            view=self.view,
            obj=obj
        )


class PermissionComponent(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def has_permission(self, request, view, obj=None):
        pass

    def __invert__(self):
        return Not(self)

    def __and__(self, component):
        return And(self, component)

    def __or__(self, component):
        return Or(self, component)


class PermissionOperator(PermissionComponent):
    """
    Base class for all logical operators for compose
    components.
    """

    def __init__(self, *components):
        self.components = tuple(components)


class Not(PermissionOperator):
    """
    Negation operator as permission composable component.
    """

    # Overwrites the default constructor for fix
    # to one parameter instead of variable list of them.
    def __init__(self, component):
        super().__init__(component)

    def has_permission(self, *args, **kwargs):
        component = self.components[0]
        return (not component.has_permission(*args, **kwargs))


class Or(PermissionOperator):
    """
    Or logical operator as permission component.
    """

    def has_permission(self, *args, **kwargs):
        valid = False

        for component in self.components:
            if component.has_permission(*args, **kwargs):
                valid = True
                break

        return valid


class And(PermissionOperator):
    """
    And logical operator as permission component.
    """

    def has_permission(self, *args, **kwargs):
        valid = True

        for component in self.components:
            if not component.has_permission(*args, **kwargs):
                valid = False
                break

        return valid


######################################################################
# Generic components.
######################################################################

class AllowAny(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        return True


class DenyAll(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        return False


class IsAuthenticated(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        return request.user and request.user.is_authenticated


class IsSuperUser(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsStaffUser(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsTheSameUser(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        return obj and request.user.is_authenticated and request.user.pk == obj.pk


class IsObjectOwner(PermissionComponent):
    def has_permission(self, request, view, obj=None):
        if obj.owner is None:
            return False

        return obj.owner == request.user


######################################################################
# Generic permissions.
######################################################################

class AllowAnyPermission(ResourcePermission):
    enought_perms = AllowAny()


class IsAuthenticatedPermission(ResourcePermission):
    enought_perms = IsAuthenticated()


class ResourcePermission(ResourcePermission):
    enought_perms = IsSuperUser()
