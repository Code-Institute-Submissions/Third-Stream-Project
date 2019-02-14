# Maacro Tracker

Data Centric Development Project - Code Institute

Macro Tracker is an app where users can easily check the nutrional information of certain foods, and can can put together meals that will show them the total calories and macro-nutrionents of the dish. 
The app allows users to:

* Add meats with an image
* Add/ edit meat cuts and their nutrional values
* Add/edit vegetables and their nutrional values
* Create a meal

It was built in Python3 using the Flask microframework.

A live version can be found [Here](https://dmongey-meat-nutrition-recipes.herokuapp.com/).

## UX

The colour theme is primarily indian red and white. The indian red matches with the fruit in the background to make it easy on the eye. The colour red is used for some buttons to make them more prominent on the screen. The overall layout is quite simple and users can access all parts of the site by using any of the links on the navigation bar.

The homepage gives a brief description of the app, which will allow the user to then use the app with ease.

### User Stories:

When a user enters the site, the will immediately have an understanding of the purpose of the app after reading the brief description. They can then easily navigate around the site using the appropriate links in the navbar and buttons on each page. They can proceed to easily view, add or edit any food that that they wish. 

If I want to add a new food, the forms are very easy to find and use with a minimalist design, another feature that makes for a positive user experience.

### Wireframing
    
Wireframes were made on pen and paper and can be found in the wireframe folder in the main project file.

## Features

### Existing Features

* Easy navigation around the site via the navbar.
* Cards representing each food and meal type.
* A collapsible list to display meat nutritional information.
* A card reveal feature to display vegetable nutrional information.
* Various forms allow users to add/edit meats, cuts, vegetables and meals.

### Features left to implement

* Currently when adding a food to a meal, all values are per 100g. I would like to change this so the user can specify how much of each food   will be in a recipe.

## Technologies Used

* HTML
* CSS
* Bootstrap
* Materialize - front-end framework used due to its user experience focus and ease of use.
* JavaScript
* JQuery - used to simplify DOM manipulation.
* Python 3
* Flask - Flask is a microframework for Python and was used due to its flexibility and simplicity, making it a suitable framework for this     app.
* MongoDB - MongoDB is a document database
* mLab – Database-as-a-Service for MongoDB, used to store goals and their data

## Testing

The site was tested on 15" and 13" laptop screens and on the following phone screens sizes: iPhone 5s/6/7/8/X; Galaxy S5, Pixel 2; and Pixel 2XL. It was also tested on iPad and iPad Pro screen sizes. The site is responsive and working on all screen sizes.

All testing was performed manually to ensure:

* Links work correctly.
* Form submissions work as intended.
* Model relationships work correctly.
* The site is responsive across all screen sizes and devices.

The following forms are posted correctly and the database is updated accordingly:

* Add Meat
* Add Cut
* Add Vegetable
* Add Meal
* Edit Cut
* Edit Vegetable

The user is redirected to the correct pages after forms are posted. All new food and meal items are displayed placed on the relevent pages.

## Deployment

The site is hosted on heroku.

In order to do this I created a new app on the heroku site and linked to the app via the cloud9 terminal.
I created a Procfile and requirements.txt file which I then pushed to heroku with the main files.
On Heroku I have set the config vars to 0.0.0.0 for the IP address and 5000 for the PORT to enable the site to work.
Heroku will also need config vars for the database name (MONGO_DBNAME) and database uri (MONGO_URI) in order to access and save data.

### Run Locally

To run this site locally, in your terminal enter: git clone https://dmongey101.github.io/Who-am-I/

## Credits

All javascript features were taken from materialize. https://materializecss.com/

### Content

Inspiration for the homapage content came from https://www.myfitnesspal.com/

### Media

* Icons used were obtained from Materialize.
* Background image retrieved from google images.


