from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# User Table Model
class UserTable(models.Model):
    username = models.CharField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(regex=r'^\w+$', message=_("Username must be alphanumeric"))],
        verbose_name=_("Username"),
    )
    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    table_no = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=_("Table Number"),
    )
    contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\d{10,15}$', message=_("Enter a valid contact number"))],
        verbose_name=_("Contact Number"),
    )

    class Meta:
        verbose_name = _("User Table")
        verbose_name_plural = _("User Tables")
        ordering = ['table_no']

    def __str__(self):
        return f"{self.username} (Table {self.table_no})"


# Day Book Model
class DayBook(models.Model):
    class StatusChoices(models.TextChoices):
        PERSONAL = 'personal', _("Personal")
        SALARY = 'salary', _("Salary")
        RENT = 'rent', _("Rent")
        OFFICE = 'office', _("Office")

    name = models.CharField(max_length=200, verbose_name=_("Transaction Name"))
    purpose = models.TextField(verbose_name=_("Purpose"))
    bill_no = models.PositiveIntegerField(unique=True, verbose_name=_("Bill Number"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    pay_option = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PERSONAL,
        verbose_name=_("Payment Option"),
    )
    bill_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Bill Date"))

    class Meta:
        verbose_name = _("Day Book Entry")
        verbose_name_plural = _("Day Book Entries")
        ordering = ['-bill_date']

    def __str__(self):
        return f"{self.name} ({self.bill_no})"


# Main Course Name Model
class MainCourseName(models.Model):
    main_name = models.CharField(max_length=200, verbose_name=_("Main Course Name"), unique=True)

    class Meta:
        verbose_name = _("Main Course Name")
        verbose_name_plural = _("Main Course Names")
        ordering = ['main_name']

    def __str__(self):
        return self.main_name


# Menu Items Model
class MenuItem(models.Model):
    main_course = models.ForeignKey(
        MainCourseName,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name=_("Main Course"),
    )
    name = models.CharField(max_length=300, verbose_name=_("Item Name"))
    description = models.TextField(verbose_name=_("Item Description"))
    image_url = models.URLField(verbose_name=_("Item Image URL"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Item Price"))

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")
        ordering = ['main_course', 'name']

    def __str__(self):
        return f"{self.name} - {self.price} USD"


# Final Order Model with Intermediary for Quantities
class FinalOrder(models.Model):
    user_table = models.ForeignKey(
        UserTable,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_("User Table"),
    )
    order_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='ordered_items',
        verbose_name=_("Ordered Item"),
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    order_date_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Order Date & Time"))
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Amount"),
    )

    class Meta:
        verbose_name = _("Final Order")
        verbose_name_plural = _("Final Orders")
        ordering = ['-order_date_time']

    def save(self, *args, **kwargs):
        # Calculate total amount before saving
        self.total_amount = self.quantity * self.order_item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.user_table.username}"
