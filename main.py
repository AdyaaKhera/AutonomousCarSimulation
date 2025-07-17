import pygame
pygame.init()

#window setup
width, height = 500, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Simulation")

#road setup
road_width = 400
road_color = (54, 69, 79)  
lane_color = (255, 255, 255)  
lane_count = 5

#car setup
car_width, car_height = 40, 80
car_color = (255, 105, 97)  
car_x = width // 2 - car_width // 2
car_y = height // 2
car_speed = 5

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((119, 221, 119)) 

    road_left = (width - road_width) // 2

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        car_y -= car_speed

    if keys[pygame.K_DOWN]:
        car_y += car_speed

    if keys[pygame.K_LEFT]:
        car_x -= car_speed
        if car_x < road_left:
            car_x = road_left

    if keys[pygame.K_RIGHT]:
        car_x += car_speed
        if car_x + car_width > road_left + road_width:
            car_x = road_left + road_width - car_width

    #road in the center
    pygame.draw.rect(screen, road_color, (road_left, 0, road_width, height))

    #lane lines
    lane_width = road_width / lane_count
    for i in range(0, lane_count+1):
        line_x = road_left + int(i * lane_width)
        pygame.draw.line(screen, lane_color, (line_x, 0), (line_x, height), 5)

    car_body = pygame.Rect(car_x, car_y, car_width, car_height)
    pygame.draw.rect(screen, car_color, car_body)

    pygame.display.flip()

pygame.quit()
