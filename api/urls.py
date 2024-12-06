from rest_framework.routers import DefaultRouter
from .views import (
    UserTableViewSet,
    DayBookViewSet,
    MainCourseNameViewSet,
    MenuItemViewSet,
    FinalOrderViewSet,
)

router = DefaultRouter()
router.register(r'user-tables', UserTableViewSet, basename='user-table')
router.register(r'day-books', DayBookViewSet, basename='day-book')
router.register(r'main-courses', MainCourseNameViewSet, basename='main-course')
router.register(r'menu-items', MenuItemViewSet, basename='menu-item')
router.register(r'final-orders', FinalOrderViewSet, basename='final-order')

urlpatterns = router.urls
