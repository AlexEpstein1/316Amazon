from werkzeug.security import generate_password_hash
import csv
import random
from faker import Faker

num_users = 50
num_category = 50
num_products = 1000
num_purchases = 1500

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
                available_pids.append(pid)
                pid_price.append(price)
            writer.writerow([pid, name, cat_name, price, product_description, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return dict(map(available_pids, pid_price))


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return


gen_users(num_users)
available_category = gen_category(num_category);
pid_price_map = gen_products(num_products)
gen_purchases(num_purchases, pid_price_map.keys())
