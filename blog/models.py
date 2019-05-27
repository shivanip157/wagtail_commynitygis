from __future__ import unicode_literals

import datetime
from datetime import date

from django import forms
from django.db import models
from django.http import Http404, HttpResponse
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format

import wagtail
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
										 InlinePanel, MultiFieldPanel,
										 PageChooserPanel, StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from blog.blocks import TwoColumnBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtailmd.utils import MarkdownField, MarkdownPanel
# Create your models here.



class BlogPage(RoutablePageMixin, Page):
	description = models.CharField(max_length=255, blank=True,)

	content_panels = Page.content_panels + [
		FieldPanel('description', classname="full")
	]

	def get_context(self, request, *args, **kwargs):
		context = super(BlogPage, self).get_context(request,*args, **kwargs)
		context['posts'] = self.posts
		context['blog_page'] = self
		return context

	def get_posts(self):
		return PostPage.objects.descendant_of(self).live()

	@route(r'^tag/(?P<tag>[-\w]+)/$')
	def post_by_tag(self, request, tag, *args, **kwargs):
		self.search_type = 'tag'
		self.search_term = tag
		self.posts = self.get_posts().filter(tags__slug=tag)
		return Page.serve(self, request, *args, **kwargs)

	@route(r'^category/(?P<category>[-\w]+)/$')
	def post_by_category(self, request, category, *args, **kwargs):
		self.search_type = 'category'
		self.search_term = category
		self.posts = self.get_posts().filter(categories__slug=category)
		return Page.serve(self, request, *args, **kwargs)

	@route(r'^$')
	def post_list(self, request, *args, **kwargs):
		self.posts = self.get_posts()
		return Page.serve(self, request, *args, **kwargs)




class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
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

@property
def blog_page(self):
		return self.get_parent().specific

def get_context(self, request, *args, **kwargs):
		context = super(PostPage, self).get_context(request, *args, **kwargs)
		context['blog_page'] = self.blog_page
		context['post'] = self
		return context       


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
