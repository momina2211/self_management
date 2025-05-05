from django.db import models
from django.utils import timezone
from users.models import User
from users.utils.models import UUIDMODEL


class Category(UUIDMODEL):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('name', 'owner')

    def __str__(self):
        return self.name


class Tag(UUIDMODEL):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='tags', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'owner')

    def __str__(self):
        return self.name


class Task(UUIDMODEL):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    RECURRENCE_CHOICES = [
        ('NONE', 'None'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    due_date = models.DateField(blank=True, null=True)
    reminder = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='NONE')
    recurrence_end = models.DateField(blank=True, null=True)
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='recurring_instances')
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

    def is_reminder_due(self):
        if self.reminder:
            return timezone.now() >= self.reminder
        return False

    class Meta:
        ordering = ['-Created_at']