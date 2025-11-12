from django.contrib import admin
from .models import (
    HeroSection, WhoWeAreSection, WhoWeAreFeature, StatCard,
    OurStorySection, OurStoryCard, WhatSetsUsApartSection,
    WhatSetsUsApartCard, CallToActionSection
)


class WhoWeAreFeatureInline(admin.TabularInline):
    model = WhoWeAreFeature
    extra = 0
    fields = ['icon', 'title', 'description', 'order']
    can_delete = True


class OurStoryCardInline(admin.TabularInline):
    model = OurStoryCard
    extra = 0
    fields = ['icon', 'title', 'description', 'order']
    can_delete = True


class WhatSetsUsApartCardInline(admin.TabularInline):
    model = WhatSetsUsApartCard
    extra = 0
    fields = ['title', 'description', 'order']
    can_delete = True


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Hero Content', {
            'fields': ('title', 'description', 'hero_image')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not HeroSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the singleton
        return False


@admin.register(WhoWeAreSection)
class WhoWeAreSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    readonly_fields = ['updated_at']
    inlines = [WhoWeAreFeatureInline]
    fieldsets = (
        ('Section Content', {
            'fields': ('title', 'description')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not WhoWeAreSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WhoWeAreFeature)
class WhoWeAreFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']
    list_editable = ['order']
    fields = ['section', 'icon', 'title', 'description', 'order']


@admin.register(StatCard)
class StatCardAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order', 'updated_at']
    list_editable = ['order']
    fields = ['value', 'label', 'order']


@admin.register(OurStorySection)
class OurStorySectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    readonly_fields = ['updated_at']
    inlines = [OurStoryCardInline]
    fieldsets = (
        ('Section Content', {
            'fields': ('title', 'description')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not OurStorySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OurStoryCard)
class OurStoryCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']
    list_editable = ['order']
    fields = ['section', 'icon', 'title', 'description', 'order']


@admin.register(WhatSetsUsApartSection)
class WhatSetsUsApartSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    readonly_fields = ['updated_at']
    inlines = [WhatSetsUsApartCardInline]
    fieldsets = (
        ('Section Content', {
            'fields': ('title', 'description')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not WhatSetsUsApartSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WhatSetsUsApartCard)
class WhatSetsUsApartCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']
    list_editable = ['order']
    fields = ['section', 'title', 'description', 'order']


@admin.register(CallToActionSection)
class CallToActionSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Section Content', {
            'fields': ('title', 'description')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not CallToActionSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False