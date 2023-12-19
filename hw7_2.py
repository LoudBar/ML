import cv2
import numpy as np
import pygame
import pytesseract


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


def predict_number():
    pygame.image.save(screen, 'drawn_number.png')
    image = cv2.imread('drawn_number.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, black_and_white = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    black_and_white = cv2.morphologyEx(black_and_white, cv2.MORPH_CLOSE, kernel)

    result = pytesseract.image_to_string(black_and_white,
                                         config='--oem 3 --psm 10 -c tessedit_char_whitelist=-0123456789')
    result = result.strip()
    print(result)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    black = (0, 0, 0)
    white = (255, 255, 255)

    drawing = False
    last_pos = (0, 0)
    radius = 15
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
                    predict_number()
                if event.key == pygame.K_RSHIFT:
                    screen.fill(white)
            draw(event)
            pygame.display.update()