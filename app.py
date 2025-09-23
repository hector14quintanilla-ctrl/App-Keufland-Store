import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json


class ProductDatabase:
    def __init__(self):
        # base de datos productos simulada
        self.products = {
            "001": {"name": "Coca Cola 355ml", "price": 15.50, "stock": 50},
            "002": {"name": "Sabritas Original", "price": 18.00, "stock": 30},
            "003": {"name": "Pan Bimbo", "price": 32.00, "stock": 25},
            "004": {"name": "Leche Lala 1L", "price": 28.50, "stock": 20},
            "005": {"name": "Agua Bonafont 600ml", "price": 12.00, "stock": 40},
            "006": {"name": "Cigarros Marlboro", "price": 85.00, "stock": 15},
            "007": {"name": "Café Nescafé", "price": 45.50, "stock": 18},
            "008": {"name": "Chicles Trident", "price": 8.50, "stock": 60},
            "009": {"name": "Cerveza Corona", "price": 25.00, "stock": 35},
            "010": {"name": "Galletas Oreo", "price": 22.00, "stock": 28}
        }

    def get_product(self, code):
        return self.products.get(code)

    def update_stock(self, code, quantity):
        if code in self.products:
            self.products[code]["stock"] -= quantity


class POSSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Punto de Venta")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.db = ProductDatabase()
        self.cart = []
        self.total = 0.0

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        title_label = tk.Label(main_frame, text="Kuefland Store System",
                               font=("Arial", 16), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=10)

        # Frame superior para entrada de productos
        input_frame = tk.Frame(main_frame, bg="#ffffff",
                               relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X, pady=5)

        # Entrada de ID del producot
        tk.Label(input_frame, text="ID de Producto:", font=("Arial", 10, "bold"),
                 bg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.product_code_var = tk.StringVar()
        self.product_entry = tk.Entry(input_frame, textvariable=self.product_code_var,
                                      font=("Arial", 12), width=15)
        self.product_entry.grid(row=0, column=1, padx=10, pady=10)
        self.product_entry.bind("<Return>", self.scan_product)

        # Cantidad
        tk.Label(input_frame, text="Cantidad:", font=("Arial", 10, "bold"),
                 bg="#ffffff").grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = tk.Entry(input_frame, textvariable=self.quantity_var,
                                  font=("Arial", 12), width=5)
        quantity_entry.grid(row=0, column=3, padx=10, pady=10)

        # Botón agregar
        add_btn = tk.Button(input_frame, text="Agregar", command=self.scan_product,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                            relief=tk.RAISED, bd=2)
        add_btn.grid(row=0, column=4, padx=10, pady=10)

        # Botón Eliminar Articulo
        delete_btn = tk.Button(input_frame, text="Eliminar Articulo", command=self.delete_item,
                               bg="#ff0000", fg="white", font=("Arial", 10, "bold"))
        delete_btn.grid(row=0, column=5, padx=10, pady=10)

        # Frame para la lista de productos
        list_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Tabla de productos en el carrito
        columns = ("ID", "Producto", "Cantidad",
                   "Precio Unit.", "Subtotal")
        self.cart_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120, anchor="center")

        self.cart_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)

        # Frame inferior para totales y botones
        bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
        bottom_frame.pack(fill=tk.X, pady=5)

        # Total
        total_frame = tk.Frame(
            bottom_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        total_frame.pack(fill=tk.X, pady=5)

        self.total_label = tk.Label(total_frame, text="Total a pagar: $0.00",
                                    font=("Arial", 18, "bold"), bg="#ffffff", fg="#000000")
        self.total_label.pack(pady=15)

        # Botones de acción
        buttons_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=5)

        # Botón limpiar todo
        clear_btn = tk.Button(buttons_frame, text="Eliminar todo", command=self.clear_cart,
                              bg="#ff0000", fg="white", font=("Arial", 10, "bold"),
                              relief=tk.RAISED, bd=2)
        clear_btn.pack(side=tk.LEFT, padx=5)
        # Botón pagar con terminal
        pay_btn = tk.Button(buttons_frame, text="Pagar con terminal", command=self.process_payment_card,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        pay_btn.pack(side=tk.RIGHT, padx=5)

        # Botón cobrar
        pay_btn = tk.Button(buttons_frame, text="Pagar con efectivo", command=self.process_payment,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                            relief=tk.RAISED, bd=2, width=13)
        pay_btn.pack(side=tk.RIGHT, padx=5)

        # Focus en el campo de entrada
        self.product_entry.focus_set()

    def scan_product(self, event=None):
        code = self.product_code_var.get().strip()
        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror(
                "Error", "La cantidad debe ser un número válido")
            return

        if not code:
            messagebox.showerror("Error", "Ingrese el ID de producto")
            return

        product = self.db.get_product(code)
        if not product:
            messagebox.showerror(
                "Error", f"Producto con ID {code} no encontrado")
            return

        if product["stock"] < quantity:
            messagebox.showerror(
                "Error", f"Stock insuficiente. Disponible: {product['stock']}")
            return

        # Agregar al carrito
        subtotal = product["price"] * quantity
        self.cart.append({
            "code": code,
            "name": product["name"],
            "quantity": quantity,
            "price": product["price"],
            "subtotal": subtotal
        })

        # Actualizar stock
        self.db.update_stock(code, quantity)

        # Actualizar interfaz
        self.update_cart_display()
        self.calculate_total()

        # Limpiar campos
        self.product_code_var.set("")
        self.quantity_var.set("1")
        self.product_entry.focus_set()

    def update_cart_display(self):
        # Limpiar tabla
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        # Agregar items del carrito
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(
                item["code"],
                item["name"],
                item["quantity"],
                f"${item['price']:.2f}",
                f"${item['subtotal']:.2f}"
            ))

    def calculate_total(self):
        self.total = sum(item["subtotal"] for item in self.cart)
        self.total_label.config(text=f"TOTAL: ${self.total:.2f}")

    def delete_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Advertencia", "Seleccione un producto para eliminar")
            return

        item_index = self.cart_tree.index(selected[0])
        removed_item = self.cart.pop(item_index)

        # Restaurar stock
        self.db.products[removed_item["code"]
                         ]["stock"] += removed_item["quantity"]

        self.update_cart_display()
        self.calculate_total()

    def clear_cart(self):
        if not self.cart:
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de limpiar todo el carrito?"):
            # Restaurar stock de todos los productos
            for item in self.cart:
                self.db.products[item["code"]]["stock"] += item["quantity"]

            self.cart.clear()
            self.update_cart_display()
            self.calculate_total()

    def process_payment_card(self):
        if not self.cart:
            messagebox.showwarning("Advertencia", "Carrito está vacío")
            return

        payment_window = tk.Toplevel(self.root)
        payment_window.title("Procesar Pago con Tarjeta")
        payment_window.geometry("400x200")
        payment_window.configure(bg="#f0f0f0")
        payment_window.transient(self.root)
        payment_window.grab_set()

        tk.Button(payment_window, text="CANCELAR", command=payment_window.destroy,
                  bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side=tk.BOTTOM, pady=10)

        # Total a pagar
        tk.Label(payment_window, text=f"TOTAL A PAGAR: ${self.total:.2f}",
                 font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#000000").pack(pady=20)
        tk.Label(payment_window, text="Inserte o acerque la tarjeta",
                 font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

        if messagebox.askyesno("Confirmar Pago", "¿Confirmas el pago por terminal?"):
            self.cart.clear()
            self.update_cart_display()
            self.calculate_total()

            payment_window.destroy()
            messagebox.showinfo("Compra exitosa")

    def process_payment(self):
        if not self.cart:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return

        # Ventana de pago
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Procesar Pago")
        payment_window.geometry("400x300")
        payment_window.configure(bg="#f0f0f0")
        payment_window.transient(self.root)
        payment_window.grab_set()

        # Total a pagar
        tk.Label(payment_window, text=f"TOTAL A PAGAR: ${self.total:.2f}",
                 font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#000000").pack(pady=20)

        # Pago recibido
        tk.Label(payment_window, text="Pago recibido:",
                 font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        payment_var = tk.StringVar()
        payment_entry = tk.Entry(
            payment_window, textvariable=payment_var, font=("Arial", 12), width=20)
        payment_entry.pack(pady=5)
        payment_entry.focus_set()

        # Cambio
        change_label = tk.Label(payment_window, text="Cambio: $0.00",
                                font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#4CAF50")
        change_label.pack(pady=10)

        def calculate_change():
            try:
                payment = float(payment_var.get())
                if payment >= self.total:
                    change = payment - self.total
                    change_label.config(text=f"Cambio: ${change:.2f}")
                else:
                    change_label.config(text="Pago insuficiente", fg="#f44336")
            except ValueError:
                change_label.config(
                    text="Ingrese un monto válido", fg="#f44336")

        payment_entry.bind("<KeyRelease>", lambda e: calculate_change())

        def complete_sale():
            try:
                payment = float(payment_var.get())
                if payment < self.total:
                    messagebox.showerror("Error", "El pago es insuficiente")
                    return

                # Limpiar carrito
                self.cart.clear()
                self.update_cart_display()
                self.calculate_total()

                payment_window.destroy()
                messagebox.showinfo("Éxito", "Venta completada exitosamente")

            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")

        # Botones
        buttons_frame = tk.Frame(payment_window, bg="#f0f0f0")
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="COMPLETAR VENTA", command=complete_sale,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="CANCELAR", command=payment_window.destroy,
                  bg="#f44336", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = POSSystem(root)
    root.mainloop()
