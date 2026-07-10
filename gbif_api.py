import requests


def get_gbif_info(gbif_id):

    if not gbif_id:
        return None

    url = f"https://api.gbif.org/v1/species/{gbif_id}"

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        return {

        "scientific_name": data.get("scientificName", "Unknown"),

        "canonical_name": data.get("canonicalName", "Unknown"),

        "kingdom": data.get("kingdom", "Unknown"),

        "phylum": data.get("phylum", "Unknown"),

        "class": data.get("class", "Unknown"),

        "order": data.get("order", "Unknown"),

        "family": data.get("family", "Unknown"),

        "genus": data.get("genus", "Unknown"),

        "species": data.get("species", "Unknown"),

        "rank": data.get("rank", "Unknown"),

        "taxonomic_status": data.get("taxonomicStatus", "Unknown"),

        "origin": data.get("origin", "Unknown"),

        "published_in": data.get("publishedIn", "Unknown")

    }

    except Exception as e:

        print("GBIF Error:", e)

        return None