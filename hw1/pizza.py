from typing import List, Optional

class MenuItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


class IPizza(MenuItem):
    def __init__(self, name: str, price: float, size: str, crust_type: str, sauce: str, toppings: List["Topping"]):
        super().__init__(name, price)
        self.size = size
        self.crust_type = crust_type
        self.sauce = sauce
        self.toppings = toppings

    def get_description(self) -> str:
        topping_names = ", ".join(topping.topping_name for topping in self.toppings)
        return f"{self.size} {self.name} Pizza with {self.crust_type} crust, {self.sauce} sauce, toppings: {topping_names}"

    def get_cost(self) -> float:
        toppings_cost = sum(topping.cost for topping in self.toppings)
        return self.price + toppings_cost


class Margherita(IPizza):
    def __init__(self, size="Medium", crust_type="Thin", sauce="Tomato"):
        super().__init__("Margherita", 10.0, size, crust_type, sauce, [Tomato(), Cheese()])

class Neapolitan(IPizza):
    def __init__(self, size="Large", crust_type="Hand Tossed", sauce="Marinara"):
        super().__init__("Neapolitan", 12.0, size, crust_type, sauce, [Tomato(), Cheese()])

class Topping:
    def __init__(self, topping_name: str, cost: float):
        self.topping_name = topping_name
        self.cost = cost

class Tomato(Topping):
    def __init__(self):
        super().__init__("Tomato", 2.0)


class Cheese(Topping):
    def __init__(self):
        super().__init__("Cheese", 3.0)


class Pepperoni(Topping):
    def __init__(self):
        super().__init__("Pepperoni", 2.5)


class Pineapple(Topping):
    def __init__(self):
        super().__init__("Pineapple", 2.0)

class Drink(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)


class Side(MenuItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)

class Combo(MenuItem):
    def __init__(self, name, pizza: IPizza, drink: Drink, side: Side, discount: float = 0.1):
        self.pizza = pizza
        self.drink = drink
        self.side = side
        self.discount = discount
        super().__init__(name, self.get_cost())

    def get_cost(self) -> float:
        return (self.pizza.get_cost() + self.drink.price + self.side.price) * (1 - self.discount)

class Payment:
    def __init__(self, msg: str = "Payment Successful"):
        self.msg = msg

    def pay(self, amount: float) -> str:
        return f"{self.msg}: Paid ${amount:.2f}"


class CreditCardPayment(Payment):
    def __init__(self):
        super().__init__("Success via Credit Card")


class GooglePay(Payment):
    def __init__(self):
        super().__init__("Success via Google Pay")


class Cash(Payment):
    def __init__(self):
        super().__init__("Success via Cash")

class OrderValidation:
    def __init__(self):
        self.next_validator: Optional["OrderValidation"] = None

    def set_next(self, next_validator: "OrderValidation") -> "OrderValidation":
        self.next_validator = next_validator
        return next_validator

    def validate(self, order: "Order"):
        if self.next_validator:
            self.next_validator.validate(order)


class InventoryCheck(OrderValidation):
    def validate(self, order: "Order"):
        print("Checking inventory...")
        super().validate(order)


class AddressCheck(OrderValidation):
    def validate(self, order: "Order"):
        print("Checking address validity...")
        super().validate(order)


class PaymentCheck(OrderValidation):
    def validate(self, order: "Order"):
        print("Verifying payment...")
        super().validate(order)

class FedexService:
    def __init__(self):
        self.msg = "Success via FedEx"

    def ship(self, address: str) -> str:
        return f"{self.msg}: Order shipped to {address}"


class LogisticAdapter:
    def __init__(self):
        self.fedex_service = FedexService()

    def ship_order(self, order: "Order") -> str:
        return self.fedex_service.ship(order.customer.address)


class Order:
    def __init__(self, order_id: int, customer: "Customer"):
        self.order_id = order_id
        self.customer = customer
        self.items: List[MenuItem] = []
        self.payment: Optional[Payment] = None

    def add_menu_item(self, item: MenuItem):
        self.items.append(item)

    def apply_discount(self, discount: float):
        for item in self.items:
            item.price *= (1 - discount)

    def set_payment(self, payment: Payment):
        self.payment = payment

    def process_order(self):
        if not self.payment:
            print("No payment method set.")
            return

        total_cost = sum(item.price for item in self.items)
        print(self.payment.pay(total_cost))


class Customer:
    def __init__(self, customer_id: int, name: str, email: str, phone: str, address: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address


if __name__ == "__main__":
    # Create customer
    customer = Customer(1, "John Doe", "john@example.com", "123-1234", "123 Main St")

    # Create an order
    order = Order(1001, customer)

    # Add items
    pizza = Margherita()
    drink = Drink("Coke", 2.5)
    side = Side("Chicken Wings", 3.0)
    combo = Combo("Margherita Chicken Combo", pizza, drink, side, 0.1)
    order.add_menu_item(pizza)
    order.add_menu_item(drink)
    order.add_menu_item(side)
    order.add_menu_item(combo)

    # Set payment
    order.set_payment(CreditCardPayment())

    # Process order
    order.process_order()

    # Order Validation Chain
    inventory_check = InventoryCheck()
    address_check = AddressCheck()
    payment_check = PaymentCheck()

    inventory_check.set_next(address_check).set_next(payment_check)
    inventory_check.validate(order)

    # Ship order
    logistics = LogisticAdapter()
    print(logistics.ship_order(order))
