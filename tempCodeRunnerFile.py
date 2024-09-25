# from ultralytics import YOLO,settings
# from PIL import Image
# import cv2


# model = YOLO("best.pt")

# #im2 = cv2.imread("TEST_IMAGE\images.jpg") 
# model.predict("TEST_IMAGE\images.jpg",save=True,show=True) 
#  # save predictions as labels
# #print(results)
# # print(len(results))
# # path =results[0].path
# # dir=results[0].save_dir
# # print(path,dir)
# # print(type(path))
# # print(len(path))
# #dir=results[10]


# # nameImage =results[0].path
# # path=results[0].save_dir
# # full_path_detect_image=path +'\\'+ nameImage


# # image = cv2.imread(full_path_detect_image)

# # text = "clip producer"
# # #position = (50, 50)  # تحديد موقع النص على الصورة
# # font = cv2.FONT_HERSHEY_SIMPLEX  # تحديد نوع الخط
# # font_scale = 1  # حجم الخط
# # color = (0, 0, 255)  # لون النص في الترتيب (BGR)
# # thickness = 2  # سمك الخط
# # # حساب أبعاد الصورة
# # image_height, image_width, _ = image.shape
# # text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

# # # حساب موقع النص في وسط الصورة
# # text_x = (image_width - text_size[0]) // 2
# # text_y = (image_height + text_size[1]) // 2

# # # وضع النص في الصورة
# # cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness)


# # cv2.imwrite(full_path_detect_image, image)
         

import numpy as np
import random

def distance(city1, city2):
    return np.linalg.norm(city1 - city2)

def total_distance(city_order, cities):
    total = 0
    for i in range(len(city_order) - 1):
        total += distance(cities[city_order[i]], cities[city_order[i + 1]])
    total += distance(cities[city_order[-1]], cities[city_order[0]])
    return total

def acceptance_probability(current_cost, new_cost, temperature):
    if new_cost < current_cost:
        return 1.0
    return np.exp((current_cost - new_cost) / temperature)

def simulated_annealing(cities, initial_order, num_iterations, initial_temperature, cooling_rate):
    current_order = initial_order
    current_cost = total_distance(current_order, cities)
    best_order = current_order.copy()
    best_cost = current_cost
    temperature = initial_temperature

    for i in range(num_iterations):
        new_order = current_order.copy()
        index1 = random.randint(0, len(cities) - 1)
        index2 = random.randint(0, len(cities) - 1)
        new_order[index1], new_order[index2] = new_order[index2], new_order[index1]
        new_cost = total_distance(new_order, cities)

        if acceptance_probability(current_cost, new_cost, temperature) > random.random():
            current_order = new_order
            current_cost = new_cost

        if current_cost < best_cost:
            best_order = current_order
            best_cost = current_cost

        temperature *= cooling_rate

    return best_order, best_cost

# Example usage
cities = np.array([[0, 0], [1, 2], [3, 1], [2, 3]])
initial_order = [0, 1, 2, 3]
num_iterations = 1000
initial_temperature = 1000.0
cooling_rate = 0.003

best_order, best_cost = simulated_annealing(cities, initial_order, num_iterations, initial_temperature, cooling_rate)
print("Best order:", best_order)
print("Best cost:", best_cost) 