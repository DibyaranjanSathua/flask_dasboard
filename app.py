"""
File:           app.py
Author:         Dibyaranjan Sathua
Created on:     14/01/21, 8:19 pm
"""
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dbhandler import DBHandler

app = Flask(__name__)


@app.route("/")
def home():
    """ Display the home page """
    db_handler = DBHandler()
    records = db_handler.get_all_potential_records()
    table_headers = list(records[0].keys())
    make_model_records = db_handler.get_all_make_models()
    make_model = defaultdict(list)
    for record in make_model_records:
        make_model[record["make"]].append(record["model"])

    return render_template(
        "home.html", table_headers=table_headers, records=records, make_model=make_model
    )


@app.route("/save-comments", methods=["POST"])
def save_comments():
    """ Save comments to potential deals table """
    potential_deal_id = int(request.form.get("id"))
    action = request.form.get("action")
    if action.lower() == "none":
        action = None
    comments = request.form.get("comments")
    db_handler = DBHandler()
    db_handler.update_by_id(potential_deal_id, action, comments)
    # return redirect(url_for("home"))
    return jsonify({"success": True}), 200


if __name__ == "__main__":
    app.run(debug=True)
