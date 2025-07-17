import pygame
pygame.init()

# Window setup
width, height = 500, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Simulation")

# Road setup
road_width = 400
road_color = (54, 69, 79)
lane_color = (255, 255, 255)
lane_count = 5

# Car setup
car_width, car_height = 40, 80
car_color = (255, 105, 97)
car_x = width // 2 - car_width // 2
car_y = height - 150  # Fixed position near the bottom

car_speed = 3  # Scroll speed

# Lane dash setup
dash_length = 20
space_length = 20
lane_offset = 0  # Scroll controller

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((119, 221, 119)) 

    road_left = (width - road_width) // 2

    # Scroll lane lines upward
    lane_offset -= car_speed
    if lane_offset <= -(dash_length + space_length):
        lane_offset = 0

    # Lane changing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
        if car_x < road_left:
            car_x = road_left

    if keys[pygame.K_RIGHT]:
        car_x += car_speed
        if car_x + car_width > road_left + road_width:
            car_x = road_left + road_width - car_width

    # Draw road
    pygame.draw.rect(screen, road_color, (road_left, 0, road_width, height))

    lane_width = road_width / lane_count
    for i in range(1, lane_count):
        line_x = road_left + int(i * lane_width)
        y = -lane_offset 
        while y < height:
            pygame.draw.line(screen, lane_color, (line_x, y), (line_x, y + dash_length), 5)
            y += dash_length + space_length

    # Draw stationary car
    car_body = pygame.Rect(car_x, car_y, car_width, car_height)
    pygame.draw.rect(screen, car_color, car_body)

    pygame.display.flip()

pygame.quit()
