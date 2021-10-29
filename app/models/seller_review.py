from flask import current_app as app

# Reviews of Sellers
# CREATE TABLE SellerReview (
# 	user_id INT NOT NULL REFERENCES Users(id),
# 	seller_id INT NOT NULL REFERENCES Sellers(id),
# 	date_time DATE NOT NULL,
# 	description VARCHAR(256) NOT NULL,
# 	rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
# 	PRIMARY KEY (user_id, seller_id)
# 	FOREIGN KEY (user_id, seller_id) REFERENCES Purchases(uid, pid)
# );

class SellerReview:
    def __init__(self, user_id, seller_id, date_time, description, rating):
        self.user_id = user_id
        self.seller_id = seller_id
        self.date_time = date_time
        self.description = description
        self.rating = rating

    @staticmethod
    def get(user_id):
        rows = app.db.execute('''
SELECT user_id, seller_id, date_time, description, rating
FROM SellerReview
WHERE user_id = :user_id
''',
                              user_id=user_id)
        return SellerReview(*(rows[0])) if rows else None
