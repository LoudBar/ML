import os

import pygame
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

model = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10 output neurons for digits 0-9
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

model.save('handwritten_integer_recognition_model.model')
model = models.load_model('handwritten_integer_recognition_model.model')

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'\nTest accuracy: {test_acc}')

def draw(event):
    global drawing, last_pos
    if event.type == pygame.MOUSEBUTTONDOWN:
        drawing = True
        last_pos = event.pos
    elif event.type == pygame.MOUSEMOTION:
        if drawing:
            pygame.draw.circle(screen, black, event.pos, radius)
            pygame.draw.line(screen, black, event.pos, last_pos, 2 * radius)
            last_pos = event.pos
    elif event.type == pygame.MOUSEBUTTONUP:
        drawing = False

def segment_digits(image_path, padding_size=15):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    digit_images = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        digit_region = image[y:y + h, x:x + w]

        digit_region_with_padding = cv2.copyMakeBorder(digit_region, padding_size * 3, padding_size * 3, padding_size * 2, padding_size * 2, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        digit_region_final = cv2.resize(digit_region_with_padding, (28, 28), interpolation=cv2.INTER_AREA)


        # Append the digit image to the list
        digit_images.append(digit_region_final)

        digit_filename = os.path.join("./", f"digit_{i}.png")
        cv2.imwrite(digit_filename, digit_region_final)

    return digit_images

def predict_number():
    digit_images = segment_digits(f"number.png")

    # Recognize each digit using the digit recognition model
    recognized_digits = []
    for i, digit_image in enumerate(digit_images):
        current_img = cv2.imread(os.path.join("./", f"digit_{i}.png"))[:, :, 0]
        img = np.invert(np.array([current_img]))

        prediction = model.predict(img)
        recognized_digit = np.argmax(prediction)
        recognized_digits.append(recognized_digit)

    # Combine the recognized digits to get the final result
    result = int("".join(map(str, recognized_digits)))
    print(f"Recognized Number: {result}")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    black = (0, 0, 0)
    white = (255, 255, 255)

    drawing = False
    last_pos = (0, 0)
    radius = 5
    screen.fill(color="#FFFFFF")
    pygame.display.update()
    is_active = True
    is_pressed = False
    count_of_keyup = 0

    while is_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_active = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    pygame.image.save(screen, "./number.png")
                    predict_number()
                if event.key == pygame.K_RSHIFT:
                    screen.fill(white)
            draw(event)
            pygame.display.update()