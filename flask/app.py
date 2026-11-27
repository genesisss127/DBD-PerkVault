
import requests

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dbd-perkvault"

API_URL = "http://127.0.0.1:8000/perks/"


# ---------------------------------------------------------------------------
# Survivor Perks
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    response = requests.get(API_URL)
    perks = response.json()
    return render_template("index.html", perks=perks)


@app.route("/perks/<int:perk_id>")
def details(perk_id):
    response = requests.get(f"{API_URL}{perk_id}")
    if response.status_code == 404:
        return "Perk not found", 404

    perk = response.json()
    return render_template("details.html", perk=perk)


@app.route("/perks/create", methods=["GET", "POST"])
def create_perk():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "character": request.form["character"],
            "description": request.form["description"],
            "icon": request.form.get("icon") or None
        }

        response = requests.post(API_URL, json=data)

        if response.status_code == 201:
            flash("Perk created successfully!")
            return redirect(url_for("index"))

        flash("Error creating perk.")

    return render_template("form.html", perk=None)


@app.route("/perks/<int:perk_id>/edit", methods=["GET", "POST"])
def update_perk(perk_id):
    response = requests.get(f"{API_URL}{perk_id}")

    if response.status_code == 404:
        return "Perk not found", 404

    perk = response.json()

    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "character": request.form["character"],
            "description": request.form["description"],
            "icon": request.form.get("icon") or None
        }

        response = requests.put(f"{API_URL}{perk_id}", json=data)

        if response.status_code == 200:
            flash("Perk updated successfully!")
            return redirect(url_for("details", perk_id=perk_id))

        flash("Error updating perk.")

    return render_template("form.html", perk=perk)


@app.route("/perks/<int:perk_id>/delete", methods=["POST"])
def delete_perk(perk_id):
    response = requests.delete(f"{API_URL}{perk_id}")

    if response.status_code == 204:
        flash("Perk deleted successfully!")
    else:
        flash("Error deleting perk.")

    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Archive Navigation
# ---------------------------------------------------------------------------

@app.route("/home")
def home():
    return render_template("coming_soon.html", category="HOME")


@app.route("/killer-perks")
def killer_perks():
    return render_template("coming_soon.html", category="KILLER PERKS")


@app.route("/maps")
def maps():
    return render_template("coming_soon.html", category="MAPS")


@app.route("/items")
def items():
    return render_template("coming_soon.html", category="ITEMS")


@app.route("/addons")
def addons():
    return render_template("coming_soon.html", category="ADD-ONS")


@app.route("/offerings")
def offerings():
    return render_template("coming_soon.html", category="OFFERINGS")


@app.route("/events")
def events():
    return render_template("coming_soon.html", category="EVENTS")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
