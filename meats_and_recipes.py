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

@app.route("/")
def show_macros():
    return render_template("homepage.html")
    
@app.route("/meats")
def show_meats():
    animals = mongo.db["images"].find()
    return render_template("meats.html", animals=animals)
    
@app.route("/vegtables")
def show_vegtables():
    vegtables = mongo.db["images"].find({"vegtable_name" : "Carrot"})
    return render_template("vegtables.html", vegtables=vegtables)
    
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
        images = form_values["image"]
        mongo.db["images"].insert_one(form_values)
        return redirect("/meats")
    else:
        
        return render_template("add_meat.html")


@app.route("/<animal_name>/cuts") 
def show_cuts(animal_name):
    animal = mongo.db["animals"].find({"animal_name" : animal_name})
    return render_template("cuts.html", animal=animal)
 
        
@app.route("/<animal_name>/add_cut", methods=["POST", "GET"])
def add_cut(animal_name):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["animals"].insert_one(form_values)
        return redirect(url_for("show_cuts", animal_name=animal_name))
    else: 
        return render_template("add_cut.html", animal_name=animal_name)
        
        
@app.route("/add_vegtable", methods=["POST", "GET"])
def add_vegtable():
    if request.method == "POST":
        image = request.files['image']  
        image_string = base64.b64encode(image.read()).decode("utf-8")
        form_values = request.form.to_dict()
        form_values["image"] = "data:image/png;base64," + image_string
        vegtable_name = request.form["vegtable_name"]
        images = form_values["image"]
        mongo.db["images"].insert_one(form_values)
        return redirect("/vegtables")
    else:
        
        return render_template("add_vegtable.html")
        

@app.route("/<vegtable_name>/vegtableType") 
def show_vegtableType(vegtable_name):
    vegtable = mongo.db["vegtables"].find({"vegtable_name" : vegtable_name})
    return render_template("vegtableType.html", vegtables=vegtable)
 
        
@app.route("/<vegtable_name>/add_vegtableType", methods=["POST", "GET"])
def add_vegtableType(vegtable_name):
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db["vegtables"].insert_one(form_values)
        return redirect(url_for("show_vegtableType", vegtable_name=vegtable_name))
    else: 
        return render_template("add_vegtableType.html", vegtable_name=vegtable_name)
    


if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
