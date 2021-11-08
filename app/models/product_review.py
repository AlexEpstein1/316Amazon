from flask import current_app as app

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
    def __init__(self, user_id, product_id, date_time, description, rating):
        self.user_id = user_id
        self.product_id = product_id
        self.date_time = date_time
        self.description = description
        self.rating = rating

    @staticmethod
    def get(user_id):
        rows = app.db.execute('''
SELECT user_id, product_id, date_time, description, rating
FROM ProductReview
WHERE user_id = :user_id
''',
                              user_id=user_id)
        return ProductReview(*(rows[0])) if rows else None

    @staticmethod
    def add_prod_review():

        reviews = ProductReview.get(user_id=current_user.id)

        return reviews


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
