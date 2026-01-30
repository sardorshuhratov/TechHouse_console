class Customer:
	def __init__(self, id, username, email, password):
		self.id = id
		self.username = username
		self.email = email
		self.password = password
		self.membership = "BRONZE"
		self.points = 0
		self.cart = []
		self.total_spent = 0

	def add_to_cart(self, product_id, quantity):
		for item in self.cart:
			if item['product_id'] == str(product_id):
				item['quantity'] += quantity
				return
		self.cart.append({
			'product_id': str(product_id),
			'quantity': quantity
		})

	def clear_cart(self):
		self.cart = []

	def add_purchase(self, amount):
		self.total_spent += amount

	def to_dict(self):
		return {
			"id": self.id,
			"username": self.username,
			"email": self.email,
			"password": self.password,
			"membership": self.membership,
			"points": self.points,
			"cart": self.cart,
			"total_spent": self.total_spent
		}