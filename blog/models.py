from __future__ import unicode_literals
from django.db import models


from wagtail.core.models import Page
from django import forms

from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField, StreamField     
from wagtail.snippets.models import register_snippet 
from modelcluster.fields import ParentalKey, ParentalManyToManyField 
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager

# Create your models here.
class BlogPage(Page):
    description = models.CharField(max_length=255, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

class PostPage(Page):
    body = RichTextField(blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
         FieldPanel('tags'),
    ]



@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')


class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(FormPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    def get_form_fields(self):
        return self.custom_form_fields.all()

    @property
    def blog_page(self):
        return self.get_parent().specific

