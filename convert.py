import json

# Read the metadata file
with open("export/metadata.json", "r") as f:
    data = json.load(f)

# Process each media item
for item in data["media_items"]:
    # Initialize lists for bboxes and categories
    bboxes = []
    categories = []

    # Process each metadata item (object detection annotation)
    for metadata in item["metadata_items"]:
        if metadata["type"] == "object_label":
            # Extract bbox (assuming format is [x, y, width, height])
            bbox = metadata["properties"]["bbox"]
            bboxes.append(bbox)

            # Map category name to index (you'll need to customize this mapping)
            category_mapping = {
                "vest": 0,
                # Add other categories as needed
            }
            category = category_mapping.get(metadata["properties"]["category_name"], 0)
            categories.append(category)

    # Create output format
    output = {
        "file_name": item["file_name"],
        "objects": {"bbox": bboxes, "category": categories},
    }

    # Print as JSON string without newlines within the object
    print(json.dumps(output))
