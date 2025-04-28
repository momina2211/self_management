from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import BMISerializer


class BMICalculateView(GenericAPIView):
    serializer_class = BMISerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1. Calculate BMI (simple math)
        height_m = data['height_cm'] / 100
        bmi = round(data['weight_kg'] / (height_m ** 2), 1)

        # 2. Determine category
        category = self._get_bmi_category(bmi)

        # 3. Generate smart advice (no API)
        advice = self._generate_health_advice(
            bmi=bmi,
            age=data['age'],
            gender=data['gender']
        )

        return Response({
            "bmi": bmi,
            "category": category,
            "advice": advice,
        })

    def _get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def _generate_health_advice(self, bmi, age, gender):
        advice = []

        # Weight management tips
        if bmi < 18.5:
            advice.append("Consider increasing calorie intake with nutrient-rich foods.")
        elif bmi >= 25:
            advice.append("Aim for gradual weight loss with portion control.")

        # Exercise recommendations
        if bmi < 25:
            advice.append("Maintain your weight with 30 mins of daily exercise.")
        else:
            advice.append("Include 45 mins of cardio (walking, cycling) 5x/week.")

        # Age-specific tips
        if age > 40:
            advice.append("Consider strength training to maintain muscle mass.")
        elif age < 25:
            advice.append("Stay active with sports or gym workouts.")

        # Gender-specific tips
        if gender == "female":
            advice.append("Ensure adequate iron and calcium intake.")
        else:
            advice.append("Monitor protein intake for muscle health.")

        return " ".join(advice)
