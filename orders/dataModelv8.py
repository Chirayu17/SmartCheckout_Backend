from PIL import Image
from torchvision import transforms
import torch
from ultralytics import YOLO
import json


model = YOLO('yolov8m.pt')
results = model.predict("/Users/cgupta/Documents/smartcheckoutv3/SmartCheckout_Backend/Fruits/Apple.jpeg")
result = results[0]
print("result->", result)
len(result.boxes)
box = result.boxes[0]

print("Object type:", box.cls)
print("Coordinates:", box.xyxy)
print("Probability:", box.conf)

cords = box.xyxy[0].tolist()
class_id = box.cls[0].item()
conf = box.conf[0].item()
print("Object type:", class_id)
print("Coordinates:", cords)
print("Probability:", conf)

cords = box.xyxy[0].tolist()
cords = [round(x) for x in cords]
class_id = result.names[box.cls[0].item()]
conf = round(box.conf[0].item(), 2)
print("Object type:", class_id)
print("Coordinates:", cords)
print("Probability:", conf)
# image_file = "/Users/cgupta/Documents/smartcheckoutv3/SmartCheckout_Backend/Fruits/Apple Fuji (Seb).jpeg"
# image = Image.open(image_file)
# resize_transform = transforms.Resize((416, 416))  # Resize image to the desired dimensions
# image = resize_transform(image)
# image = transforms.ToTensor()(image).unsqueeze(0)

# results = model(image)
# # Extract the bounding boxes, class labels, and probabilities
# bboxes = results.xyxy[0][:, :4].tolist()
# labels = results.names[0][results.pred[0][:, -1].long()].tolist()
# scores = results.pred[0][:, 4].tolist()
# # Combine the labels and probabilities into predictions
# predictions = [{"label": label, "score": score} for label, score in zip(labels, scores)]
# # Process the results and count the fruits
# fruit_count = len(predictions)
# # Return the results as a JSON response
# print(json({"fruit_count": fruit_count, "‘fruit_predictions’": predictions}))

