from ..drf.permissions import ResourcePermission, IsSuperUser, IsStaffUser, AllowAny


class ProductPermissions(ResourcePermission):
    enought_perms = IsSuperUser()
    global_perms = AllowAny()
    retrieve_perms = AllowAny()

    create_perms = IsStaffUser()
    destroy_perms = IsStaffUser()
    update_perms = IsStaffUser()
    partial_update_perms = IsStaffUser()
