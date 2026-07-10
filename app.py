from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from plantnet_api import identify_plant
from gbif_api import get_gbif_info
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- Home ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- Serve Uploaded Images ---------------- #

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
app.config["UPLOAD_FOLDER"],
filename
)


# ---------------- Predict ---------------- #

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No Image Found"

    file = request.files["image"]

    if file.filename == "":
        return "No File Selected"

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    result = identify_plant(filepath)

    if result is None:
        return "PlantNet API Error"

    if len(result["results"]) == 0:
        return "No Plant Detected"

    best = result["results"][0]

    gbif_id = None

    if "gbif" in best and best["gbif"]:
        gbif_id = best["gbif"].get("id")

    gbif = get_gbif_info(gbif_id)
    # Common Name
    common_names = best["species"].get("commonNames", [])
    flower_name = common_names[0] if common_names else "Unknown"

    # Scientific Name
    scientific_name = best["species"].get(
        "scientificNameWithoutAuthor",
        "Unknown"
    )

    # Family
    family = best["species"].get(
        "family",
        {}
    ).get(
        "scientificNameWithoutAuthor",
        "Unknown"
    )

    # Genus
    genus = best["species"].get(
        "genus",
        {}
    ).get(
        "scientificNameWithoutAuthor",
        "Unknown"
    )

    # Confidence
    confidence = round(best["score"] * 100, 2)

    # Top Predictions
    predictions = []

    for item in result["results"][:5]:

        predictions.append({

            "name": item["species"].get(
                "scientificNameWithoutAuthor",
                "Unknown"
            ),

            "score": round(item["score"] * 100, 2)

        })

    return render_template(
    "index.html",

    flower_name=flower_name,

    scientific_name=scientific_name,

    family=family,

    genus=genus,

    common_name=flower_name,

    confidence=confidence,

    predictions=predictions,

    image=filename,
    gbif=gbif
)


# ---------------- Run ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)