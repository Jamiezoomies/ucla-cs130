import pytest
from pizza import (
    Margherita, Neapolitan, Drink, Side, Combo, CreditCardPayment,
    GooglePay, Cash, Order, Customer, LogisticAdapter, InventoryCheck,
    AddressCheck, PaymentCheck
)

def test_margherita_pizza():
    pizza = Margherita()
    assert pizza.get_description() == "Medium Margherita Pizza with Thin crust, Tomato sauce, toppings: Tomato, Cheese"
    assert pizza.get_cost() == 15.0


def test_neapolitan_pizza():
    pizza = Neapolitan()
    assert pizza.get_description() == "Large Neapolitan Pizza with Hand Tossed crust, Marinara sauce, toppings: Tomato, Cheese"
    assert pizza.get_cost() == 17.0


def test_combo_discount():
    pizza = Margherita()
    drink = Drink("Coke", 2.5)
    side = Side("Chicken Wings", 3.0)
    combo = Combo("Margherita Chicken Wings Combo", pizza, drink, side, 0.1)
    
    expected_cost = (15.0 + 2.5 + 3.0) * 0.9
    assert combo.get_cost() == expected_cost


def test_credit_card_payment():
    payment = CreditCardPayment()
    assert payment.pay(20) == "Success via Credit Card: Paid $20.00"


def test_google_pay_payment():
    payment = GooglePay()
    assert payment.pay(15) == "Success via Google Pay: Paid $15.00"


def test_cash_payment():
    payment = Cash()
    assert payment.pay(10) == "Success via Cash: Paid $10.00"


def test_order_processing():
    customer = Customer(1, "John Doe", "john@example.com", "123-1234", "123 Main St")
    order = Order(1001, customer)

    pizza = Margherita()
    drink = Drink("Coke", 2.5)
    side = Side("Dipping Sauce", 1.0)

    order.add_menu_item(pizza)
    order.add_menu_item(drink)
    order.add_menu_item(side)
    
    order.set_payment(CreditCardPayment())

    assert len(order.items) == 3
    assert order.payment is not None
    assert order.payment.pay(15.5) == "Success via Credit Card: Paid $15.50"


def test_shipping():
    customer = Customer(1, "John Doe", "john@example.com", "123-1234", "123 Main St")
    order = Order(1001, customer)
    
    logistic_adapter = LogisticAdapter()
    shipping_result = logistic_adapter.ship_order(order)
    
    assert shipping_result == "Success via FedEx: Order shipped to 123 Main St"


def test_order_validation_chain():
    customer = Customer(1, "John Doe", "john@example.com", "123-1234", "123 Main St")
    order = Order(1001, customer)

    inventory_check = InventoryCheck()
    address_check = AddressCheck()
    payment_check = PaymentCheck()

    inventory_check.set_next(address_check).set_next(payment_check)

    try:
        inventory_check.validate(order)
    except Exception as e:
        pytest.fail(f"Validation chain failed with error: {e}")
