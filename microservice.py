from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def search():
    body = request.get_json(silent=True)

    # Validate request body
    if not body:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    data = body.get("data")
    keyword = body.get("keyword")
    category = body.get("category")

    # Validate that data is present and is a list
    if data is None:
        return jsonify({"error": "Missing required field: 'data' (array of items)."}), 400
    if not isinstance(data, list):
        return jsonify({"error": "'data' must be a JSON array."}), 400

    # Validate that at least one filter is provided
    if keyword is None and category is None:
        return jsonify({"error": "At least one of 'keyword' or 'category' must be provided."}), 400

    results = data

    # Apply keyword filter (case-insensitive, searches name and description)
    if keyword is not None:
        keyword_lower = keyword.lower()
        results = [
            item for item in results
            if keyword_lower in str(item.get("name", "")).lower()
            or keyword_lower in str(item.get("description", "")).lower()
        ]

    # Apply category filter (exact match, case-insensitive)
    if category is not None:
        category_lower = category.lower()
        results = [
            item for item in results
            if str(item.get("category", "")).lower() == category_lower
        ]

    return jsonify({"results": results}), 200


if __name__ == "__main__":
    print("Search/Filter Microservice running on http://localhost:5003")
    app.run(port=5003)
