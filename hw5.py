import pygame
from sklearn import svm


RADIUS = 5


def draw():
    model = svm.SVC(kernel='linear')
    points = []
    classes = []
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    screen.fill(color='white')
    pygame.display.update()
    colors = ['red', 'blue', 'black', 'yellow']
    play = True
    learning_mode = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if learning_mode:
                    pygame.draw.circle(screen, color=colors[0], center=event.pos, radius=RADIUS)
                    pygame.display.update()
                    points.append(list(event.pos))
                    classes.append(0)
                else:
                    c = model.predict([event.pos])
                    print(c)
                    pygame.draw.circle(screen, color=colors[c[0]], center=event.pos, radius=RADIUS)
                    pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if learning_mode:
                    pygame.draw.circle(screen, color=colors[1], center=event.pos, radius=RADIUS)
                    pygame.display.update()
                    points.append(list(event.pos))
                    classes.append(1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                learning_mode = False
                print(points)
                model.fit(points, classes)
                coef = model.coef_[0]
                print(model.coef_, model.intercept_)
                start_pos = [0, model.intercept_[0] / -coef[1]]
                print(start_pos)
                end_pos = [800, coef[0] / -coef[1] * 800 + model.intercept_[0] / -coef[1]]
                print(end_pos)
                pygame.draw.line(screen, color='black', start_pos=start_pos, end_pos=end_pos)
                pygame.display.update()


if __name__ == '__main__':
    draw()