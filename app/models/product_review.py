from flask import current_app as app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import exc
import datetime

# Reviews of Products
# CREATE TABLE ProductReview (
# 	user_id INT NOT NULL REFERENCES Users(id),
# 	product_id INT NOT NULL REFERENCES Products(id),
# 	date_time DATE NOT NULL,
# 	description VARCHAR(256) NOT NULL,
# 	rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
# 	PRIMARY KEY (user_id, product_id)
# 	-- probably need a FOREIGN KEY
# );

class ProductReview:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.product_id = kwargs.get('product_id')
        self.date_time = kwargs.get('date_time')
        self.description = kwargs.get('description', '')
        self.rating = kwargs.get('rating')
        self.exists = kwargs.get('exists')

    @staticmethod
    def get(user_id, product_id = None):
        # If no passed in `product_id`, then just return all reviews from that user
        if product_id is None:
            rows = app.db.execute('''
            SELECT user_id, product_id, date_time, description, rating
            FROM ProductReview
            WHERE user_id = :user_id
            ORDER BY date_time DESC
            ''',
                                  user_id = user_id)
        # If `product_id` passed in, then return review from that user for the given product
        else:
            rows = app.db.execute('''
            SELECT user_id, product_id, date_time, description, rating
            FROM ProductReview
            WHERE user_id = :user_id AND product_id = :product_id
            ''',
                                  user_id = user_id,
                                  product_id = product_id)

        # If there exists a previous review, create the object
        if rows:
            return[ProductReview(user_id = row[0],
                                 product_id = row[1],
                                 date_time = row[2],
                                 description = row[3],
                                 rating = row[4],
                                 exists = True) for row in rows]
        # Otherwise, create an empty ProductReview object
        else:
            return(ProductReview(exists = False))

    @staticmethod
    def add_prod_review(request, product_id):
        # Get information to add to review
        date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        description = request.form['body']
        rating = request.form['numstars']

        # print(date_time)
        # print(description)
        # print(rating)

        try:
            rows = app.db.execute("""
        INSERT INTO ProductReview(user_id, product_id, date_time, description, rating)
        VALUES(:user_id, :product_id, :date_time, :description, :rating)
        RETURNING user_id
        """,
                      user_id = current_user.id,
                      product_id = product_id,
                      date_time = date_time,
                      description = description,
                      rating = rating)
        # this means already a review for this product from this user
        except exc.IntegrityError as e:
            return False

        return True

    @staticmethod
    def update_review(request, product_id):

        date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        description = request.form['body']
        rating = request.form['numstars']

        rows = app.db.execute("""
    UPDATE ProductReview
    SET rating = :rating, description = :description
    WHERE user_id = :user_id AND product_id = :product_id
    RETURNING user_id
    """,
                  rating = rating,
                  description = description,
                  user_id = current_user.id,
                  product_id = product_id)

        return True

    @staticmethod
    def delete_review(product_id):
        rows = app.db.execute("""
    DELETE FROM ProductReview
    WHERE user_id = :user_id AND product_id = :product_id
    RETURNING user_id
    """,
                  user_id = current_user.id,
                  product_id = product_id)
        # flash('Deleted product review for product ID: ' + product_id)
        return 'Deleted product review for product ID: ' + product_id

    # def add_review():
    #
    # item_id = request.args['itemid']
    # if request.method == 'POST':
    #     username= session['username']
    #     username = "'" +str(username)+"'"
    #     dt_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    #     day = "'"+str(dt_string)+"'"
    #     content = str(request.form['body'])
    #     content = "'"+str(content)+"'"
    #     stars= float(request.form['numstars'])
    #     cur = conn.cursor()
    #     checkSeller = "SELECT * FROM SellsItem WHERE seller_username = %s AND item_id=%d;" % (username, int(item_id))
    #     cur.execute(checkSeller)
    #     checker=cur.fetchall()
    #     if len(checker)>0:
    #         flash("Cannot review an item you are selling!")
    #         return redirect(url_for('productDescription', itemid=item_id))
    #     else:
    #         cur = conn.cursor()
    #         AlreadyReviewToday = "SELECT * FROM Reviews WHERE username = %s AND item_id=%d AND date_time=%s;" % (username, int(item_id), day)
    #         cur.execute(AlreadyReviewToday)
    #         checker2=cur.fetchall()
    #         if len(checker2)>0:
    #             flash("Cannot review an item twice on same day!")
    #             return redirect(url_for('productDescription', itemid=item_id))
    #         else:
    #             cur = conn.cursor()
    #             addRev = "INSERT INTO Reviews VALUES (%s, %d, %s, %s, %d);" % (username, int(item_id), day, content, stars)
    #             cur.execute(addRev)
    #             conn.commit()
    #             flash("Review submitted successfully")
    #             return redirect(url_for('productDescription', itemid=item_id))
    # getName = "SELECT name FROM Items WHERE item_id = %d;" % int(item_id)
    # cur = conn.cursor()
    # cur.execute(getName)
    # item_name = cur.fetchall()[0][0]
    # item = {
    #     "itemid": item_id,
    #     "itemname": item_name
    # }
    # return render_template("reviews.html", item=item)


class ProductReviewWithName:
    def __init__(self, user_id, firstname, lastname, product_id, date_time, description, rating):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.product_id = product_id
        self.date_time = date_time
        self.description = description
        self.rating = rating

    @staticmethod
    def get_reviews(product_id):
        # If no passed in `product_id`, then just return all reviews from that user

        rows = app.db.execute('''
        SELECT user_id, firstname, lastname, product_id, date_time, description, rating
        FROM ProductReview, Users
        WHERE product_id = :product_id AND user_id = id
        ORDER BY date_time DESC
        ''',
             product_id=product_id)
        # If `product_id` passed in, then return review from that user for the given product

        return [ProductReviewWithName(*row) for row in rows] if rows else None
