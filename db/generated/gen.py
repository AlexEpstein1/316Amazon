from werkzeug.security import generate_password_hash
import csv
import random
from faker import Faker

num_users = 50
num_category = 50
num_products = 1000
num_purchases = 1500
num_cart = 3000
num_item_sold = 4000
max_stock_unit = 1000
max_purchase_unit = 10
status_list = ['Complete', 'Incomplete']

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            balance = random.random()*10000
            writer.writerow([uid, email, password, firstname, lastname, balance])
        print(f'{num_users} generated')
    return


def gen_category(num_category):
    available_category = []
    with open('Category.csv', 'w') as f:
        writer = get_csv_writer(f)
        for pid in range(num_category):
            name = fake.sentence(nb_words=1)[:-1]
            description = fake.sentence(nb_words=10)[:-1]
            writer.writerow([name, description])
            available_category.append(name)
        print(f'{num_category} generated; {len(available_category)} available')
    return available_category

def gen_products(num_products):
    available_pids = []
    pid_price = []
    product_dict = {}
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=2)[:-1]
            cat_name = fake.random_element(elements=available_category)
            product_description = fake.sentence(nb_words=10)[:-1];
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                product_dict[pid] = price
            writer.writerow([pid, name, cat_name, price, product_description, available])
        print(f'{num_products} generated; {len(product_dict)} available')
    return product_dict


def gen_purchases(num_purchases, product_dict):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=product_dict.keys())
            status = fake.random_element(elements=status_list)
            time_purchased = fake.date_time()
            quantity = fake.random_int(min=0, max=max_purchase_unit)
            payment_amount = float(product_dict.get(pid)) * int(quantity)
            writer.writerow([id, pid, uid, sid, payment_amount, quantity, time_purchased, status])
        print(f'{num_purchases} generated')
    return

def gen_cart(num_cart, product_dict):
    with open('Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        for id in range(num_cart):
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=product_dict.keys())
            quantity = fake.random_int(min=0, max=max_purchase_unit)
            price = product_dict.get(pid)
            writer.writerow([uid, sid, pid, quantity, price])
        print(f'{num_purchases} generated')
    return

def gen_SellsIten(num_item_sold, product_dict):
    with open('SellsItem.csv', 'w') as f:
        writer = get_csv_writer(f)
        for id in range(num_item_sold):
            sid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=product_dict.keys())
            price = product_dict.get(pid)
            stock = fake.random_int(min=0, max=max_stock_unit)
            writer.writerow([sid, pid, price, stock])
        print(f'{num_purchases} generated')
    return


gen_users(num_users)
available_category = gen_category(num_category);
product_dict = gen_products(num_products)
gen_purchases(num_purchases, product_dict)
gen_cart(num_cart, product_dict)
gen_SellsIten(num_item_sold, product_dict)
