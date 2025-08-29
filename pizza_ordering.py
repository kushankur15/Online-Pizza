import streamlit as st
import sqlite3
from datetime import datetime

# --- DATABASE CONNECTION ---
conn = sqlite3.connect("pizza.db")
c = conn.cursor()

# --- CREATE TABLES IF NOT EXISTS ---
c.execute("""CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                date TEXT,
                payment_method TEXT
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                pizza TEXT,
                quantity INTEGER,
                total REAL,
                date TEXT
            )""")
conn.commit()

# --- STREAMLIT APP ---
st.title("🍕 Online Pizza Ordering App")

# --- CUSTOMER DETAILS ---
st.header("Customer Details")
name = st.text_input("Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email")
order_date = st.date_input("Date", datetime.today())

if st.button("Save Details"):
    if name and phone and email:
        c.execute("INSERT INTO customers (name, phone, email, date) VALUES (?, ?, ?, ?)", 
                  (name, phone, email, str(order_date)))
        conn.commit()
        st.success("✅ Customer details saved!")
    else:
        st.error("⚠️ Please fill all details before saving.")

# --- PIZZA MENU ---
st.header("Pizza Menu")
menu = {
    "Margherita": 200,
    "Pepperoni": 350,
    "Veggie Delight": 250,
    "Chicken Supreme": 400
}

order_list = []
for p, price in menu.items():
    qty = st.number_input(f"{p} (₹{price})", min_value=0, step=1, key=p)
    if qty > 0:
        total = price * qty
        order_list.append((p, qty, total))

if st.button("Add to Order"):
    if name:
        for p, qty, total in order_list:
            c.execute("INSERT INTO orders (customer_name, pizza, quantity, total, date) VALUES (?, ?, ?, ?, ?)", 
                      (name, p, qty, total, str(order_date)))
        conn.commit()
        st.success("✅ Your pizzas were added successfully!")
    else:
        st.error("⚠️ Please enter customer details first.")

# --- DISPLAY ORDERS ---
st.header("Your Orders")
c.execute("SELECT pizza, quantity, total FROM orders WHERE customer_name=?", (name,))
orders = c.fetchall()
if orders:
    for pizza, qty, tot in orders:
        st.write(f"{pizza} × {qty} = ₹{tot}")
    total_bill = sum([o[2] for o in orders])
    st.subheader(f"💰 Total Bill: ₹{total_bill}")
else:
    st.info("No orders yet!")

# --- FAKE PAYMENT ---
if orders:
    st.header("💳 Payment")
    payment_method = st.radio("Choose a payment method", 
                              ["Credit Card", "UPI", "Cash on Delivery"])
    
    if st.button("Proceed to Payment"):
        # update customers table with payment method
        c.execute("UPDATE customers SET payment_method=? WHERE name=? AND date=?",
                  (payment_method, name, str(order_date)))
        conn.commit()
        
        st.success(f"✅ Payment Successful via {payment_method}!")
        st.balloons()
        st.info("🎉 Your pizza is on the way 🚴‍♂️🍕")
