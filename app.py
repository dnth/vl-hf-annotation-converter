import json

import gradio as gr


def process_metadata(file):
    # Read the uploaded JSON file
    with open(file.name, "r") as f:
        data = json.load(f)

    # First pass: collect all unique categories
    unique_categories = set()
    for item in data["media_items"]:
        for metadata in item["metadata_items"]:
            if metadata["type"] == "object_label":
                unique_categories.add(metadata["properties"]["category_name"])

    # Create category mapping dynamically
    category_mapping = {cat: idx for idx, cat in enumerate(sorted(unique_categories))}

    # Create a formatted string of the mapping
    mapping_str = "\n".join([f"{cat}: {idx}" for cat, idx in category_mapping.items()])

    results = []
    # Process each media item
    for item in data["media_items"]:
        # Initialize lists for bboxes and categories
        bboxes = []
        categories = []

        # Process each metadata item
        for metadata in item["metadata_items"]:
            if metadata["type"] == "object_label":
                bbox = metadata["properties"]["bbox"]
                bboxes.append(bbox)

                category = category_mapping.get(
                    metadata["properties"]["category_name"], 0
                )
                categories.append(category)

        # Create output format
        output = {
            "file_name": item["file_name"],
            "objects": {"bbox": bboxes, "category": categories},
        }
        results.append(json.dumps(output))

    # Return both results and mapping
    return "\n".join(results), mapping_str


def save_text(text):
    # Create a temporary file to save the output
    temp_file = "metadata.jsonl"
    with open(temp_file, "w") as f:
        f.write(text)
    return temp_file


# Create Gradio interface
with gr.Blocks(title="VL-HF Annotations Converter") as iface:
    gr.Markdown("# VL-HF Annotations Converter")
    gr.Markdown(
        "Upload a JSON annotations file exported from Visual Layer and get a JSONL file to be used in Hugging Face AutoTrain."
    )

    with gr.Row():
        input_file = gr.File(label="Upload JSON file exported from Visual Layer")

    with gr.Row():
        output_text = gr.Textbox(label="Converted JSONL output", lines=10, scale=3)
        mapping_text = gr.Textbox(label="Category Mapping", lines=10)

    with gr.Row():
        download_btn = gr.DownloadButton(
            label="Download JSONL", value="metadata.jsonl", interactive=True
        )

    # Connect the components
    output = input_file.change(
        fn=process_metadata, inputs=[input_file], outputs=[output_text, mapping_text]
    ).then(  # Chain the save operation immediately after processing
        fn=save_text, inputs=[output_text], outputs=[download_btn]
    )

if __name__ == "__main__":
    iface.launch()
