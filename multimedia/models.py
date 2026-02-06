from django.db import models
from django.utils import timezone
import uuid


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())


def upload_to_podcast_thumbnails(instance, filename):
    """Upload path for podcast thumbnails"""
    return f'podcasts/thumbnails/{instance.id}/{filename}'


def upload_to_video_thumbnails(instance, filename):
    """Upload path for video thumbnails"""
    return f'videos/thumbnails/{instance.id}/{filename}'


def upload_to_gallery_images(instance, filename):
    """Upload path for gallery images"""
    return f'gallery/images/{instance.id}/{filename}'


class Podcast(models.Model):
    """Model for podcasts with YouTube integration"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    description = models.TextField()
    youtube_id = models.CharField(max_length=100, help_text="YouTube video ID for embedding")
    youtube_url = models.URLField(blank=True, null=True, help_text="Full YouTube URL")
    thumbnail = models.ImageField(upload_to=upload_to_podcast_thumbnails, blank=True, null=True)
    duration = models.CharField(max_length=20, help_text="Duration in MM:SS format")
    category = models.CharField(max_length=100)
    guest = models.CharField(max_length=200, blank=True, null=True, help_text="Guest speaker or host")
    featured = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Generate YouTube embed URL"""
        return f"https://www.youtube.com/embed/{self.youtube_id}?autoplay=1&rel=0"


class Video(models.Model):
    """Model for videos with YouTube integration"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    description = models.TextField()
    youtube_id = models.CharField(max_length=100, help_text="YouTube video ID for embedding")
    youtube_url = models.URLField(blank=True, null=True, help_text="Full YouTube URL")
    thumbnail = models.ImageField(upload_to=upload_to_video_thumbnails, blank=True, null=True)
    duration = models.CharField(max_length=20, help_text="Duration in MM:SS format")
    category = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Generate YouTube embed URL"""
        return f"https://www.youtube.com/embed/{self.youtube_id}?autoplay=1&rel=0"


class GalleryGroup(models.Model):
    """Model for organizing gallery images into groups/albums"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Gallery Group'
        verbose_name_plural = 'Gallery Groups'

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """Model for individual gallery images"""
    id = models.CharField(max_length=255, primary_key=True, default=generate_uuid)
    group = models.ForeignKey(GalleryGroup, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    alt_text = models.CharField(max_length=200, help_text="Alt text for accessibility")
    image = models.ImageField(upload_to=upload_to_gallery_images)
    caption = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order within the group")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['group', 'order', '-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return f"{self.group.title} - {self.title}"


class Poll(models.Model):
    """Model for Citizen Voice Polls"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=300, help_text="Poll question or title", db_index=True)
    description = models.TextField(blank=True, help_text="Detailed description of the poll")
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category or topic (e.g., Legislation, Budget, Governance)",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Current status of the poll",
    )
    start_date = models.DateTimeField(null=True, blank=True, help_text="When the poll becomes active")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When the poll closes")
    allow_multiple_votes = models.BooleanField(default=False, help_text="Allow users to vote multiple times")
    show_results_before_voting = models.BooleanField(default=False, help_text="Show results before user votes")
    featured = models.BooleanField(default=False, help_text="Feature this poll on the homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return self.title

    @property
    def total_votes(self):
        return PollVote.objects.filter(poll=self).count()

    @property
    def is_active(self):
        if self.status != 'active':
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class PollOption(models.Model):
    """Model for Poll Options/Choices"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500, help_text="Option text")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Poll Option'
        verbose_name_plural = 'Poll Options'

    def __str__(self):
        return f"{self.poll.title} - {self.text}"

    @property
    def vote_count(self):
        return PollVote.objects.filter(poll=self.poll, option=self).count()

    @property
    def vote_percentage(self):
        total = self.poll.total_votes
        if total == 0:
            return 0
        return round((self.vote_count / total) * 100, 1)


class PollVote(models.Model):
    """Model to track individual votes"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Voter's IP address")
    session_id = models.CharField(max_length=100, blank=True, help_text="Session identifier")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Poll Vote'
        verbose_name_plural = 'Poll Votes'

    def __str__(self):
        return f"Vote for {self.option.text} in {self.poll.title}"


class XPollEmbed(models.Model):
    """
    Standalone X (Twitter) poll embed. Paste the full embed code from Twitter.
    Not related to Poll.
    """
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional label for admin (e.g. poll topic)",
    )
    embed_html = models.TextField(
        help_text="Paste the full embed from Twitter: the <blockquote class=\"twitter-tweet\">...</blockquote> part.",
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'X Poll Embed'
        verbose_name_plural = 'X Poll Embeds'

    def __str__(self):
        return self.title or f"X Poll Embed #{self.id}"


class Trivia(models.Model):
    """Trivia set for Citizens Voice."""
    title = models.CharField(max_length=200, help_text="Title of the trivia set", db_index=True)
    description = models.TextField(blank=True, help_text="Short description shown on the card")
    image = models.ImageField(
        upload_to='trivia/',
        blank=True,
        null=True,
        help_text="Optional cover image for the trivia card",
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower first)")
    is_active = models.BooleanField(default=True, help_text="Show on Citizens Voice page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Trivia'
        verbose_name_plural = 'Trivia'

    def __str__(self):
        return self.title


class TriviaQuestion(models.Model):
    """A single question in a trivia set."""
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(help_text="The question shown on the card")
    answer_text = models.TextField(
        blank=True,
        help_text="Optional answer to reveal (e.g. for quiz-style trivia)",
    )
    order = models.PositiveIntegerField(default=0, help_text="Order within the trivia")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Trivia Question'
        verbose_name_plural = 'Trivia Questions'

    def __str__(self):
        return self.question_text[:50] + ('...' if len(self.question_text) > 50 else '')


class TriviaOption(models.Model):
    """Multiple choice option for a trivia question. One option should be marked as correct."""
    question = models.ForeignKey(TriviaQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500, help_text="Option text")
    is_correct = models.BooleanField(default=False, help_text="Whether this is the correct answer")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Trivia Option'
        verbose_name_plural = 'Trivia Options'

    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.text}"