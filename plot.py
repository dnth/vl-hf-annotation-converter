import json
import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image


def plot_image_with_bbox(image_path, bboxes, categories):
    """
    Plot an image with its bounding boxes
    Args:
        image_path: Path to the image
        bboxes: List of bounding boxes in format [x, y, width, height]
        categories: List of categories corresponding to each bbox
    """
    # Read image
    img = Image.open(image_path)

    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the image
    ax.imshow(img)

    # Colors for different categories
    colors = ["r", "g", "b", "y"]  # Add more colors if needed

    # Plot each bounding box
    for bbox, category in zip(bboxes, categories):
        x, y, w, h = bbox

        # Create a Rectangle patch
        rect = patches.Rectangle(
            (x, y),
            w,
            h,
            linewidth=2,
            edgecolor=colors[category % len(colors)],
            facecolor="none",
        )

        # Add the patch to the Axes
        ax.add_patch(rect)

        # Add category label
        plt.text(
            x,
            y - 5,
            f"Category: {category}",
            color=colors[category % len(colors)],
            bbox=dict(facecolor="white", alpha=0.7),
        )

    plt.axis("off")
    plt.show()


def main():
    # Get the directory containing the JSONL file
    jsonl_dir = os.path.abspath("data/train/")

    # Read JSONL file using the full path
    jsonl_path = os.path.join(jsonl_dir, "metadata.jsonl")
    with open(jsonl_path, "r") as f:
        for line in f:
            data = json.loads(line)

            # Images are in the same directory as the JSONL file
            image_path = os.path.join(jsonl_dir, data["file_name"])
            bboxes = data["objects"]["bbox"]
            categories = data["objects"]["category"]

            # If there's only one bbox/category, convert to list
            if not isinstance(bboxes[0], list):
                bboxes = [bboxes]
            if not isinstance(categories, list):
                categories = [categories]

            # Plot image with bounding boxes
            try:
                plot_image_with_bbox(image_path, bboxes, categories)

                # Wait for user input before showing next image
                input("Press Enter to continue...")
                plt.close()
            except FileNotFoundError:
                print(f"Image not found: {data['file_name']}")
                continue


if __name__ == "__main__":
    main()
