from werkzeug.security import generate_password_hash
import csv
import random
from faker import Faker
from datetime import datetime, timedelta


num_users = 200
num_category = 30
num_products = 1000
num_purchases = 2000
num_cart = 2000
num_item_sold = 2000
num_product_review = 1000
num_seller_review = 1000
max_stock_unit = 1000
max_purchase_unit = 10
status_list = ['Complete', 'Incomplete']
purchase_user_ID = []
purchase_seller_ID= []
purchase_product_ID = []

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
        print('Category...', end=' ', flush=True)
        for pid in range(num_category):
            name = fake.sentence(nb_words=1)[:-1]
            description = fake.sentence(nb_words=10)[:-1]
            if name not in available_category:
                writer.writerow([name, description])
                available_category.append(name)
        print(f'{num_category} generated; {len(available_category)} available')
    return available_category

def gen_products(num_products, available_category):
    product_name = []
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
            img = 'img'
            if name not in product_name:
                product_dict[pid] = price
                product_name.append(name)
                writer.writerow([pid, name, cat_name, product_description, img, available])
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
            purchase_user_ID.append(uid)
            purchase_seller_ID.append(sid)
            purchase_product_ID.append(pid)
            time_purchased = fake.date_time()
            time_processed = time_purchased + timedelta(weeks = 2) # Assumed all purchases are processes in a week
            if time_processed > datetime.now(tz=None): 
                status = 'Incomplete'
                time_processed = datetime(1, 1, 1, 1, 1, 1)
            else: 
                status = 'Complete'
            quantity = fake.random_int(min=0, max=max_purchase_unit)
            payment_amount = float(product_dict.get(pid)) * int(quantity)
            writer.writerow([id, pid, uid, sid, payment_amount, quantity, time_purchased, time_processed, status])
        print(f'{num_purchases} generated')
    return


def gen_cart(num_cart, product_dict):
    cart_id = []
    with open('Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for id in range(num_cart):
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=product_dict.keys())
            quantity = fake.random_int(min=1, max=max_purchase_unit)
            price = product_dict.get(pid)
            key = [uid, sid, pid]
            if key not in cart_id:
                cart_id.append(key)
                writer.writerow([uid, sid, pid, quantity, price])
        print(f'{num_cart} generated')
    return

def gen_SellsIten(num_item_sold, product_dict):
    sold_item_id = []
    with open('SellsItem.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellsItem...', end=' ', flush=True)
        for id in range(num_item_sold):
            sid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=product_dict.keys())
            price = product_dict.get(pid)
            stock = fake.random_int(min=0, max=max_stock_unit)
            key = [sid, pid]
            if key not in sold_item_id:
                sold_item_id.append(key)
                writer.writerow([sid, pid, price, stock])
        print(f'{num_item_sold} generated')
    return


def gen_ProductReview(num_product_review):
    key_list = []
    with open('ProductReview.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ProductReview...', end=' ', flush=True)
        for i in range(num_product_review):
            purchase_record = fake.random_int(min=0, max= len(purchase_user_ID)-1)
            uid = purchase_user_ID[purchase_record]
            pid = purchase_product_ID[purchase_record]
            time = fake.date_time()
            description = fake.sentence(nb_words=10)[:-1]
            rating = fake.random_int(min=1, max=5)
            key = [uid, pid]
            if key not in key_list:
                key_list.append(key)
                writer.writerow([uid, pid, time, description,rating])
        print(f'{num_product_review} generated')
    return 

def gen_SellerReview(num_seller_review):
    key_list = []
    with open('SellerReview.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerReview...', end=' ', flush=True)
        for i in range(num_seller_review):
            purchase_record = fake.random_int(min=0, max= len(purchase_user_ID)-1)
            uid = purchase_user_ID[purchase_record]
            sid = purchase_seller_ID[purchase_record]
            time = fake.date_time()
            description = fake.sentence(nb_words=10)[:-1]
            rating = fake.random_int(min=1, max=5)
            key = [uid, sid]
            if key not in key_list:
                key_list.append(key)
                writer.writerow([uid, sid, time, description,rating])
        print(f'{num_seller_review} generated')
    return 


gen_users(num_users)
available_category = gen_category(num_category);
product_dict = gen_products(num_products, available_category)
gen_purchases(num_purchases, product_dict)
gen_cart(num_cart, product_dict)
gen_SellsIten(num_item_sold, product_dict)
gen_ProductReview(num_product_review)
gen_SellerReview(num_seller_review)
