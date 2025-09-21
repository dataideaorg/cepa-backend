from rest_framework.routers import DefaultRouter
from .views import ContactSubmissionViewSet

router = DefaultRouter()
router.register(r'submissions', ContactSubmissionViewSet, basename='contact-submission')

urlpatterns = router.urls
