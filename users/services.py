import stripe

from config.settings import STRIPE_API_KEY
stripe.api_key = STRIPE_API_KEY


def create_stripe_product_and_price(product_name, amount):
    '''Создает продукт и цену в Stripe.'''
    product = stripe.Product.create(name=product_name)
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.get('id'),
    )

def create_stripe_session(price):
    '''Создает сессию на оплату в Stripe.'''
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/lms/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
