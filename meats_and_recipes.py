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


def get_category_names():
    categories = []
    for category in mongo.db.collection_names():
        if not category.startswith("system.") and not category.startswith("animals") and not category.startswith("vegetables") and not category.startswith("images") and not category.startswith("recipes"):
            categories.append(category)
    return categories  

@app.route("/")
def show_macros():
    return render_template("homepage.html")
    
@app.route("/meats")
def show_meats():
    animals = mongo.db["images"].find({"animal_name": { "$exists": True }})
    return render_template("meats.html", animals=animals)
    
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
        
@app.route("/<animal_name>/cuts") 
def show_cuts(animal_name):
    animal = mongo.db["animals"].find({"animal_name" : animal_name})
    return render_template("cuts.html", animal=animal, animal_name=animal_name)
    
@app.route("/<animal_name>/add_cut", methods=["POST", "GET"])
def add_cut(animal_name):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["animals"].insert_one(form_values)
        return redirect(url_for("show_cuts", animal_name=animal_name))
    else: 
        return render_template("add_cut.html", animal_name=animal_name)
        
@app.route("/<animal_name>/<cut_id>/edit/cut", methods=["POST", "GET"])        
def edit_cut(animal_name, cut_id):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["animals"].update({"_id": ObjectId(cut_id)}, form_values)
        
        if form_values["animal_name"] != animal_name:
            the_cut = mongo.db["animals"].find_one({"_id": ObjectId(cut_id)})
            mongo.db["animals"].remove(the_cut)
            mongo.db[form_values["animal_name"]].insert(the_cut)
            
        return redirect(url_for("show_cuts", animal_name=form_values["animal_name"]))
    else:
        the_cut =  mongo.db["animals"].find_one({"_id": ObjectId(cut_id)})
        return render_template('edit_cut.html', cut=the_cut)
    
@app.route("/vegetables")
def show_vegetables():
    vegetables = mongo.db["vegetables"].find({"vegetable_name": { "$exists": True }})
    return render_template("vegetables.html", vegetables=vegetables)
    
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

@app.route("/<vegetable_name>/<vegetable_id>/edit/", methods=["POST", "GET"])        
def edit_vegetable(vegetable_name, vegetable_id):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["vegetables"].update({"_id": ObjectId(vegetable_id)}, form_values)
        return redirect(url_for("show_vegetables"))
    else:
        the_vegetable =  mongo.db["vegetables"].find_one({"_id": ObjectId(vegetable_id)})
        return render_template('edit_vegetable.html', vegetable=the_vegetable)
 
    
@app.route("/recipes")
def show_recipes():
    recipes = mongo.db["images"].find({"recipe_name": { "$exists": True }})
    return render_template("recipes.html", recipes=recipes)
        
        
def meat_nutrition_info(meat):
    animal, cut = meat.split(" ")
    ingredient = mongo.db["animals"].find_one({"animal_name" : animal, "cut_name" : cut})
    return { "carbs" : ingredient["carbohydrates"], "fat" : ingredient["fat"], "protein" : ingredient["protein"], "calories" : ingredient["calories"] }
    
def veg_nutrition_info(veg):
    ingredient = mongo.db["vegetables"].find_one({"vegetable_name" : veg})
    return { "carbs" : ingredient["carbohydrates"], "fat" : ingredient["fat"], "protein" : ingredient["protein"], "calories" : ingredient["calories"] }
        
@app.route("/add_recipe", methods=["POST", "GET"])
def add_recipe():
    if request.method == "POST":
        image = request.files['image']  
        image_string = base64.b64encode(image.read()).decode("utf-8")
        image_collection = request.form.to_dict()
        image_collection["image"] = "data:image/png;base64," + image_string
        recipe_collection = request.form.to_dict()
        meats = request.form.getlist("meats")
        recipe_collection["meats"] = {meat : meat_nutrition_info(meat) for meat in meats}
        vegetables = request.form.getlist("vegetables")
        recipe_collection["vegetables"] = {veg : veg_nutrition_info(veg) for veg in vegetables}
        herbs_and_spices = request.form.getlist("herbs_or_spices")
        recipe_collection["herbs_or_spices"] = herbs_and_spices
        mongo.db["images"].insert_one(image_collection)
        mongo.db["recipes"].insert_one(recipe_collection)
        return redirect("/recipes")
    else:
        meat_images = mongo.db["images"].find({"animal_name": { "$exists": True }})
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
            
        return render_template("add_recipe.html", meat_options=meat_options, vegetables=vegetable, herbs=herbs, spices=spices)
        
@app.route("/recipe/<recipe_name>/<recipe_id>/") 
def show_recipe(recipe_name, recipe_id):
    recipe = mongo.db["recipes"].find({"recipe_name" : recipe_name})
    images = mongo.db["images"].find({"recipe_name": recipe_name})
    
    cals = []
    carbs = []
    fat = []
    protein = []
    for r in recipe:
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
        recipe_name = r["recipe_name"]
        recipe_id = r["_id"]
        recipe_meats = r["meats"]
        recipe_vegetables = r["vegetables"]
        recipe_seasoning = r["herbs_or_spices"]
        
    total_cals = round(sum(cals), 1)
    total_carbs = round(sum(carbs), 1)
    total_fat = round(sum(fat), 1)
    total_protein = round(sum(protein), 1)
    return render_template("recipe.html", images=images, recipe_name=recipe_name, recipe_id=recipe_id, recipe_meats=recipe_meats, recipe_vegetables=recipe_vegetables, recipe_seasoning=recipe_seasoning, total_cals=total_cals, total_carbs=total_carbs, total_fat=total_fat, total_protein=total_protein)
    
@app.route("/<recipe_name>/<recipe_id>/edit/recipe", methods=["POST", "GET"])        
def edit_recipe(recipe_name, recipe_id):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["recipes"].update({"_id": ObjectId(recipe_id)}, form_values)
        
        if form_values["recipe_name"] != recipe_name:
            the_recipe = mongo.db["recipes"].find_one({"_id": ObjectId(recipe_id)})
            mongo.db["recipes"].remove(the_recipe)
            mongo.db[form_values["recipe_name"]].insert(recipe_name)
            
        return redirect(url_for("show_recipes", recipe_name=form_values["recipe_name"]))
    else:
        the_recipe =  mongo.db["recipes"].find_one({"_id": ObjectId(recipe_id)})
        meat_images = mongo.db["images"].find({"animal_name": { "$exists": True }})
        veg_images = mongo.db["images"].find({"vegtable_name": { "$exists": True }})
        herbs = mongo.db["herbs"].find()
        spices = mongo.db["spices"].find()
        
        meat_options = {}
        for image in meat_images:
            name = image["animal_name"]
            cut_names = []
            animals = mongo.db["animals"].find({"animal_name": name})
            for animal in animals:
                cut_names.append(animal["cut_name"])
            
            meat_options[name] = cut_names
            
        veg_options = {}
        for image in veg_images:
            name = image["vegtable_name"]
            veg_names = []
            vegetables = mongo.db["vegetables"].find({"vegtable_name": name})
            for vegtable in vegetables:
                veg_names.append(vegtable["veg_option"])
            
            veg_options[name] = veg_names
            
        return render_template('edit_recipe.html', recipe=the_recipe, meat_options=meat_options, veg_options=veg_options, herbs=herbs, spices=spices)

if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)

