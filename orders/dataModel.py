# import torch
# from PIL import Image

# # Install YOLOv5 package

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# # # Set the device to CPU

# device = torch.device('cpu')
# model = model.to(device)



# # Detect fruits



# def ImageDetection(image_data):

# #     model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# # # Set the device to CPU
# #     device = torch.device('cpu')
# #     model = model.to(device)
#     results = model(image_data)
  
#     detectedData = {"Fruits" : {}}
#     fruit_counts = {}
#     for detection in results.pandas().xyxy[0].iterrows():
     
#         fruit_name = detection[1]['name']
#         if fruit_name not in fruit_counts:
#             fruit_counts[fruit_name] = 0
#         fruit_counts[fruit_name] += 1

#     print("fruit_count->", fruit_counts)
#     if not fruit_counts:
#          detectedData = {}
#     else:
#         for fruit_name, count in fruit_counts.items():
#             detectedData["Fruits"][fruit_name] = count

#     print(detectedData)
#     return detectedData