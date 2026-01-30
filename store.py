import json
import os
import time
from datetime import datetime
from product import Product
from customer import Customer

class TechStore:
    def __init__(self):
        self.products = []
        self.customers = []
        self.current_user = None
        self.load_data()

    def print_line(self):
        print("-" * 60)

    def simple_loading(self, text):
        print(f"\n⏳ {text}...")
        time.sleep(0.9)

    def support_menu(self):
        self.print_line()
        print("ALOQA / SUPPORT")
        self.print_line()
        print("📞 Telefon: +998 97 552 40 50")
        print("📧 Email: info@techhouse.uz")
        print("📍 Manzil: Toshkent sh., Amir Temur ko'chasi 123")
        print("🕐 Ish vaqti: Dushanba - Shanba 08:00 - 20:00")
        self.print_line()

        print("1. Supportga xabar qoldirish")
        print("0. Orqaga")
        ch = self.get_int_input(">>> ", 0, 1)
        if ch == 0:
            return

        msg = input("Xabaringiz: ").strip()
        if not msg:
            print("⚠️ Xabar bo'sh bo'lmasin!")
            return

        if not os.path.exists("data"):
            os.makedirs("data")

        path = "data/support_requests.json"
        data = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except:
                    data = []

        username = self.current_user.username if self.current_user else "Mehmon"
        data.append({"user": username, "message": msg, "date": "28.01.2026 / 11:53"})

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.simple_loading("Xabar yuborilmoqda")
        print("✅ Xabaringiz qabul qilindi! Tez orada javob beriladi.")
        print("0. Orqaga\n")
        self.get_int_input(">>> ", 0, 0)

    def get_int_input(self, prompt, min_val=None, max_val=None):
        while True:
            val_str = input(prompt).strip()
            if not val_str:
                print("⚠️ Iltimos, raqam tanlang!")
                continue
            try:
                value = int(val_str)
                if min_val is not None and value < min_val:
                    print(f"⚠️ {min_val} dan kichik bo'lmasin!")
                    continue
                if max_val is not None and value > max_val:
                    print(f"⚠️ {max_val} dan katta bo'lmasin!")
                    continue
                return value
            except ValueError:
                print("⚠️ Faqat raqam kiriting!")

    def calculate_discount(self, total_amount, membership):
        rates = {
            "SILVER": 0.03,  # 3%
            "GOLD": 0.05,  # 5%
            "BIZNES": 0.10  # 10%
        }

        percent = rates.get(membership, 0)
        return int(total_amount * percent)

    def load_data(self):
        if os.path.exists("data/products.json"):
            try:
                with open("data/products.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.products = [
                        Product(i['id'], i['name'], i['price'], i['category'], i['stock'], i.get('description', '')) for
                        i in data]
            except:
                self.products = []

        if os.path.exists("data/customers.json"):
            try:
                with open("data/customers.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for i in data:
                        u_name = i.get('username', i.get('name', 'User'))
                        cust = Customer(i['id'], u_name, i['email'], i['password'])
                        cust.membership = i.get('membership', 'BRONZE')
                        cust.points = i.get('points', 0)
                        cust.cart = i.get('cart', [])
                        self.customers.append(cust)
            except:
                self.customers = []

    def save_customers(self):
        if not os.path.exists("data"): os.makedirs("data")
        data = [c.to_dict() for c in self.customers]
        with open("data/customers.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_order(self, total, final, delivery_type, delivery_info=None):
        orders = []
        path = "data/orders.json"

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    orders = json.load(f)
            except:
                orders = []

        # items: kim nima oldi, nechta oldi
        items = []
        for item in self.current_user.cart:
            prod = next((p for p in self.products if p.id == item['product_id']), None)
            if prod:
                items.append({
                    "product_id": prod.id,
                    "name": prod.name,
                    "qty": item["quantity"],
                    "unit_price": prod.price
                })

        new_order = {
            "username": self.current_user.username,
            "items": items,
            "original_price": total,
            "final_paid": final,
            "delivery": "Kuryer" if delivery_type == 1 else "Olib ketish",
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_info": delivery_info or {}
        }

        orders.append(new_order)

        if not os.path.exists("data"):
            os.makedirs("data")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(orders, f, indent=2, ensure_ascii=False)

    def login(self):
        print("\n==== KIRISH ====\n")
        user_input = input("Username: ").strip()
        pass_input = input("Parol: ").strip()

        self.simple_loading("Tekshirilmoqda")
        for user in self.customers:
            if user.username == user_input and user.password == pass_input:
                self.current_user = user
                print(f"Tizimga muvaffaqiyatli kirildi!")
                return True
        print("❌ Xato login yoki parol!")
        return False

    def register(self):
        print("\n==== RO'YXATDAN O'TISH ====\n")
        username = input("Yangi Username: ").strip()
        for c in self.customers:
            if c.username == username:
                print("❌ Bunday foydalanuvchi mavjud!")
                return
        email = input("Email: ")
        password = input("Parol: ")

        self.simple_loading("Saqlanmoqda")
        new_id = f"C{len(self.customers) + 1:03d}"
        new_user = Customer(new_id, username, email, password)
        self.customers.append(new_user)
        self.save_customers()
        print("✅ Ro'yxatdan o'tdingiz!")

    def admin_login(self):
        self.print_line()
        print("ADMIN KIRISH")
        self.print_line()
        u = input("Admin username: ").strip()
        p = input("Admin parol: ").strip()

        # xohlasangiz keyin json orqali ham qilamiz
        if u == "admin" and p == "admin123":
            print("✅ Admin panelga kirdingiz.")
            return True

        print("❌ Login yoki parol xato!")
        return False

    def admin_panel(self):
        while True:
            self.print_line()
            print("ADMIN PANEL")
            self.print_line()
            print("1. Buyurtmalar tarixi")
            print("2. Tovar qoldig'i (Stock)")
            print("0. Orqaga")

            ch = self.get_int_input(">>> ", 0, 2)
            if ch == 0:
                return
            elif ch == 1:
                self.admin_view_orders()
            elif ch == 2:
                self.admin_view_stock()

    def admin_view_orders(self):
        path = "data/orders.json"
        if not os.path.exists(path):
            print("⚠️ Hali buyurtmalar yo'q!")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                orders = json.load(f)
        except:
            print("⚠️ orders.json o‘qilmadi!")
            return

        if not orders:
            print("⚠️ Hali buyurtmalar yo'q!")
            return

        for i, o in enumerate(orders, 1):
            self.print_line()
            print(f"{i}) User: {o.get('username', '-')}")
            print(f"   Sana/soat: {o.get('datetime', o.get('date', '-'))}")
            print(f"   Yetkazish: {o.get('delivery', '-')}")

            paid = o.get("final_paid", 0)
            try:
                print(f"   To'lov: {int(paid):,} so'm")
            except:
                print(f"   To'lov: {paid}")

            info = o.get("delivery_info", {})
            if info:
                print(f"   Manzil: {info.get('viloyat', '-')}, {info.get('tuman', '-')}, {info.get('manzil', '-')}")
                print(f"   Telefon: {info.get('telefon', '-')}")

            print("   Xaridlar:")
            items = o.get("items", [])
            # eski orders.json (items string) va yangi (dict) ikkisini ham ko‘rsatadi
            for it in items:
                if isinstance(it, str):
                    print(f"    - {it}")
                else:
                    print(f"    - {it.get('name', '-')} x{it.get('qty', 0)}")

    def admin_view_stock(self):
        self.print_line()
        print("TOVAR QOLDIG'I (STOCK)")
        self.print_line()
        print(f"{'ID':<6} {'Nom':<28} {'Kategoriya':<18} {'Stock':<6}")
        self.print_line()

        for p in self.products:
            stock = getattr(p, "stock", 0)
            print(f"{p.id:<6} {p.name[:28]:<28} {p.category[:18]:<18} {stock:<6}")

        self.print_line()
        print("0. Orqaga")
        self.get_int_input(">>> ", 0, 0)

    def run_app(self):
        while True:
            self.print_line()
            print("   TECH HOUSE - maishiy texnika dokoni")
            self.print_line()
            print("1. Kirish")
            print("2. Ro'yxatdan o'tish")
            print("3. Aloqa / Support")
            print("4. Admin panel")
            print("0. Chiqish")

            choice = self.get_int_input("\n>>> Tanlang: ", 0, 4)
            if choice == 0:
                print("\nXayr👋, dokonimizda korganimizdan xursandmiz!\n\n")
                break
            elif choice == 1:
                if self.login(): self.customer_menu()
            elif choice == 2:
                self.register()
            elif choice == 3:
                self.support_menu()
            elif choice == 4:
                if self.admin_login():
                    self.admin_panel()

    def customer_menu(self):
        while True:
            u = self.current_user
            self.print_line()
            print(f"Xush kelibsz {u.username}\nTechHouse - maishiy texnika dokoni")
            self.print_line()
            print("1. Mahsulotlar")
            print("2. Qidiruv")
            print("3. Savatcha")
            print("4. Profil")
            print("5. Aloqa / Support")
            print("0. Chiqish")

            choice = self.get_int_input("\n>>> Tanlang: ", 0, 5)
            if choice == 0:
                self.current_user = None
                break
            elif choice == 1:
                self.shop_cycle()
            elif choice == 2:
                self.search_interface()
            elif choice == 3:
                self.show_cart()
            elif choice == 4:
                self.print_line()
                print("Xush kelibsz shaxsiy profilga")
                self.print_line()
                print(f"User: {u.username}\nEmail: {u.email}\nPassword: {u.password}\nA'zolik: {u.membership}\nBallaringiz: {u.points}")
                print("\n0. Orqaga")
                self.get_int_input(">>> ", 0, 0)
            elif choice == 5:
                self.support_menu()

    def add_to_cart_logic(self, product_id):
        product = next((p for p in self.products if p.id == str(product_id)), None)
        if not product:
            print("⚠️ Bunday ID yo'q!")
            return False

        print(f"\nTanlandi: {product.name} | {product.price:,} so'm")
        qty = self.get_int_input(f"Nechta olasiz? : ", 1, 100)

        self.current_user.add_to_cart(product.id, qty)
        self.simple_loading("✅ Savatga tushmoqda!")
        print("Savatcha bolimidan korishingiz mumkin\n")
        return True

    def shop_cycle(self):
        while True:
            self.print_line()
            print("KATALOGLAR:")
            categories = sorted(list(set([p.category for p in self.products])))
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            print("0. Asosiy Menyu")

            cat_choice = self.get_int_input("\n>>> Tanlang: ", 0, len(categories))
            if cat_choice == 0: break

            selected_cat = categories[cat_choice - 1]

            while True:
                self.print_line()
                print(f"BO'LIM: {selected_cat.upper()}")

                filtered = [p for p in self.products if p.category == selected_cat]
                print(f"{'ID:':<6} {'Nom':<30} {'Narx':<15}")
                for p in filtered:
                    print(f"{p.id:<6} {p.name:<30} {p.price:,} so'm")
                self.print_line()

                print("1. Savatga qo'shish")
                print("2. Boshqa katalogga o'tish")
                print("0. Asosiy Menyu")

                action = self.get_int_input("\n>>> ", 0, 2)

                if action == 0:
                    return
                elif action == 2:
                    break
                elif action == 1:
                    pid = input(">>> ID kiriting: ").strip()
                    if self.add_to_cart_logic(pid):
                        self.save_customers()

                        print("1. Yana shu bo'limdan xarid qilish")
                        print("2. Boshqa katalogga o'tish")
                        print("0. Asosiy menyuga qaytish")

                        next_step = self.get_int_input("\n>>> ", 0, 2)

                        if next_step == 1:
                            continue
                        elif next_step == 2:
                            break
                        elif next_step == 0:
                            return

    def search_interface(self):
        while True:
            self.print_line()
            print("QIDIRUV TIZIMI")
            categories = sorted(list(set([p.category for p in self.products])))
            print("Bo'limlar: " + ", ".join(categories))

            keyword = input("\nQidirish (0-chiqish): ").strip().lower()
            if keyword == '0' or not keyword: return

            found = [p for p in self.products if keyword in p.name.lower() or keyword in p.category.lower()]

            if found:
                while True:
                    self.print_line()
                    print(f"Topildi {len(found)} ta:")
                    print(f"Qidiruv natijalari:\n")
                    for p in found:
                        print(f"{p.id:<6} {p.name:<30} {p.price:,} so'm")
                    self.print_line()

                    print("\n1. Savatga joylash")
                    print("2. Yangi qidiruv")
                    print("0. Orqaga")

                    ch = self.get_int_input(">>> ", 0, 2)
                    if ch == 0:
                        return
                    elif ch == 2:
                        break
                    elif ch == 1:
                        pid = input(">>> ID kiriting: ").strip()
                        if self.add_to_cart_logic(pid):
                            self.save_customers()
                            print("1. Yana shu ro'yxatdan tanlash")
                            print("2. Yangi qidiruv")
                            print("0. Asosiy menyu")

                            ns = self.get_int_input(">>> ", 0, 2)
                            if ns == 1:
                                continue
                            elif ns == 2:
                                break
                            elif ns == 0:
                                return
            else:
                print("❌ Topilmadi.")
                print("0. Orqaga")
                self.get_int_input(">>> ", 0, 0)

    def show_cart(self):
        while True:
            self.print_line()
            print("SAVATCHA")
            u = self.current_user

            if not u.cart:
                print("Savat bo'sh!")
                print("0. Orqaga")
                self.get_int_input(">>> ", 0, 0)
                return

            total = 0
            for item in u.cart:
                prod = next((p for p in self.products if p.id == item['product_id']), None)
                if prod:
                    s = prod.price * item['quantity']
                    total += s
                    print(f"{prod.name:<30} x {item['quantity']} = {s:,} so'm")

            disc = self.calculate_discount(total, u.membership)
            final = total - disc

            self.print_line()
            print(f"JAMI: {total:,} so'm")

            if disc > 0:
                print(f"Chegirma ({u.membership}): -{disc:,} so'm")

            print(f"TO'LOVGA: {final:,} so'm")

            print("\n1. Buyurtma berish")
            print("2. Savatni tozalash")
            print("0. Orqaga")

            ch = self.get_int_input(">>> ", 0, 2)
            if ch == 0:
                break
            elif ch == 2:
                u.clear_cart()
                self.save_customers()
                print("Tozalandi!")
            elif ch == 1:
                print("\n1. Kuryer")
                print("2. Olib ketish")
                d = self.get_int_input(">>> ", 1, 2)
                delivery_info = {}
                if d == 1:
                    self.print_line()
                    print("  Yetkazib berish ma'lumotlari")
                    self.print_line()
                    viloyat = input("\nViloyatingizni kiriting: ").strip()
                    tuman = input("Tuman yoki shahringizni kiriting: ").strip()
                    telefon = input("Telefon raqamingiz: ").strip()
                    delivery_info = {
                        "viloyat": viloyat,
                        "tuman": tuman,
                        "telefon": telefon
                    }
                self.simple_loading("Buyurtma qabul qilinmoqda")
                self.simple_loading("Buyurtma sizga yuborilmoqda")

                points = int(final / 100000)
                u.points += points

                if u.points >= 100:
                    u.membership = "BIZNES"
                elif u.points >= 50:
                    u.membership = "GOLD"
                elif u.points >= 20:
                    u.membership = "SILVER"

                self.save_order(total, final, d, delivery_info)
                u.clear_cart()
                self.save_customers()

                print("\nO`z tuman yoki shahringizdagi topshirish punkitlaridan olib ketishingiz mumkin!")
                print(f"Xaridingiz uchun rahmat! Sizga {points} ball berildi.")
                print("\n0. Asosiy Menyu")
                self.get_int_input(">>> ", 0, 0)
                return