from __future__ import absolute_import, unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class HomePage(Page):
    header_image_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        ImageChooserPanel('header_image_logo'),
        InlinePanel('players', label='Players'),
        InlinePanel('navigation_items', label="Navigation items"),
    ]


@register_snippet
class Position(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    content_panels = [
        FieldPanel('description'),
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title


class Players(Orderable, models.Model):
    page = ParentalKey('home.HomePage', related_name='players')
    position = models.ForeignKey('home.Position', related_name='+')

    content_panels = [
        SnippetChooserPanel('lecture'),
    ]

    def __str__(self):
        return "{} -> {}".format(self.page.title, self.position.title)


@register_snippet
class NavigationItem(Orderable, models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    redirect_to = models.CharField(max_length=40, blank=True, null=True)

    content_panels = [
        FieldPanel('name'),
        FieldPanel('redirect_to'),
    ]

    def __str__(self):
        return self.name


class NavigationItems(Orderable, models.Model):
    page = ParentalKey('home.HomePage', related_name='navigation_items')
    navigation_item = models.ForeignKey('home.NavigationItem', related_name='+')

    panels = [
        SnippetChooserPanel('navigation_item'),
    ]
