from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from dateutil.relativedelta import relativedelta


@receiver(post_save, sender=Task)
def handle_recurring_task(sender, instance, created, **kwargs):
    if not created or not instance.is_recurring or instance.recurrence_pattern == 'NONE':
        return

    if not instance.parent_task:
        instance.parent_task = instance
        instance.save()

    next_date = None
    if instance.recurrence_pattern == 'DAILY':
        next_date = instance.due_date + relativedelta(days=1)
    elif instance.recurrence_pattern == 'WEEKLY':
        next_date = instance.due_date + relativedelta(weeks=1)
    elif instance.recurrence_pattern == 'MONTHLY':
        next_date = instance.due_date + relativedelta(months=1)
    elif instance.recurrence_pattern == 'YEARLY':
        next_date = instance.due_date + relativedelta(years=1)

    if next_date and (not instance.recurrence_end or next_date <= instance.recurrence_end):
        Task.objects.create(
            title=instance.title,
            description=instance.description,
            status='TODO',
            priority=instance.priority,
            due_date=next_date,
            reminder=instance.reminder,
            category=instance.category,
            is_recurring=True,
            recurrence_pattern=instance.recurrence_pattern,
            recurrence_end=instance.recurrence_end,
            parent_task=instance.parent_task,
            owner=instance.owner
        )