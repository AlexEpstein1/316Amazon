--- Users Guru
-- Users
CREATE TABLE Users (
	id INT GENERATED BY DEFAULT AS IDENTITY,
	email VARCHAR UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL,
	firstname VARCHAR(255) NOT NULL,
	lastname VARCHAR(255) NOT NULL,
	balance DECIMAL(10,2) NOT NULL
);
-- Sellers
CREATE TABLE Sellers (
	id INT NOT NULL PRIMARY KEY REFERENCES Users(id)
);
-- Buyers
CREATE TABLE Buyers (
	id INT NOT NULL PRIMARY KEY REFERENCES Users(id)
);
--- Products Guru
-- Products
CREATE TABLE Products (
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL,
	cat_name VARCHAR(256) NOT NULL REFERENCES Category(cat_name),
	price FLOAT NOT NULL,
	description VARCHAR(1024) NOT NULL,
	image_file VARCHAR(256) NOT NULL,
	available BOOLEAN DEFAULT TRUE
);
-- Categories of Products
CREATE TABLE Category (
	cat_name VARCHAR(256) NOT NULL PRIMARY KEY,
	description VARCHAR(256) NOT NULL
);
-- Purchases of Products
CREATE TABLE Purchases (
	id INT NOT NULL PRIMARY KEY,
	uid INT NOT NULL REFERENCES Buyers(id),
	pid INT NOT NULL REFERENCES Sellers(id),
	time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);
--- Carts Guru
-- Cart
CREATE TABLE Cart (
	user_id INT NOT NULL REFERENCES Users(id),
	seller_id INT NOT NULL REFERENCES Sellers(id),
	product_id INT NOT NULL REFERENCES Products(id),
	quantity INT NOT NULL CHECK(quantity >= 0),
	price_per_item DECIMAL(10, 2) NOT NULL CHECK(price_per_item >= 0),
	PRIMARY KEY(user_id, seller_id, product_id)
);
-- Submitting Orders
CREATE TABLE OrderEntry (
	order_id INT NOT NULL,
	buyer_id INT NOT NULL REFERENCES Buyers(id),
	seller_id INT NOT NULL REFERENCES Sellers(id),
	product_id INT NOT NULL REFERENCES Products(id),
	payment_amount DECIMAL(10, 2) NOT NULL,
	quantity INT NOT NULL CHECK(quantity >= 0),
	PRIMARY KEY(order_id)
);

--- Sellers Guru
-- For Sale
CREATE TABLE SellsItem (
	seller_id INT NOT NULL REFERENCES Sellers(id),
	product_id INT NOT NULL REFERENCES Products(id),
	price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
	stock INT NOT NULL CHECK(stock >= 0),
	PRIMARY KEY(seller_id, product_id)
);

-- History of orders fulfilled or to be fulfilled?

--- Social Guru
-- Reviews of Products
CREATE TABLE ProductReview (
	user_id INT NOT NULL REFERENCES Users(id),
	product_id INT NOT NULL REFERENCES Products(id),
	date_time DATE NOT NULL,
	description VARCHAR(256) NOT NULL,
	rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
	PRIMARY KEY (user_id, product_id)
	-- probably need a FOREIGN KEY
);
-- Reviews of Sellers
CREATE TABLE SellerReview (
	user_id INT NOT NULL REFERENCES Users(id),
	seller_id INT NOT NULL REFERENCES Sellers(id),
	date_time DATE NOT NULL,
	description VARCHAR(256) NOT NULL,
	rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
	PRIMARY KEY (user_id, seller_id)
	FOREIGN KEY (user_id, seller_id) REFERENCES Purchases(uid, pid)
);
