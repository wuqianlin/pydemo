import model_v6 as model


class LineItem:
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, weight, price):
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
