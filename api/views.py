from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserTable, DayBook, MainCourseName, MenuItem, FinalOrder
from .serializers import (
    UserTableSerializer,
    DayBookSerializer,
    MainCourseNameSerializer,
    MenuItemSerializer,
    FinalOrderSerializer,
)

# User Table ViewSet
class UserTableViewSet(viewsets.ModelViewSet):
    queryset = UserTable.objects.all()
    serializer_class = UserTableSerializer

# Day Book ViewSet
class DayBookViewSet(viewsets.ModelViewSet):
    queryset = DayBook.objects.all()
    serializer_class = DayBookSerializer

# Main Course Name ViewSet
class MainCourseNameViewSet(viewsets.ModelViewSet):
    queryset = MainCourseName.objects.all()
    serializer_class = MainCourseNameSerializer

# Menu Item ViewSet
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# Final Order ViewSet
class FinalOrderViewSet(viewsets.ModelViewSet):
    queryset = FinalOrder.objects.all()
    serializer_class = FinalOrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create to include custom error handling or additional logic
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Override update to handle updates and automatic total amount recalculation
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
