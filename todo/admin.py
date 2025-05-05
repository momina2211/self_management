from django.contrib import admin
from .models import Task, Category, Tag

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'priority', 'due_date', 'completed')
    list_filter = ('status', 'priority', 'completed', 'category')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name',)