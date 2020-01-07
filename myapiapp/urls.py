from rest_framework import routers
from .views import AllUserViewSet, AdminUserViewSet, OptionsViewSet, QuestionViewSet, VoteView
from django.urls import path, include

router = routers.DefaultRouter()
router.register('allusers', AllUserViewSet)
router.register('adminusers', AdminUserViewSet)
router.register('options', OptionsViewSet)
router.register('questions', QuestionViewSet)
#router.register('vote', VoteView.as_view())

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('vote', VoteView.as_view())
]