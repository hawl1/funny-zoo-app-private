"""
Very Epic Zoo App
"""

import random

from flask import Flask, render_template, redirect, url_for, request
from peewee import SqliteDatabase, Model, CharField, IntegerField

app = Flask(__name__)

# Create a unique database name using the current time
DB_NAME = "databasezoo.db"

# Define a SQLite database
db = SqliteDatabase(DB_NAME)


class Animal(Model):
    """
    Animal model representing individual animals in the zoo.
    """

    name = CharField()
    gender = CharField()
    id = IntegerField(primary_key=True)

    class Meta:
        """
        Tells that this model is into that database.
        """

        database = db


# Connect to the database
db.connect()

# Create tables
db.create_tables([Animal])


# Close the database connection after each request
@app.teardown_appcontext
def close_db(exception):
    """
    Close the database connection.
    """

    if not db.is_closed():
        db.close()


@app.route("/")
def home():
    """
    Render the home page with a list of animals.
    """
    animals = Animal.select()
    return render_template("index.html", title="Zoo App", animals=animals)


@app.route("/add")
def add_page():
    """
    Animal adding page.
    """
    return render_template("add.html", title="Add Animals")


@app.route("/remove")
def remove_page():
    """
    Remove page for animals.
    """

    return render_template("remove.html", title="Remove Animals")


@app.route("/breed")
def breed_page():
    """
    Page for breeding animals
    """

    return render_template("breed.html", title="Breed Animals")


@app.route("/api/breed")
def breed():
    """
    Breed two animals and create a new one.
    """

    # Get parent IDs from query parameters
    parent1_id = request.args.get("parent1")
    parent2_id = request.args.get("parent2")

    # Retrieve the selected parent animals
    parent1 = Animal.get(Animal.id == parent1_id)
    parent2 = Animal.get(Animal.id == parent2_id)

    # Create a new animal with a random gender
    Animal.create(
        name=f"{parent1.name[:3]}{parent2.name[-3:]}",
        gender=random.choice(["Male", "Female"]),
    )

    return redirect(url_for("home"))


@app.route("/api/add")
def add():
    """
    Add a new animal with specified gender and name.
    """

    # Get the gender and name from the query parameters
    gender = request.args.get("gender", "Female")
    name = request.args.get("name", f"New Animal {random.randint(1, 100)}")

    Animal.create(name=name, gender=gender)

    return redirect(url_for("home"))


from flask import request


@app.route("/api/remove")
def remove():
    """
    Remove an animal by its ID.
    """
    animal_id = request.args.get("animal_id")

    if animal_id:
        Animal.delete().where(Animal.id == int(animal_id)).execute()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
