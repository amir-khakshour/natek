from django.db import models
from django.db.models import SlugField
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from treebeard.mp_tree import MP_Node

from .managers import CategoryQuerySet

User = get_user_model()


class Brand(models.Model):
    """
    The Brand object, stores product brands
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(MP_Node):
    """
    A product category.

    Uses :py:mod:`django-treebeard`.
    """
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    description = models.TextField(_('Description'), blank=True)
    slug = SlugField(_('Slug'), max_length=255, db_index=True)

    _slug_separator = '/'
    _full_name_separator = ' > '

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ['path']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        names = [category.name for category in self.get_ancestors_and_self()]
        return self._full_name_separator.join(names)

    def generate_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def get_ancestors_and_self(self):
        if self.is_root():
            return [self]

        return list(self.get_ancestors()) + [self]

    def get_descendants_and_self(self):
        return self.get_tree(self)

    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_children().count()


class ProductCategory(models.Model):
    """
    Joining model between products and categories. Exists to allow customising.
    """
    product = models.ForeignKey(
        'goods.Product',
        on_delete=models.PROTECT,
        verbose_name=_("Product"))

    category = models.ForeignKey(
        'goods.Category',
        on_delete=models.PROTECT,
        verbose_name=_("Category"))

    class Meta:
        ordering = ['product', 'category']
        unique_together = ('product', 'category')
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')

    def __str__(self):
        return "<productcategory for product '%s'>" % self.product


class Product(models.Model):
    """
    The product object

    some suggestions:
    1. Move price details to another model which also stores additional data, e.g. supplier, stock record and ...
    2. remove model and utilize a hierarchical structure between products like a parent and child
    """
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True, db_index=True)

    categories = models.ManyToManyField(
        'goods.Category', through='ProductCategory',
        verbose_name=_("Categories"))

    date_updated = models.DateTimeField(
        _("Date updated"), auto_now=True, db_index=True)

    price = models.DecimalField(
        _("Cost Price"), decimal_places=2, max_digits=12)

    price_currency = models.CharField(
        _("Currency"), max_length=12, default='EUR')

    class Meta:
        ordering = ['-date_created']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    An image of a product
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Product"))
    caption = models.CharField(_("Caption"), max_length=200, blank=True)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    display_order = models.PositiveIntegerField(
        _("Display order"), default=0, db_index=True,
        help_text=_("An image with a display order of zero will be the primary"
                    " image for a product"))

    class Meta:
        ordering = ["display_order"]
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')

    def __str__(self):
        return "Image of '%s'" % self.product

    def is_primary(self):
        """
        Return bool if image display order is 0
        """
        return self.display_order == 0
