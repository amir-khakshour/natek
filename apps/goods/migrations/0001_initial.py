# Generated by Django 2.2.9 on 2020-02-08 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['path'],
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Cost Price')),
                ('price_currency', models.CharField(default='EUR', max_length=12, verbose_name='Currency')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.Brand')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ['-date_created'],
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=200, verbose_name='Caption')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('display_order', models.PositiveIntegerField(db_index=True, default=0, help_text='An image with a display order of zero will be the primary image for a product', verbose_name='Display order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name_plural': 'Product images',
                'ordering': ['display_order'],
                'verbose_name': 'Product image',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.Category', verbose_name='Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name_plural': 'Product categories',
                'unique_together': {('product', 'category')},
                'ordering': ['product', 'category'],
                'verbose_name': 'Product category',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(through='goods.ProductCategory', to='goods.Category', verbose_name='Categories'),
        ),
    ]
