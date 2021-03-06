# Generated by Django 2.1.8 on 2019-04-16 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('blog', '0004_remove_postpage_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpagetag',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='blogpagetag',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='formfield',
            name='page',
        ),
        migrations.RemoveField(
            model_name='formpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.RemoveField(
            model_name='postpage',
            name='categories',
        ),
        migrations.DeleteModel(
            name='BlogCategory',
        ),
        migrations.DeleteModel(
            name='BlogPageTag',
        ),
        migrations.DeleteModel(
            name='FormField',
        ),
        migrations.DeleteModel(
            name='FormPage',
        ),
    ]
