# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from ...models import Task
# # from ...utils import send_reminder_email  # Implement this function
#
#
# class Command(BaseCommand):
#     help = 'Checks for due reminders and sends notifications'
#
#     def handle(self, *args, **options):
#         now = timezone.now()
#         due_tasks = Task.objects.filter(
#             reminder__lte=now,
#             reminder_sent=False,
#             completed=False
#         )
#
#         for task in due_tasks:
#             send_reminder_email(task)
#             task.reminder_sent = True
#             task.save()
#
#         self.stdout.write(f'Sent reminders for {due_tasks.count()} tasks')