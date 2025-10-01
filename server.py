from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask (__name__)


# http://127.0.0.1:5000/
@app.route("/", methods=["GET"])
def index():
    return "Welcome to Flask framework!"


# http://127.0.0.1:5000/cohort-60
@app.route("/cohort-60", methods=["GET"])
def hello_world():
    print("Cohort 60 endpoint accessed")
    return "Hello Cohort#60"


# http://127.0.0.1:5000/contact
@app.route("/contact", methods=["GET"])
def contact():
    information = {"email": "zanem201@gmail.com", "phone": "1-234-567-8910"}
    return information


@app.route("/course", methods=["GET"])
def course_information():
    return {
        "title": "Introductory Web API Flask",
        "duration": "4 sessions",
        "level": "Beginner"
    }


@app.route("/user", methods=["Get"])
def user_info():
    user_information = {
        "name": "Zane",
        "role": "Student",
        "is_active": True,
        "favorite_technologies": ["React", "jQuery", "Python"]
    }
    return user_information  
   

student_names = ["Reggie", "Tim", "Zane", "Michael", "Jake", "Jose"]

@app.route("/students", methods=["GET"])
def get_students():
    print("Students endpoint accessed")
    return student_names


@app.route("/students", methods=["POST"])
def add_student():
    student_names.append("Leo")
    return student_names


# -------- Assignment #1 --------

products = [
  {"id": 1, "name": "Cake", "price": 25},
  {"id": 2, "name": "Ice-cream", "price": 5},
  {"id": 3, "name": "Cookie", "price": 3},
  {"id": 4, "name": "Chocolate", "price": 10}
]

@app.route("/api/products", methods=["GET"])
def get_products():
    return products


@app.route("/api/products/count", methods=["GET"])
def products_count():
    return  {"count": len(products)}

# -------------------------------
# -------- Assignment #2 --------
@app.route("/api/products", methods=["POST"])
def create_product():
    new_product = request.get_json()
    print(new_product)
    products.append(new_product)
    return jsonify(new_product), HTTPStatus.CREATED


@app.route("/api/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    for product in products:
        if product["id"] == id:
            return jsonify(product), HTTPStatus.OK
    return jsonify({"message": "Product Not Found"}), HTTPStatus.NOT_FOUND    


@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    for index, product in enumerate(products):
        if product["id"] == id:
            products.pop(index)
            return "", HTTPStatus.NO_CONTENT
    return "Product Not Found", HTTPStatus.NOT_FOUND

# -------------------------------
# --------- Session #2 ---------

coupons = [
    {"_id":1, "code": "WELCOME10", "discount": 10},
    {"_id":2, "code": "FALL25", "discount": 25},
    {"_id":3, "code": "VIP50", "discount": 50} 
]

# READ all coupons
@app.route("/api/coupons", methods=["GET"])
def get_coupons():
    return jsonify(coupons), HTTPStatus.OK


# CREATE, add a new coupon
@app.route("/api/coupons", methods=["POST"])
def create_coupon():
    new_coupon = request.get_json()
    print(new_coupon)
    coupons.append(new_coupon)
    return jsonify(new_coupon), HTTPStatus.CREATED 


# Path parameter
@app.route("/greet/<string:name>", methods=["GET"])
def greet(name):
    return f"hello {name}", HTTPStatus.OK 


# GET a coupon by id
@app.route("/api/coupons/<int:id>", methods=["GET"])
def get_coupon_by_id(id):
    for coupon in coupons:
        if coupon["_id"] == id:
            return jsonify(coupon), HTTPStatus.OK
    return jsonify({"message": "Coupon Not Found"}), HTTPStatus.NOT_FOUND    


# UPDATE - /api/products/2
@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    for product in products:
        if product["id"] == id:
            product["name"] = data.get("name")
            product["price"] = data.get("price")
            return jsonify({"message": "Product updated successfully"}), HTTPStatus.OK
    return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND


# -------- Assignment #4 --------
@app.route("/api/coupons/<int:id>", methods=["PUT"])
def update_coupon(id):
    data = request.get_json()
    for coupon in coupons:
        if coupon["_id"] == id:
            coupon["code"] = data.get("code")
            coupon["discount"] = data.get("discount")
            return jsonify({"message": "Coupon updated successfully"}), HTTPStatus.OK
    return jsonify({"message": "Coupon Not Found!"}), HTTPStatus.NOT_FOUND


@app.route("/api/coupons/search", methods=["GET"])
def get_coupons_by_discount():
    max_discount = request.args.get("max_discount")
    if max_discount is None:
        return jsonify({"message": "max_discount parameter is required"}), HTTPStatus.BAD_REQUEST
    try:
        max_discount = int(max_discount)
    except ValueError:
        return jsonify({"message": "max_discount must be a number"}), HTTPStatus.BAD_REQUEST
    
    matched = []
    for coupon in coupons:
        if coupon["discount"] < max_discount:
            matched.append(coupon)
    return jsonify({"results": matched}), HTTPStatus.OK
# --------- Session #4 ---------
# Query parameters
# A query parameter is added to the end of the URL to filter, sort or modify the response

# GET /api/products/search?name=xxxx
@app.route("/api/products/search", methods=["GET"])
def get_product_by_name():
    keyword = request.args.get("name").lower()

    matched = []
    for product in products:
        if keyword in product("name").lower():
            matched.append(product)
    return jsonify({"results": matched}), HTTPStatus.OK


# DELETE - delete a coupon
@app.route("/api/coupons/<int:id>", methods=["DELETE"])
def delete_coupon(id):
    for index, coupon in enumerate(coupons):
        if coupon["_id"] == id:
            coupons.pop(index)
            return "", HTTPStatus.NO_CONTENT  #204
    return "testing"


if __name__ == "__main__":
    app.run(debug=True)