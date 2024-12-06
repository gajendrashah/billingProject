from rest_framework import serializers
from .models import UserTable, DayBook, MainCourseName, MenuItem, FinalOrder

# User Table Serializer
class UserTableSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()  # Calculate total orders made by the user table

    class Meta:
        model = UserTable
        fields = '__all__'

    def get_total_orders(self, obj):
        return obj.orders.count()  # Count the number of related orders


# Day Book Serializer
class DayBookSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()  # Format the date in a readable way

    class Meta:
        model = DayBook
        fields = '__all__'

    def get_formatted_date(self, obj):
        return obj.bill_date.strftime('%B %d, %Y %I:%M %p')  # Format example: "December 06, 2024 02:30 PM"


# Main Course Name Serializer
class MainCourseNameSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()  # Count the total menu items under this main course

    class Meta:
        model = MainCourseName
        fields = '__all__'

    def get_total_items(self, obj):
        return obj.menu_items.count()  # Count related menu items


# Menu Item Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    main_course = serializers.StringRelatedField()  # Display the name of the related main course
    is_expensive = serializers.SerializerMethodField()  # Add a dynamic field to flag expensive items

    class Meta:
        model = MenuItem
        fields = '__all__'

    def get_is_expensive(self, obj):
        return obj.price > 50.00  # Flag items as expensive if their price exceeds 50 USD


# Final Order Serializer
class FinalOrderSerializer(serializers.ModelSerializer):
    user_table = UserTableSerializer(read_only=True)  # Include nested user table details
    order_item = MenuItemSerializer(read_only=True)  # Include nested ordered item details
    user_table_id = serializers.PrimaryKeyRelatedField(
        queryset=UserTable.objects.all(), source='user_table', write_only=True
    )  # Allow user table selection by ID
    order_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='order_item', write_only=True
    )  # Allow order item selection by ID

    class Meta:
        model = FinalOrder
        fields = '__all__'
        read_only_fields = ['total_amount', 'order_date_time']

    def create(self, validated_data):
        # Automatically calculate total amount during order creation
        order = FinalOrder(**validated_data)
        order.total_amount = order.quantity * order.order_item.price
        order.save()
        return order

    def update(self, instance, validated_data):
        # Automatically update total amount if quantity or order item changes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.total_amount = instance.quantity * instance.order_item.price
        instance.save()
        return instance
