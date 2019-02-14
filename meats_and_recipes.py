from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from base64 import b64encode
import base64
import os

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "dmongey_meats_and_recipes"
app.config["MONGO_URI"] = "mongodb://dmongey:Password1@ds247223.mlab.com:47223/dmongey_meats_and_recipes"

mongo = PyMongo(app)

# ----------- Homepage -----------------


@app.route("/")
def show_macros():
    return render_template("homepage.html")

# ------------- List the meats -----------


@app.route("/meats")
def show_meats():
    animals = mongo.db["images"].find({"animal_name": {"$exists": True}})
    return render_template("meats.html", animals=animals)

# ------------ Add a meat form -------------


@app.route("/add_animal", methods=["POST", "GET"])
def add_animal():
    if request.method == "POST":
        image = request.files['image']
        image_string = base64.b64encode(image.read()).decode("utf-8")
        form_values = request.form.to_dict()
        form_values["image"] = "data:image/png;base64," + image_string
        mongo.db["images"].insert_one(form_values)
        return redirect("/meats")
    else:
        return render_template("add_meat.html")

# -------------- List the Cuts -----------------


@app.route("/<animal_name>/cuts")
def show_cuts(animal_name):
    animal = mongo.db["animals"].find({"animal_name": animal_name})
    return render_template("cuts.html", animal=animal, animal_name=animal_name)

# ------------------- Add a cut form --------------


@app.route("/<animal_name>/add_cut", methods=["POST", "GET"])
def add_cut(animal_name):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["animals"].insert_one(form_values)
        return redirect(url_for("show_cuts", animal_name=animal_name))
    else:
        return render_template("add_cut.html", animal_name=animal_name)

# ----------------- Edit a cut -------------------------


@app.route("/<animal_name>/<cut_id>/edit/cut", methods=["POST", "GET"])
def edit_cut(animal_name, cut_id):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["animals"].update({"_id": ObjectId(cut_id)}, form_values)

        if form_values["animal_name"] != animal_name:
            the_cut = mongo.db["animals"].find_one({"_id": ObjectId(cut_id)})
            mongo.db["animals"].remove(the_cut)
            mongo.db[form_values["animal_name"]].insert(the_cut)
            animal_name = form_values["animal_name"]

        return redirect(url_for("show_cuts", animal_name=animal_name))
    else:
        the_cut = mongo.db["animals"].find_one({"_id": ObjectId(cut_id)})
        return render_template('edit_cut.html', cut=the_cut)

# ----------------- List vegetables ----------------------


@app.route("/vegetables")
def show_vegetables():
    vegetables = mongo.db["vegetables"].find({"vegetable_name":
                                             {"$exists": True}})
    return render_template("vegetables.html", vegetables=vegetables)

# ------------------- Add vegetable form --------------------


@app.route("/add_vegtable", methods=["POST", "GET"])
def add_vegetable():
    if request.method == "POST":
        image = request.files['image']
        image_string = base64.b64encode(image.read()).decode("utf-8")
        form_values = request.form.to_dict()
        form_values["image"] = "data:image/png;base64," + image_string
        mongo.db["vegetables"].insert_one(form_values)
        return redirect("/vegetables")
    else:
        return render_template("add_vegetable.html")

# ----------------- Edit vegetable form ---------------------


@app.route("/<vegetable_name>/<vegetable_id>/edit/", methods=["POST", "GET"])
def edit_vegetable(vegetable_name, vegetable_id):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["vegetables"].update({"_id":
                                      ObjectId(vegetable_id)}, form_values)
        return redirect(url_for("show_vegetables"))
    else:
        vegetable = mongo.db["vegetables"].find_one({"_id":
                                                     ObjectId(vegetable_id)})
        return render_template('edit_vegetable.html', vegetable=vegetable)

# --------------------- List meals --------------------------


@app.route("/meal")
def show_meals():
    meals = mongo.db["images"].find({"meal_name": {"$exists": True}})
    return render_template("meals.html", meals=meals)

# --- Saves nutrition info of meat for a meal in dictionary form ---


def meat_nutrition_info(meat):
    animal, cut = meat.split(" ")
    ingredient = mongo.db["animals"].find_one({"animal_name": animal,
                                               "cut_name": cut})
    return {"carbs": ingredient["carbohydrates"],
            "fat": ingredient["fat"],
            "protein": ingredient["protein"],
            "calories": ingredient["calories"]}

# --- Saves nutrition info of veg for a meal in dictionary form ---


def veg_nutrition_info(veg):
    ingredient = mongo.db["vegetables"].find_one({"vegetable_name": veg})
    return {"carbs": ingredient["carbohydrates"],
            "fat": ingredient["fat"],
            "protein": ingredient["protein"],
            "calories": ingredient["calories"]}

# -------------- Add meal form --------------------


@app.route("/add_meal", methods=["POST", "GET"])
def add_meal():
    if request.method == "POST":
        image = request.files['image']
        image_string = base64.b64encode(image.read()).decode("utf-8")
        image_collection = request.form.to_dict()
        image_collection["image"] = "data:image/png;base64," + image_string
        meal_collection = request.form.to_dict()
        meats = request.form.getlist("meats")
        meal_collection["meats"] = {meat: meat_nutrition_info(meat)
                                    for meat in meats}
        vegetables = request.form.getlist("vegetables")
        meal_collection["vegetables"] = {veg: veg_nutrition_info(veg)
                                         for veg in vegetables}
        herbs_and_spices = request.form.getlist("herbs_or_spices")
        meal_collection["herbs_or_spices"] = herbs_and_spices
        mongo.db["images"].insert_one(image_collection)
        mongo.db["meals"].insert_one(meal_collection)
        return redirect("/meals")
    else:
        meat_images = mongo.db["images"].find({"animal_name":
                                              {"$exists": True}})
        vegetables = mongo.db["vegetables"].find()
        herbs = mongo.db["herbs"].find()
        spices = mongo.db["spices"].find()
        vegetable = []
        for veg in vegetables:
            vegetable.append(veg["vegetable_name"])

        meat_options = {}
        for image in meat_images:
            name = image["animal_name"]
            cut_names = []
            animals = mongo.db["animals"].find({"animal_name": name})
            for animal in animals:
                cut_names.append(animal["cut_name"])

            meat_options[name] = cut_names

        return render_template("add_meal.html",
                               meat_options=meat_options,
                               vegetables=vegetable,
                               herbs=herbs, spices=spices)

# --------------- Ingredients and nutritional info for meals ---------------


@app.route("/meal/<meal_name>/<meal_id>/")
def show_meal(meal_name, meal_id):
    meal = mongo.db["meals"].find({"meal_name": meal_name})
    images = mongo.db["images"].find({"meal_name": meal_name})

    cals = []
    carbs = []
    fat = []
    protein = []
    for r in meal:
        vegetables = r["vegetables"]

        for veg, info in vegetables.items():
            cals.append(float(info["calories"]))
            carbs.append(float(info["carbs"]))
            fat.append(float(info["fat"]))
            protein.append(float(info["protein"]))

        meats = r["meats"]
        for meat, info in meats.items():
            cals.append(float(info["calories"]))
            carbs.append(float(info["carbs"]))
            fat.append(float(info["fat"]))
            protein.append(float(info["protein"]))
        meal_name = r["meal_name"]
        meal_id = r["_id"]
        meal_meats = r["meats"]
        meal_vegetables = r["vegetables"]
        meal_seasoning = r["herbs_or_spices"]

    total_cals = round(sum(cals), 1)
    total_carbs = round(sum(carbs), 1)
    total_fat = round(sum(fat), 1)
    total_protein = round(sum(protein), 1)
    return render_template("meal.html",
                           images=images, meal_name=meal_name,
                           meal_id=meal_id, meal_meats=meal_meats,
                           meal_vegetables=meal_vegetables,
                           meal_seasoning=meal_seasoning,
                           total_cals=total_cals, total_carbs=total_carbs,
                           total_fat=total_fat, total_protein=total_protein)

if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'),
                port=int(os.getenv('PORT', 8080)), debug=True)
