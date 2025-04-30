from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from fitness.workout.models import Exercise, WorkoutPlan,ExerciseCategory


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'instructions', 'default_reps', 'default_sets', 'rest_time_seconds']

class ExerciseCategorySerializer(serializers.ModelSerializer):
    exercises =ExerciseSerializer (source='Exercises', many=True, read_only=True)
    exercise_ids = serializers.PrimaryKeyRelatedField(
        source='Exercises',
        queryset=Exercise.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = ExerciseCategory
        fields = ['id', 'name', 'user', 'exercises', 'exercise_ids']
        read_only_fields = ['user']

    def create(self, validated_data):
        user=self.context['request'].user
        exercises = validated_data.pop('Exercises', [])
        exercise_category = ExerciseCategory.objects.create(**validated_data)
        exercise_category.Exercises.set(exercises)
        return exercise_category

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise PermissionDenied("You are not authorized to update this category.")
        exercises = validated_data.pop('Exercises', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if exercises is not None:
            instance.Exercises.set(exercises)
        return instance

    def destroy(self, instance):
        user = self.context['request'].user
        if instance.user != user:
            raise PermissionDenied("You are not authorized to delete this category.")
        instance.delete()


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises =serializers.PrimaryKeyRelatedField( queryset=Exercise.objects.all(),source='exercise',many=True,required=False)
    price = serializers.DecimalField( max_digits=10,decimal_places=2, min_value=Decimal('0.50'),required=False  )

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'name', 'level', 'user','price','visibility', 'exercises']
        read_only_fields = ['user']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        price = validated_data.get('price', None)
        if price is not None:
            validated_data['price'] = Decimal(str(price))
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        workout_plan.exercise.set(exercises_data)
        return workout_plan

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise PermissionDenied("You are not authorized to update this workout plan.")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        exercises_data = validated_data.pop('exercises', None)
        instance.save()
        if exercises_data is not None:
            instance.exercise.set(exercises_data)
        return instance

    def destroy(self, instance):
        user = self.context['request'].user
        if instance.user != user:
            raise PermissionDenied("You are not authorized to delete this workout plan.")
        instance.delete()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        exercises = instance.exercise.all()
        representation['exercises'] = ExerciseSerializer(exercises, many=True).data
        return representation


class PurchaseWorkoutPlanSerializer(serializers.Serializer):
    workout_plan_id = serializers.UUIDField()
    payment_method_id = serializers.CharField()

    def validate_workout_plan_id(self, value):
        try:
            plan = WorkoutPlan.objects.get(
                id=value,
                visibility=WorkoutPlan.VisibilityChoices.PRIVATE,
            )
            if plan.user == self.context['request'].user:
                raise serializers.ValidationError("You cannot purchase your own plan")
            return plan
        except WorkoutPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or non-purchasable workout plan")