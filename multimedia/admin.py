from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Podcast, Video, GalleryGroup, GalleryImage,
    Poll, PollOption, PollVote, XPollEmbed, Trivia, TriviaQuestion, TriviaOption,
)


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'guest', 'duration', 'featured', 'date']
    list_filter = ['category', 'featured', 'date']
    search_fields = ['title', 'description', 'guest']
    list_editable = ['featured']
    ordering = ['-date', '-created_at']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'featured', 'date']
    list_filter = ['category', 'featured', 'date']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    ordering = ['-date', '-created_at']


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['title', 'alt_text', 'image', 'caption', 'order']
    show_change_link = True


@admin.register(GalleryGroup)
class GalleryGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_count', 'featured', 'date']
    list_filter = ['featured', 'date']
    search_fields = ['title', 'description']
    list_editable = ['featured']
    inlines = [GalleryImageInline]
    ordering = ['-date', '-created_at']
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'order', 'created_at']
    list_filter = ['group', 'created_at']
    search_fields = ['title', 'alt_text', 'caption']
    list_editable = ['order']
    ordering = ['group', 'order', '-created_at']


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2
    ordering = ['order']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'total_votes_display', 'featured', 'created_at']
    list_filter = ['status', 'category', 'featured', 'created_at']
    search_fields = ['title', 'description', 'category']
    list_editable = ['featured', 'status']
    inlines = [PollOptionInline]
    ordering = ['-featured', '-created_at']

    def total_votes_display(self, obj):
        return obj.total_votes
    total_votes_display.short_description = 'Total Votes'


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'order', 'vote_count_display', 'vote_percentage_display']
    list_filter = ['poll', 'created_at']
    search_fields = ['text', 'poll__title']
    ordering = ['poll', 'order']

    def vote_count_display(self, obj):
        return obj.vote_count
    vote_count_display.short_description = 'Votes'

    def vote_percentage_display(self, obj):
        return f"{obj.vote_percentage}%"
    vote_percentage_display.short_description = 'Percentage'


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option', 'ip_address', 'created_at']
    list_filter = ['poll', 'created_at']
    search_fields = ['poll__title', 'option__text', 'ip_address']
    ordering = ['-created_at']


@admin.register(XPollEmbed)
class XPollEmbedAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['title', 'embed_html']
    ordering = ['order', '-created_at']


class TriviaOptionInline(admin.TabularInline):
    model = TriviaOption
    extra = 2
    ordering = ['order']


class TriviaQuestionInline(admin.TabularInline):
    model = TriviaQuestion
    extra = 1
    ordering = ['order']


@admin.register(Trivia)
class TriviaAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'question_count_display', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    inlines = [TriviaQuestionInline]
    ordering = ['order', '-created_at']

    def question_count_display(self, obj):
        return obj.questions.count()
    question_count_display.short_description = 'Questions'


@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ['trivia', 'order', 'question_preview', 'option_count', 'created_at']
    list_filter = ['trivia', 'created_at']
    search_fields = ['question_text', 'answer_text', 'trivia__title']
    ordering = ['trivia', 'order']
    inlines = [TriviaOptionInline]

    def question_preview(self, obj):
        return obj.question_text[:60] + ('...' if len(obj.question_text) > 60 else '')
    question_preview.short_description = 'Question'

    def option_count(self, obj):
        return obj.options.count()
    option_count.short_description = 'Options'


@admin.register(TriviaOption)
class TriviaOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'text_preview', 'is_correct', 'order', 'created_at']
    list_filter = ['is_correct', 'question__trivia', 'created_at']
    search_fields = ['text', 'question__question_text', 'question__trivia__title']
    ordering = ['question', 'order']
    list_editable = ['is_correct', 'order']

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Option'