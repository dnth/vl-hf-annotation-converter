import matplotlib.patches as patches
import matplotlib.pyplot as plt
import torch
from PIL import Image
from transformers import DetrForObjectDetection, DetrImageProcessor

# Load image
image = Image.open("data/train/006251_jpg.rf.a583fbabac5449aa982bb8246c4d849c.jpg")

model_name = "./autotrain-detr-resnet-50"
processor = DetrImageProcessor.from_pretrained(model_name)
model = DetrForObjectDetection.from_pretrained(model_name)

# Prepare inputs
inputs = processor(images=image, return_tensors="pt")

# Run inference
outputs = model(**inputs)

# Post-process outputs
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs, target_sizes=target_sizes, threshold=0.70
)[0]

# Create figure and axes
fig, ax = plt.subplots(1)
ax.imshow(image)

# Draw bounding boxes
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]

    # Create a Rectangle patch
    rect = patches.Rectangle(
        (box[0], box[1]),
        box[2] - box[0],
        box[3] - box[1],
        linewidth=2,
        edgecolor="r",
        facecolor="none",
    )

    # Add the rectangle to the plot
    ax.add_patch(rect)

    # Add label and score
    plt.text(
        box[0],
        box[1] - 5,
        f"{model.config.id2label[label.item()]}: {round(score.item(), 3)}",
        color="red",
        fontsize=8,
        bbox=dict(facecolor="white", alpha=0.8),
    )

# Remove axes
plt.axis("off")

# Show the plot
plt.show()

# Print results
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
        f"Detected {model.config.id2label[label.item()]} with confidence {round(score.item(), 3)} at location {box}"
    )
