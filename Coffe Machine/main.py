import datetime


class Resource:
    def __init__(self, name):
        self.name: str = name


class Item:
    def __init__(self, name, price, ingredients: dict[Resource, int]):
        self.name: str = name
        self.price: float = price
        self.ingredients = ingredients


class OrderItem(Item):
    def __init__(self, name, price, ingredients, quantity):
        super().__init__(name, price, ingredients)
        self.quantity: int = quantity

    def get_cost(self):
        return self.quantity * self.price

    def get_receipt(self):
        return "%s x %s -> %s$" % (self.name, self.quantity, self.get_cost())


class Order:
    def __init__(self):
        self.datetime = datetime.datetime.now()
        self.o_items: list[OrderItem] = []

    def add_item(self, item: OrderItem):
        self.o_items.append(item)

    def get_items(self) -> list[OrderItem]:
        return self.o_items

    def calculate_total(self):
        total = 0
        for order_item in self.o_items:
            total += order_item.price * order_item.quantity
        return total

    def print_receipt(self):
        print("===============Reciept===============")
        print(self.datetime.strftime("Order Date: %m/%d/%Y, %H:%M:%S"))
        for o_i in self.o_items:
            print(o_i.get_receipt())
        print("total: %s$" % self.calculate_total())


class Menu:
    def __init__(self, items: list[Item]):
        self.items = items

    def print_menu(self):
        print("===========Coffee type================")
        for i in range(len(self.items)):
            print("%s) %s  - (Price: %s$)" % (i + 1, self.items[i].name, self.items[i].price))
        index = int(input("Enter item index: "))
        if 1 <= index <= len(self.items) + 1:
            return self.items[index-1]
        return None


class Stock:
    def __init__(self, stock: dict[Resource, int]):
        self.stock = stock

    def calculate_needed_resources(self, order: Order) -> dict[Resource, int]:
        needed_resources: dict[Resource, int] = {}
        for o_i in order.o_items:
            for k in o_i.ingredients.keys():
                needed_resources[k] = (o_i.quantity * o_i.ingredients[k]) + (
                    needed_resources[k] if k in needed_resources.keys() else 0)
        return needed_resources

    def is_sufficient_resources(self, order: Order):
        needed_resources = self.calculate_needed_resources(order)
        for r in needed_resources.keys():
            if self.stock[r] - needed_resources[r] < 0:
                return False
        return True

    def execute_order(self, order: Order):
        needed_resources = self.calculate_needed_resources(order)
        for r in needed_resources.keys():
            self.stock[r] = self.stock[r] - needed_resources[r]

    def show_stock(self):
        print("Stock:", " - ".join(["%s -> %s" % (k.name, v) for k, v in self.stock.items()]))


class CoffeeMachine:
    def __init__(self, stock: Stock, items: list[Item]):
        self.money = 0
        self.stock = stock
        self.items = items
        self.menu = Menu(items)

    def main_menu(self):
        exit_loop = False
        while not exit_loop:
            print("==========Coffee Machine Menu==========")
            print("Press")
            print("1) Make order")
            print("2) Show summary")
            print("3) Exit")
            print("======================================")
            choice = int(input())
            match choice:
                case 1:
                    self.order_menu()
                    continue
                case 2:
                    self.show_summary()
                    continue
                case 3:
                    exit_loop = True
                    continue
                case default:
                    print("Error choice!")
                    continue

    def show_summary(self):
        print("Total money: %s$" % self.money)
        self.stock.show_stock()

    def order_menu(self):
        exit_loop = False
        order = Order()
        while not exit_loop:
            print("=============Add Item Menu============")
            print("1) Add item")
            print("2) Show order")
            print("3) Process order")
            print("4) Done")
            print("======================================")
            choice = int(input())
            match choice:
                case 1:
                    item = self.menu.print_menu()
                    if item is None:
                        print("Item error")
                        continue
                    qty = int(input("Enter quantity: "))
                    order.add_item(OrderItem(item.name, item.price, item.ingredients, qty))
                    continue
                case 2:
                    order.print_receipt()
                    continue
                case 3:
                    exit_loop = True
                    if not self.stock.is_sufficient_resources(order):
                        print("Not sufficient resources !")
                        continue
                    self.process_payment(order)
                    self.money += order.calculate_total()
                    self.stock.execute_order(order)
                    order.print_receipt()
                case 4:
                    exit_loop = True
                    continue

    def process_payment(self, order):
        print("==========Payment Processor===========")
        print("Waiting payment of %s." % order.calculate_total())
        print("Payment received.")
        self.money + order.calculate_total()
        return True


if __name__ == '__main__':
    beans = Resource("Beans")
    milk = Resource("Milk")
    sugar = Resource("Sugar")
    my_stock = Stock({
        beans: 5000,
        milk: 100,
        sugar: 2000
    })
    black_coffee = Item("Black Coffee", 3, {beans: 10, sugar: 1})
    black_coffee_no_sugar = Item("Black Coffee (No Sugar)", 3, {beans: 10, sugar: 0})
    coffee_with_milk = Item("Coffee Milk", 5, {beans: 10, milk: 2, sugar: 1})

    my_items = [black_coffee, black_coffee_no_sugar, coffee_with_milk]

    my_machine = CoffeeMachine(my_stock, my_items)
    my_machine.main_menu()