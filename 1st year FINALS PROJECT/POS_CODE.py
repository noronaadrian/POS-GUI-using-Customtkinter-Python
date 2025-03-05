from customtkinter import *
from tkinter import *
from datetime import date
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog, END
from datetime import datetime
import os
import logging

window = CTk()
window.geometry("1000x600")
window.title("CATPUCCINO")
window.resizable(False, False)
set_appearance_mode("light")

window.iconbitmap()
icon = PhotoImage(file='meow6.png')
window.iconphoto(True, icon)

window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f"+{x_cordinate}+{y_cordinate}")

item_prices = {
    "macchiato": {"Tall": 145.00, "Grande": 160.00, "Venti": 175.00},
    "mocha": {"Tall": 145.00, "Grande": 160.00, "Venti": 175.00},
    "flat white": {"Tall": 145.00, "Grande": 160.00, "Venti": 175.00},
    "hazelnut latte": {"Tall": 145.00, "Grande": 160.00, "Venti": 175.00},
    "cappuccino": {"Tall": 145.00, "Grande": 160.00, "Venti": 175.00},
    "spanish latte": {"Tall": 145.00, "Grande": 160.00, "Venti": 175.00},
    "baguette": {"None": 160.00},
    "brioche": {"None": 130.00},
    "croissant": {"None": 180.00},
    "eclair": {"None": 220.00},
    "kouign": {"None": 190.00},
    "macaron": {"None": 80.00},
    "caramel": {"Tall": 175.00, "Grande": 190.00, "Venti": 205.00},
    "ube halaya": {"Tall": 175.00, "Grande": 190.00, "Venti": 205.00},
    "cookies n cream": {"Tall": 175.00, "Grande": 190.00, "Venti": 205.00},
    "strawberry": {"Tall": 175.00, "Grande": 190.00, "Venti": 205.00},
    "matcha": {"Tall": 175.00, "Grande": 190.00, "Venti": 205.00},
    "double dutch": {"Tall": 175.00, "Grande": 190.00, "Venti": 205.00},
}

coffee_quantities = {
    "macchiato": {"Tall": 0, "Grande": 0, "Venti": 0},
    "mocha": {"Tall": 0, "Grande": 0, "Venti": 0},
    "flat white": {"Tall": 0, "Grande": 0, "Venti": 0},
    "hazelnut latte": {"Tall": 0, "Grande": 0, "Venti": 0},
    "cappuccino": {"Tall": 0, "Grande": 0, "Venti": 0},
    "spanish latte": {"Tall": 0, "Grande": 0, "Venti": 0},
    "baguette": {"None": 0},
    "brioche": {"None": 0},
    "croissant": {"None": 0},
    "eclair": {"None": 0},
    "kouign": {"None": 0},
    "macaron": {"None": 0},
    "caramel": {"Tall": 0, "Grande": 0, "Venti": 0},
    "ube halaya": {"Tall": 0, "Grande": 0, "Venti": 0},
    "cookies n cream": {"Tall": 0, "Grande": 0, "Venti": 0},
    "strawberry": {"Tall": 0, "Grande": 0, "Venti": 0},
    "matcha": {"Tall": 0, "Grande": 0, "Venti": 0},
    "double dutch": {"Tall": 0, "Grande": 0, "Venti": 0},
}

pwd_discount = 0.2
pwd_active = False
selected_sugar_level = None

cash_received = 0
change = 0
payment_method_used = ""

logging.basicConfig(filename='pos_system.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

menu_bar = Menu(window)
window.config(menu=menu_bar)

version = "1.0"

def open_file():
    file_path = r"C:\Users\Administrator\Desktop\POS NAMIN\pos_system.log"
    try:
        transaction_history_window = Toplevel(window)
        transaction_history_window.title("Transaction History")
        transaction_history_window.geometry("600x400")

        transaction_history_window.update_idletasks()
        window_width = transaction_history_window.winfo_width()
        window_height = transaction_history_window.winfo_height()
        screen_width = transaction_history_window.winfo_screenwidth()
        screen_height = transaction_history_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        transaction_history_window.geometry(f"+{x_cordinate}+{y_cordinate}")

        transaction_history_window.configure(bg="#D4B37F")

        text_box = Text(transaction_history_window, wrap=WORD, font=("Helvetica", 12, "bold"), bg="#f8f8ff", fg="black")
        scroll_bar = Scrollbar(transaction_history_window, command=text_box.yview)
        text_box.configure(yscrollcommand=scroll_bar.set)

        text_box.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_bar.pack(side=RIGHT, fill=Y)

        with open(file_path, 'r') as file:
            content = file.readlines()

        formatted_content = ""
        in_receipt = False

        for line in content:
            if "--------------- RECEIPT ------------------------------" in line:
                if in_receipt:
                    formatted_content += "\n" + "-" * 100 + "\n"
                formatted_content += "\n" + "-" * 100 + "\n"
                in_receipt = True
            elif "Date:" in line:
                formatted_content += f"\n{line.strip()}\n"
            elif "Customer Name:" in line:
                formatted_content += f"{line.strip()}\n"
            elif "Item Name" in line:
                formatted_content += f"\n{line.strip()}\n"
            elif "PWD/Senior Citizen:" in line:
                formatted_content += f"\n{line.strip()}\n"
            elif "Payment Method:" in line:
                formatted_content += f"{line.strip()}\n"
            elif "Cash Received:" in line or "Change:" in line:
                formatted_content += f"{line.strip()}\n"
            elif "Total Amount:" in line:
                formatted_content += f"{line.strip()}\n"
            else:
                formatted_content += line

        if in_receipt:
            formatted_content += "\n" + "-" * 100 + "\n"

        text_box.insert(END, formatted_content)
        text_box.yview_moveto(1)

        text_box.config(state=DISABLED)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_client():
    global version
    major, minor = map(int, version.split('.'))
    minor += 1
    version = f"{major}.{minor}"
    messagebox.showinfo("Update", f"POS System v{version}")

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Transaction History", command=open_file)
file_menu.add_command(label="Save", command=lambda: messagebox.showinfo("Save", "Save clicked"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About POS System", command=lambda: messagebox.showinfo("About", f"POS System v{version}"))

more_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="More", menu=more_menu)
more_menu.add_command(label="Support", command=lambda: messagebox.showinfo("Support", "Support clicked"))
more_menu.add_command(label="Update Client", command=update_client)


def kape1():
    add_item_to_order("macchiato")


def kape2():
    add_item_to_order("mocha")


def kape3():
    add_item_to_order("flat white")


def kape4():
    add_item_to_order("hazelnut latte")


def kape5():
    add_item_to_order("cappuccino")


def kape6():
    add_item_to_order("spanish latte")


def tinapay1():
    add_item_to_order("baguette")


def tinapay2():
    add_item_to_order("brioche")


def tinapay3():
    add_item_to_order("croissant")


def tinapay4():
    add_item_to_order("eclair")


def tinapay5():
    add_item_to_order("kouign")


def tinapay6():
    add_item_to_order("macaron")


def prop1():
    add_item_to_order("caramel")


def prop2():
    add_item_to_order("ube halaya")


def prop3():
    add_item_to_order("cookies n cream")


def prop4():
    add_item_to_order("strawberry")


def prop5():
    add_item_to_order("matcha")


def prop6():
    add_item_to_order("double dutch")


def add_item_to_order(item):
    selected_size = selected_sizes[item]

    coffee_quantities[item][selected_size] += 1

    update_order_display()

    update_total_amount()

def remove_item(item):
    item_name, item_size = item.split('|')
    coffee_quantities[item_name][item_size] -= 1
    update_order_display()
    update_total_amount()

def update_order_display():
    for widget in order.winfo_children():
        widget.destroy()

    headers = ["Item", "Quantity", "", "Size", "Price"]
    for idx, header in enumerate(headers):
        header_label = CTkLabel(order, text=header, font=("Helvetica", 12, "bold"), fg_color="#D3D3D3", text_color="black")
        header_label.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")

    row_num = 1
    items_found = False
    for item, sizes in coffee_quantities.items():
        for size, quantity in sizes.items():
            if quantity > 0:
                items_found = True
                item_name_display = item.replace("_", " ").title()
                total_item_price = quantity * get_price_with_size(item, size)
                quantity_display = f"x{quantity}"
                item_label = CTkLabel(order, text=item_name_display, font=("Helvetica", 12), fg_color="#D3D3D3", text_color="black")
                quantity_label = CTkLabel(order, text=quantity_display, font=("Helvetica", 12), fg_color="#D3D3D3", text_color="black")
                size_label = CTkLabel(order, text=size, font=("Helvetica", 12), fg_color="#D3D3D3", text_color="black")
                price_label = CTkLabel(order, text=f"P{total_item_price:.2f}", font=("Helvetica", 12), fg_color="#D3D3D3", text_color="black")
                remove_button = CTkButton(order, text="X", width=3, fg_color="#D3D3D3", hover_color="#D34A24",
                                          font=("Roboto", 10, "bold"), text_color="black",
                                          command=lambda item=f"{item}|{size}": remove_item(item))

                item_label.grid(row=row_num, column=0, padx=0, pady=5, sticky="nsew")
                quantity_label.grid(row=row_num, column=1, padx=0, pady=5, sticky="nsew")
                remove_button.grid(row=row_num, column=2, padx=0, pady=0)
                size_label.grid(row=row_num, column=3, padx=0, pady=5, sticky="nsew")
                price_label.grid(row=row_num, column=4, padx=0, pady=5, sticky="nsew")

                row_num += 1

    for col in range(5):
        order.grid_columnconfigure(col, weight=1)

    if not items_found:
        messagebox.showerror("Error", "No items in the order.")

def update_total_amount():
    total_price = sum(
        quantities[size] * get_price_with_size(item, size)
        for item, quantities in coffee_quantities.items()
        for size, quantity in quantities.items() if quantity > 0
    )
    if pwd_active:
        total_price *= (1 - pwd_discount)
    total_label.configure(text=f"Total: P{total_price:.2f}")
    return total_price


def pwd():
    global pwd_active
    pwd_active = not pwd_active
    update_total_amount()
    status = "applied" if pwd_active else "removed"
    messagebox.showinfo("PWD Discount", f"PWD Discount {status}")


def void_button():
    for item in coffee_quantities:
        for size in coffee_quantities[item]:
            coffee_quantities[item][size] = 0
    update_order_display()
    update_total_amount()

sizes = ["Tall", "Grande", "Venti"]

selected_sizes = {
    "macchiato": "Tall",
    "mocha": "Tall",
    "flat white": "Tall",
    "hazelnut latte": "Tall",
    "cappuccino": "Tall",
    "spanish latte": "Tall",
    "baguette": "None",
    "brioche": "None",
    "croissant": "None",
    "eclair": "None",
    "kouign": "None",
    "macaron": "None",
    "caramel": "Tall",
    "ube halaya": "Tall",
    "cookies n cream": "Tall",
    "strawberry": "Tall",
    "matcha": "Tall",
    "double dutch": "Tall",
}


def get_price_with_size(item, size):
    return item_prices[item][size]


def update_size(item, new_size):
    selected_sizes[item] = new_size
    update_total_amount()


receipt_dir = "receipts"
if not os.path.exists(receipt_dir):
    os.makedirs(receipt_dir)


def get_next_receipt_number():
    files = os.listdir(receipt_dir)
    receipt_numbers = [int(f.split()[1].split('.')[0]) for f in files if f.startswith("receipt")]
    next_number = max(receipt_numbers, default=0) + 1
    return next_number


def receipt():
    global selected_sugar_level, cash_received, change, payment_method_used

    total_amount = update_total_amount()

    receipt_number = get_next_receipt_number()
    file_path = os.path.join(receipt_dir, f"receipt {receipt_number}.txt")

    content = (
        "----------------------------------------------------------------\n"
        "                     CATPUCCINO\n"
        "                  Near at CVSU Imus\n"
        "                    0912-5911-391\n"
        "----------------------------------------------------------------\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Customer Name: {entry.get()}\n"
        f"Sugar Level: {selected_sugar_level}\n"
        "----------------------------------------------------------------\n"
        "Item Name               Quantity      Size       Price\n"
        "----------------------------------------------------------------\n"
    )

    transaction_details = []

    for item, sizes in coffee_quantities.items():
        for size, quantity in sizes.items():
            if quantity > 0:
                item_name_display = item.replace("_", " ").title()
                total_item_price = quantity * get_price_with_size(item, size)
                quantity_display = f"x{quantity}"
                content += f"{item_name_display:<25} {quantity_display:<10} {size:<10} P{total_item_price:.2f}\n"
                transaction_details.append({
                    "item": item_name_display,
                    "quantity": quantity,
                    "size": size,
                    "price": total_item_price
                })

    content += (
        "----------------------------------------------------------------\n"
        f"Discount: {'Yes' if pwd_active else 'No'}\n"
        f"Payment Method: {payment_method_used}\n"
    )
    if payment_method_used == "Cash":
        content += f"Cash Received: P{cash_received:.2f}\n"
        content += f"Change: P{change:.2f}\n"
    content += (
        f"Total Amount: P{total_amount:.2f}\n"
        "----------------------------------------------------------------\n"
        "              THANK YOU FOR YOUR VISIT\n"
        "           We hope to see you again soon.\n"
        "----------------------------------------------------------------\n"
        "           This serves as your Official Receipt\n"
        "    Visit our Facebook Page: www.facebook.com/znn666\n"
        "----------------------------------------------------------------\n"
    )

    try:
        with open(file_path, "w") as text_file:
            text_file.write(content)
        logging.info(f"Receipt saved successfully: {file_path}")
        
        logging.info("**Transaction Details:**")
        logging.info(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"**Customer Name:** {entry.get()}")
        logging.info(f"**Sugar Level:** {selected_sugar_level}")
        for detail in transaction_details:
            logging.info(f"**Item:** {detail['item']}, **Quantity:** {detail['quantity']}, **Size:** {detail['size']}, **Price:** P{detail['price']:.2f}")
        logging.info(f"**PWD/Senior Citizen:** {'Yes' if pwd_active else 'No'}")
        logging.info(f"**Payment Method:** {payment_method_used}")
        if payment_method_used == "Cash":
            logging.info(f"**Cash Received:** P{cash_received:.2f}")
            logging.info(f"**Change:** P{change:.2f}")
        logging.info(f"**Total Amount:** P{total_amount:.2f}")
        
    except Exception as e:
        logging.error(f"Failed to save receipt: {e}")
        messagebox.showerror("Error", f"Failed to save receipt: {e}")
        return

    for item, sizes in coffee_quantities.items():
        for size in sizes:
            coffee_quantities[item][size] = 0

    update_total_amount()

    messagebox.showinfo("Checkout", "Receipt saved. Check your receipt in the files.")


def sugar_level(selected_value):
    global selected_sugar_level
    selected_sugar_level = selected_value


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username.lower() == "admin" and password.lower() == "admin":
        login_frame.destroy()
        messagebox.showinfo("Succesful", "Login Succesfully")
    else:
        messagebox.showerror("Unsuccesful", "Wrong username or password")


login_frame = CTkFrame(window, height=600, width=1000, fg_color="#D4B37F")
login_frame.pack()

image21 = Image.open("meow7.jpg")
image21 = image21.resize((500, 600), Image.LANCZOS)
login_photo = ImageTk.PhotoImage(image21)
login_image = CTkLabel(login_frame, text="", image=login_photo)
login_image.place(x=0, y=0)

username_label = CTkLabel(login_frame, text="Username", font=("Helvetica", 15, "bold"))
username_label.place(x=650, y=270)

username_entry = CTkEntry(login_frame, placeholder_text="Username", width=220, font=("Helvetica", 15, "bold"))
username_entry.place(x=650, y=300)

password_label = CTkLabel(login_frame, text="Password", font=("Helvetica", 15, "bold"))
password_label.place(x=650, y=330)

password_entry = CTkEntry(login_frame, placeholder_text="Password", show="*", width=220, font=("Helvetica", 15, "bold"))
password_entry.place(x=650, y=360)

login_button = CTkButton(login_frame, text="Login", command=login, width=220, font=("Helvetica", 15, "bold"), fg_color="black", hover_color="grey")
login_button.place(x=650, y=400)

image22 = Image.open("loginn.png")
image22 = image22.resize((120, 120), Image.LANCZOS)
login_photo1 = ImageTk.PhotoImage(image22)
login_image1 = CTkLabel(login_frame, text="", image=login_photo1)
login_image1.place(x=700, y=130)

main_frame = CTkFrame(window, height=600, width=1000, fg_color="#f8f8ff")
main_frame.pack()

order = CTkScrollableFrame(main_frame, width=320, height=320, fg_color="#D3D3D3")
order.place(x=650, y=87)


item_order = CTkLabel(order, text="")
item_order.grid(row=2, column=1)

quantity_order = CTkLabel(order, text="")
quantity_order.grid(row=2, column=2)

size_order = CTkLabel(order, text="")
size_order.grid(row=2, column=3)

price_order = CTkLabel(order, text="")
price_order.grid(row=2, column=4)

my_tab = CTkTabview(main_frame, width=610, height=500, anchor="nw", fg_color="#D4B37F", segmented_button_fg_color="#A3866A", segmented_button_selected_color="#BD9A7A",
                    text_color="black", segmented_button_selected_hover_color="light grey", segmented_button_unselected_color="#A3866A")
my_tab.place(x=30, y=70)

tab1 = my_tab.add("Hot Coffee")
tab3 = my_tab.add("Frappe")
tab2 = my_tab.add("Bread & Pastries")

total_label = CTkLabel(main_frame, text="Total: 0.00", font=("Helvetica", 15, "bold"))
total_label.place(x=660, y=420)

label2 = CTkLabel(main_frame, text="Current Order", font=("Helvetica", 30, "bold"))
label2.place(x=700, y=50)

price_list2 = CTkFrame(tab3, height=60, width=600, corner_radius=15, fg_color="#6F4E37")
price_list2.place(x=0, y=380)

price4 = CTkLabel(price_list2, text="Price List", font=("Helvetica", 15, "bold"))
price4.place(x=10, y=5)

price5 = CTkLabel(price_list2, text="Tall: P175", font=("Helvetica", 15, "bold"))
price5.place(x=10, y=30)

price6 = CTkLabel(price_list2, text="Grande: P190", font=("Helvetica", 15, "bold"))
price6.place(x=100, y=30)

price7 = CTkLabel(price_list2, text="Venti: P205", font=("Helvetica", 15, "bold"))
price7.place(x=220, y=30)

price_list = CTkFrame(tab1, height=60, width=600, corner_radius=15, fg_color="#6F4E37")
price_list.place(x=0, y=380)

price1 = CTkLabel(price_list, text="Price List", font=("Helvetica", 15, "bold"))
price1.place(x=10, y=5)

price2 = CTkLabel(price_list, text="Tall: P145", font=("Helvetica", 15, "bold"))
price2.place(x=10, y=30)

price3 = CTkLabel(price_list, text="Grande: P160", font=("Helvetica", 15, "bold"))
price3.place(x=100, y=30)

price8 = CTkLabel(price_list, text="Venti: P175", font=("Helvetica", 15, "bold"))
price8.place(x=220, y=30)

image1 = Image.open('COFFEE2/cafe.png')
image1 = image1.resize((80, 80), Image.LANCZOS)
americano = ImageTk.PhotoImage(image1)
coffee1 = CTkButton(tab1, command=kape1, border_color="black", border_width=2, image=americano, text="Macchiato\n", width=130, height=120, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
coffee1.place(x=30, y=25)

size1 = CTkSegmentedButton(tab1, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size1.place(x=30, y=151)
size1.configure(command=lambda size: update_size("macchiato", size))

image2 = Image.open('COFFEE2/espresso.png')
image2 = image2.resize((80, 80), Image.LANCZOS)
cafe = ImageTk.PhotoImage(image2)
coffee2 = CTkButton(tab1, command=kape2, image=cafe, border_color="black", border_width=2, text="Mocha\n", width=130, height=120, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
coffee2.place(x=230, y=25)

size2 = CTkSegmentedButton(tab1, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size2.place(x=230, y=151)
size2.configure(command=lambda size: update_size("mocha", size))

image3 = Image.open('COFFEE2/cappuccino.png')
image3 = image3.resize((80, 80), Image.LANCZOS)
cappuccino = ImageTk.PhotoImage(image3)
coffee3 = CTkButton(tab1, command=kape3, border_color="black", border_width=2, image=cappuccino, text="Flat White\n", width=130, height=120, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
coffee3.place(x=430, y=25)

size3 = CTkSegmentedButton(tab1, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size3.place(x=430, y=151)
size3.configure(command=lambda size: update_size("flat white", size))

image4 = Image.open('COFFEE2/americano.png')
image4 = image4.resize((80, 80), Image.LANCZOS)
espresso = ImageTk.PhotoImage(image4)
coffee4 = CTkButton(tab1, command=kape4, border_color="black", border_width=2, image=espresso, text="Hazelnut Latte\n", width=130, height=120, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
coffee4.place(x=30, y=220)

size4 = CTkSegmentedButton(tab1, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size4.place(x=30, y=345)
size4.configure(command=lambda size: update_size("hazelnut latte", size))

image5 = Image.open('COFFEE2/frappuccino.png')
image5 = image5.resize((80, 80), Image.LANCZOS)
frappuccino = ImageTk.PhotoImage(image5)
coffee5 = CTkButton(tab1, command=kape5, border_color="black", border_width=2, image=frappuccino, text="Cappuccino\n", width=130, height=120, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
coffee5.place(x=230, y=220)

size5 = CTkSegmentedButton(tab1, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size5.place(x=230, y=345)
size5.configure(command=lambda size: update_size("cappuccino", size))

image6 = Image.open('COFFEE2/macchiato.png')
image6 = image6.resize((80, 80), Image.LANCZOS)
macchiato = ImageTk.PhotoImage(image6)
coffee6 = CTkButton(tab1, command=kape6, border_color="black", border_width=2, image=macchiato, text="Spanish Latte\n", width=130, height=120, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
coffee6.place(x=430, y=220)

size6 = CTkSegmentedButton(tab1, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size6.place(x=430, y=345)
size6.configure(command=lambda size: update_size("spanish latte", size))

image7 = Image.open('PASTRY/baguette.png')
image7 = image7.resize((80, 80), Image.LANCZOS)
baguette = ImageTk.PhotoImage(image7)
pastry1 = CTkButton(tab2, command=tinapay1, border_color="black", border_width=2, image=baguette, text="Baguette\n  P160.00", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
pastry1.place(x=30, y=25)

image8 = Image.open('PASTRY/brioche.png')
image8 = image8.resize((80, 80), Image.LANCZOS)
brioche = ImageTk.PhotoImage(image8)
pastry2 = CTkButton(tab2, command=tinapay2, border_color="black", border_width=2, image=brioche, text="Brioche\nP130.00", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
pastry2.place(x=230, y=25)

image9 = Image.open('PASTRY/croissant.png')
image9 = image9.resize((80, 80), Image.LANCZOS)
crossaint = ImageTk.PhotoImage(image9)
pastry3 = CTkButton(tab2, command=tinapay3, image=crossaint, border_color="black", border_width=2, text="Crossaint\nP180.00", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
pastry3.place(x=430, y=25)

image10 = Image.open('PASTRY/eclair.png')
image10 = image10.resize((80, 80), Image.LANCZOS)
eclair = ImageTk.PhotoImage(image10)
pastry4 = CTkButton(tab2, command=tinapay4, image=eclair, border_color="black", border_width=2, text="Éclair\nP 220.00", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
pastry4.place(x=30, y=220)

image11 = Image.open('PASTRY/kouign.png')
image11 = image11.resize((80, 80), Image.LANCZOS)
kougin = ImageTk.PhotoImage(image11)
pastry5 = CTkButton(tab2, command=tinapay5, image=kougin, border_color="black", border_width=2, text="Kouign Amann\n   P190.00", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
pastry5.place(x=230, y=220)

image12 = Image.open('PASTRY/macaron.png')
image12 = image12.resize((80, 80), Image.LANCZOS)
macaron = ImageTk.PhotoImage(image12)
pastry6 = CTkButton(tab2, command=tinapay6, image=macaron, border_color="black", border_width=2, text="Macaron\n P80.00", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
pastry6.place(x=430, y=220)

image15 = Image.open('FRAPPED/frap1.png')
image15 = image15.resize((50, 70), Image.LANCZOS)
frapp1 = ImageTk.PhotoImage(image15)
prap1 = CTkButton(tab3, command=prop1, image=frapp1, border_color="black", border_width=2, text="Caramel\n", width=130, height=140, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
prap1.place(x=30, y=25)

size7 = CTkSegmentedButton(tab3, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size7.place(x=30, y=151)
size7.configure(command=lambda size: update_size("caramel", size))

image16 = Image.open('FRAPPED/frap2.png')
image16 = image16.resize((50, 70), Image.LANCZOS)
frapp2 = ImageTk.PhotoImage(image16)
prap2 = CTkButton(tab3, command=prop2, image=frapp2, border_color="black", border_width=2, text="Ube Halaya \n", width=130, height=130, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
prap2.place(x=230, y=25)

size8 = CTkSegmentedButton(tab3, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size8.place(x=230, y=151)
size8.configure(command=lambda size: update_size("ube halaya", size))

image17 = Image.open('FRAPPED/frap3.png')
image17 = image17.resize((50, 70), Image.LANCZOS)
frapp3 = ImageTk.PhotoImage(image17)
prap3 = CTkButton(tab3, command=prop3, image=frapp3, border_color="black", border_width=2, text="Cookies 'n Cream\n", width=130, height=130, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
prap3.place(x=430, y=25)

size9 = CTkSegmentedButton(tab3, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size9.place(x=430, y=151)
size9.configure(command=lambda size: update_size("cookies n cream", size))

image18 = Image.open('FRAPPED/frap4.png')
image18 = image18.resize((50, 70), Image.LANCZOS)
frapp4 = ImageTk.PhotoImage(image18)
prap4 = CTkButton(tab3, command=prop4, image=frapp4, border_color="black", border_width=2, text="Strawberry\n", width=130, height=130, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
prap4.place(x=30, y=220)

size10 = CTkSegmentedButton(tab3, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size10.place(x=30, y=345)
size10.configure(command=lambda size: update_size("strawberry", size))

image19 = Image.open('FRAPPED/frap5.png')
image19 = image19.resize((50, 70), Image.LANCZOS)
frapp5 = ImageTk.PhotoImage(image19)
prap5 = CTkButton(tab3, command=prop5, image=frapp5, border_color="black", border_width=2, text="Matcha\n", width=130, height=130, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
prap5.place(x=230, y=220)

size11 = CTkSegmentedButton(tab3, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size11.place(x=230, y=345)
size11.configure(command=lambda size: update_size("matcha", size))

image20 = Image.open('FRAPPED/frap6.png')
image20 = image20.resize((50, 70), Image.LANCZOS)
frapp6 = ImageTk.PhotoImage(image20)
prap6 = CTkButton(tab3, command=prop6, image=frapp6, border_color="black", border_width=2, text="Double Dutch\n", width=130, height=130, compound=TOP, fg_color="white", hover_color="grey", cursor="plus", font=("Helvetica", 12, "bold"), text_color="black")
prap6.place(x=430, y=220)

size12 = CTkSegmentedButton(tab3, values=sizes, fg_color="#987654", selected_hover_color="#664c28", selected_color="#664c28", unselected_color="#987654", text_color="black", font=("Helvetica", 12, "bold"))
size12.place(x=430, y=345)
size12.configure(command=lambda size: update_size("double dutch", size))

void = CTkButton(main_frame, text="Void", command=void_button, hover_color="#d2691e", fg_color="#D4B37F", text_color="black", font=("Helvetica", 12, "bold"))
void.place(x=660, y=540)

receipt_button = CTkButton(main_frame, command=receipt, text="Check out", fg_color="#D4B37F", text_color="black", font=("Helvetica", 12, "bold"), hover_color="#d2691e")
receipt_button.place(x=660, y=500)

optionmenu_var = StringVar(value="Sugar Level")
sugar_percent = ["50%", "75%", "100%"]
sugar = CTkOptionMenu(main_frame, variable=optionmenu_var, values=sugar_percent, fg_color="#D4B37F", text_color="black", font=("Helvetica", 12, "bold"), button_color="brown", button_hover_color="#d2691e", command=sugar_level)
sugar.place(x=820, y=540)

customer_name = CTkLabel(main_frame, text="Customer name:", font=("Helvetica", 15, "bold"))
customer_name.place(x=660, y=455)

entry = CTkEntry(main_frame, font=("Helvetica", 12, "bold"), height=10, width=180)
entry.place(x=780, y=460)

pwd_button = CTkButton(main_frame, text="PWD/Senior Citizen", font=("Helvetica", 13, "bold"),
                       fg_color="#D4B37F", text_color="black", hover_color="#d2691e",
                       command=pwd)
pwd_button.place(x=820, y=500)


def payment_method():
    # Check if there are any items in the order
    items_found = False
    for sizes in coffee_quantities.values():
        if any(quantity > 0 for quantity in sizes.values()):
            items_found = True
            break
    
    if not items_found:
        messagebox.showerror("Error", "No items in the order.")
        return

    payment_selection_window = Toplevel(window)
    payment_selection_window.title("Select Payment Method")
    payment_selection_window.configure(bg="#D4B37F")
    
    payment_selection_window.update_idletasks()
    window_width = payment_selection_window.winfo_width()
    window_height = payment_selection_window.winfo_height()
    screen_width = payment_selection_window.winfo_screenwidth()
    screen_height = payment_selection_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    payment_selection_window.geometry(f"+{x_cordinate}+{y_cordinate}")
    
    Label(payment_selection_window, text="Select Payment Method", font=("Helvetica", 16, "bold"), width=20, bg="#D4B37F").pack(pady=20)
    Button(payment_selection_window, text="Cash", background="#D4B37F", font=("Helvetica", 12, "bold"), command=lambda: open_cash_payment_window(payment_selection_window), width=20, height=2).pack(pady=10)
    Button(payment_selection_window, text="Card/GCash", background="#D4B37F", font=("Helvetica", 12, "bold"), command=lambda: open_gcash_payment_window(payment_selection_window), width=20, height=2).pack(pady=10)

def open_cash_payment_window(parent_window):
    parent_window.destroy()

    def add_digit(digit):
        current = amount_tendered_entry.get()
        amount_tendered_entry.delete(0, END)
        amount_tendered_entry.insert(0, current + digit)

    def clear_entry():
        amount_tendered_entry.delete(0, END)

    def process_payment():
        global cash_received, change, payment_method_used
        payment_method_used = "Cash"
        try:
            cash_received = float(amount_tendered_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
        total_amount = update_total_amount()
        if cash_received < total_amount:
            messagebox.showerror("Error", "Cash received is less than total amount.")
            return
        change = cash_received - total_amount
        messagebox.showinfo("Change", f"Change: ₱{change:.2f}")
        complete_payment(payment_window)

    payment_window = Toplevel(window)
    payment_window.title("Cash Payment")
    payment_window.configure(bg="#D4B37F")

    payment_window.update_idletasks()
    window_width = payment_window.winfo_width()
    window_height = payment_window.winfo_height()
    screen_width = payment_window.winfo_screenwidth()
    screen_height = payment_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    payment_window.geometry(f"+{x_cordinate}+{y_cordinate}")

    total_amount = update_total_amount()

    Label(payment_window, text=f"Bill ₱{total_amount:.2f}", font=("Helvetica", 14, "bold"), bg="#D4B37F").grid(row=0, column=0, columnspan=3, pady=10)
    amount_tendered_entry = Entry(payment_window, font=("Helvetica", 14))
    amount_tendered_entry.grid(row=0, column=3, columnspan=3, pady=10, padx=10)

    buttons = [
        ('1', 1, 0), ('2', 1, 1), ('3', 1, 2), ('4', 2, 0),
        ('5', 2, 1), ('6', 2, 2), ('7', 3, 0), ('8', 3, 1),
        ('9', 3, 2), ('0', 4, 1), ('00', 4, 2), ('C', 4, 0),
    ]

    for (text, row, col) in buttons:
        Button(payment_window, text=text, width=10, height=3, command=lambda t=text: add_digit(t) if t != 'C' else clear_entry()).grid(row=row, column=col, padx=5, pady=5)

    Button(payment_window, text="Enter", command=process_payment, width=10, height=3).grid(row=1, column=3, padx=5, pady=5)

def open_gcash_payment_window(parent_window):
    parent_window.destroy()

    global cash_received, change, payment_method_used
    payment_method_used = "Card/GCash"
    cash_received = 0
    change = 0
    gcash_window = Toplevel(window)
    gcash_window.title("Card/GCash Payment")
    gcash_window.configure(bg="#D4B37F")

    gcash_window.update_idletasks()
    window_width = gcash_window.winfo_width()
    window_height = gcash_window.winfo_height()
    screen_width = gcash_window.winfo_screenwidth()
    screen_height = gcash_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    gcash_window.geometry(f"+{x_cordinate}+{y_cordinate}")

    qr_image = Image.open('gcash.jpg')
    qr_image = qr_image.resize((300, 500), Image.LANCZOS)
    gcash = ImageTk.PhotoImage(qr_image)
    qr_label = Label(gcash_window, image=gcash, bg="#D4B37F")
    qr_label.image = gcash 
    qr_label.pack(pady=0)
    Button(gcash_window, text="Done", background="#D4B37F", font=("Helvetica", 12, "bold"), command=lambda: complete_payment(gcash_window)).pack(pady=10)
    
def complete_payment(payment_window):
    payment_window.destroy()
    receipt()
    # Clear the current order after payment
    for item in coffee_quantities:
        for size in coffee_quantities[item]:
            coffee_quantities[item][size] = 0
    update_order_display()
    update_total_amount()
    

payment_button = CTkButton(main_frame, text="Payment", command=payment_method, fg_color="#D4B37F", text_color="black", font=("Helvetica", 12, "bold"), hover_color="#d2691e")
payment_button.place(x=660, y=500)

image14 = Image.open("meow5.png")
image14 = image14.resize((350, 70), Image.LANCZOS)
logo2 = ImageTk.PhotoImage(image14)

pic2 = CTkLabel(main_frame, image=logo2, text="")
pic2.place(x=40, y=2)

def on_enter(event):
    login()

window.bind('<Return>', on_enter)

window.mainloop()
