from rest_framework import serializers
from .models import Task, Category, Tag
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, required=False)
    category = CategorySerializer(required=False)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'reminder',
            'completed',
            'completed_at',
            'category',
            'tags',
            'is_recurring',
            'recurrence_pattern',
            'recurrence_end',
            'Created_at',
            'updated_at',
            'owner'
        ]
        read_only_fields = ['id', 'Created_at', 'updated_at', 'owner', 'completed_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', None)

        task = Task.objects.create(**validated_data)

        if category_data:
            category, _ = Category.objects.get_or_create(
                name=category_data['name'],
                owner=validated_data['owner']
            )
            task.category = category

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(
                name=tag_data['name'],
                owner=validated_data['owner']
            )
            task.tags.add(tag)

        task.save()
        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        category_data = validated_data.pop('category', None)

        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(
                    name=tag_data['name'],
                    owner=instance.owner
                )
                instance.tags.add(tag)

        if category_data:
            category, _ = Category.objects.get_or_create(
                name=category_data['name'],
                owner=instance.owner
            )
            instance.category = category
        elif category_data == {}:  # Handle category removal
            instance.category = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance