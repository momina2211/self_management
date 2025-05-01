import stripe


def create_stripe_products(workout_plan, user):
    """Helper method to create Stripe product and price"""
    product = stripe.Product.create(
        name=workout_plan.name,
        description=f"Workout Plan: {workout_plan.name}",
        metadata={
            'workout_plan_id': str(workout_plan.id),
            'user_id': str(user.id),
            'system': 'FitnessApp'
        }
    )

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(workout_plan.price * 100),  # Convert to cents
        currency='usd',
        metadata={
            'workout_plan_id': str(workout_plan.id),
            'user_id': str(user.id)
        }
    )

    # Update our model with Stripe IDs
    workout_plan.stripe_product_id = product.id
    workout_plan.stripe_price_id = price.id
    workout_plan.save(update_fields=['stripe_product_id', 'stripe_price_id'])

def update_stripe_products(workout_plan):
    """Helper method to update Stripe product and create new price"""
    # Update product name/description if changed
    stripe.Product.modify(
        workout_plan.stripe_product_id,
        name=workout_plan.name,
        description=f"Workout Plan: {workout_plan.name}",
    )

    # Create new price (since prices are immutable)
    new_price = stripe.Price.create(
        product=workout_plan.stripe_product_id,
        unit_amount=int(workout_plan.price * 100),
        currency='usd',
        metadata={
            'workout_plan_id': str(workout_plan.id),
            'user_id': str(workout_plan.user.id)
        }
    )

    # Update our model with new price ID
    workout_plan.stripe_price_id = new_price.id
    workout_plan.save(update_fields=['stripe_price_id'])