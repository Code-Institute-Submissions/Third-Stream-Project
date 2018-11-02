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

def get_animal_names():
    animals = []
    for animal in mongo.db.collection_names():
        if not animal.startswith("system.") and not animal.startswith("recipes") and not animal.startswith("images"):
            animals.append(animal)
    return animals

@app.route("/")
def show_macros():
    return render_template("homepage.html")
    
@app.route("/meats")
def show_meats():
    animals = mongo.db["images"].find()
    return render_template("meats.html", animals=animals)
    
@app.route("/recipes")
def show_recipes():
    return render_template("recipes.html")
    
@app.route("/add_animal", methods=["POST", "GET"])
def add_animal():
    if request.method == "POST":
        image = request.files['image']  
        image_string = base64.b64encode(image.read()).decode("utf-8")
        form_values = request.form.to_dict()
        form_values["image"] = "data:image/png;base64," + image_string
        animal_name = request.form["animal_name"]
        mongo.db.create_collection(animal_name)
        images = form_values["image"]
        mongo.db["images"].insert_one(form_values)
        return redirect("/meats")
    else:
        return render_template("add_meat.html")

@app.route("/<animal_name>/cuts") 
def show_cuts(animal_name):
    animal = mongo.db[animal_name].find()
    return render_template("cuts.html", animal=animal)
 
        
@app.route("/<animal_name>/add_cut", methods=["POST", "GET"])
def add_cut(animal_name):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db[animal_name].insert_one(form_values)
        return redirect(url_for("show_cuts", animal_name=animal_name))
    else: 
        return render_template("add_cut.html")
        
    


if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
