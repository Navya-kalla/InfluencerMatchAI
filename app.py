from flask import Flask, render_template, request
import pandas as pd

app = Flask(
    __name__,
    template_folder="website/templates",
    static_folder="website/static"
)
df = pd.read_csv("dataset/influencer_clustered.csv")

@app.route("/")
def home():
    categories = sorted(df["Category"].unique())
    return render_template("index.html", categories=categories)

@app.route("/recommend", methods=["POST"])
def recommend():

    budget = int(request.form["budget"])
    category = request.form["category"]

    filtered = df[
        (df["Category"] == category) &
        (df["Collab_Cost"] <= budget)
    ]

    recommendations = filtered.sort_values(
        by=["Engagement_Rate", "Followers"],
        ascending=False
    ).head(5)

    return render_template(
        "result.html",
        tables=recommendations.to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)