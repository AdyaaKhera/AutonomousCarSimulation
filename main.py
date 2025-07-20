import pygame, random

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

# Obstacle cars setup
obstacle_width, obstacle_height = 40, 80

obstacles = []
obstacle_spawn_delay = random.randint(30, 90)
obstacle_spawn_timer = 0

car_speed = 3  # Scroll speed

score = 0

# Lane dash setup
dash_length = 20
space_length = 20
lane_offset = 0 

font = pygame.font.SysFont(None, 40)
game_over = False

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
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

        # Draw obstacle at intervals
        obstacle_spawn_timer += 1
        if obstacle_spawn_timer >= obstacle_spawn_delay:
            obstacle_spawn_timer = 0
            obstacle_spawn_delay = random.randint(30, 90)
            num_obs_to_spawn = random.choices([1, 2], weights=[0.8, 0.2])[0]

            # Mark occupied lanes 
            occupied_lanes = set()
            for obs in obstacles:
                obs_lane_index = int((obs[0] - road_left) // (road_width / lane_count))
                if obs[1] < obstacle_height * 2:  # Check if obstacle is near top
                    occupied_lanes.add(obs_lane_index)

            available_lanes = [i for i in range(lane_count) if i not in occupied_lanes]

            # Spawn obstacles only in free lanes 
            if available_lanes:
                num_to_spawn = min(len(available_lanes), random.choices([1, 2], weights=[0.8, 0.2])[0])

                for _ in range(num_to_spawn):
                    lane_index = random.choice(available_lanes)
                    available_lanes.remove(lane_index)  # Mark lane as occupied now
                    lane_x = road_left + int(lane_index * (road_width / lane_count)) + (road_width / lane_count - obstacle_width) // 2
                    speed = random.randint(4, 6)
                    color = random.choice([
                        (176, 224, 168),
                        (174, 198, 207), 
                        (230, 230, 250),
                        (255,223,186),
                        (255,255,186)
                    ])
                    obstacles.append([lane_x, -obstacle_height, speed, color])

        for obstacle in obstacles[:]:
            obstacle[1] += obstacle[2] # Move down - add to y coordinate
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            pygame.draw.rect(screen, obstacle[3], obstacle_rect)
            if obstacle_rect.colliderect(pygame.Rect(car_x, car_y, car_width, car_height)):
                game_over = True
            if obstacle[1] > height:
                obstacles.remove(obstacle)
                score += 1

        # --- LIDAR SENSORS ---
        lidar_rays = [-45, -30, -15, 0, 15, 30, 45]  
        lidar_max_range = random.randint(100, 150)  
        start_x = car_x + car_width // 2
        start_y = car_y

        for angle in lidar_rays:
            distance = 0
            hit = False
            rad = (angle / 180) * 3.14159
            dx, dy = 0, 0  

            while distance < lidar_max_range and not hit:
                distance += 1
                dx = int(distance * pygame.math.Vector2(0, -1).rotate(angle).x)
                dy = int(distance * pygame.math.Vector2(0, -1).rotate(angle).y)
                check_x = start_x + dx
                check_y = start_y + dy

                if check_x < road_left or check_x > road_left + road_width or check_y < 0:
                    hit = True
                    break

                # Obstacle check
                for obstacle in obstacles:
                    obs_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
                    if obs_rect.collidepoint(check_x, check_y):
                        hit = True
                        break

            fade = 255 - int((distance / lidar_max_range) * 180)
            fade = max(0, min(255, fade))
            ray_color = (fade, fade, 0) 

            # Draw the ray
            pygame.draw.line(screen, ray_color, (start_x, start_y), (start_x + dx, start_y + dy), 2)

        # Draw stationary car
        car_body = pygame.Rect(car_x, car_y, car_width, car_height)
        pygame.draw.rect(screen, car_color, car_body)

        # Display car overtake number
        score_bg_rect = pygame.Rect(0, 0, 280, 50) 
        pygame.draw.rect(screen, (255, 255, 255), score_bg_rect, border_radius=5)  
        score_text = font.render(f"Cars overtaken: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    else:
        # Game over
        screen.fill((50, 50, 50))
        game_over_text = font.render("COLLISION!", True, (255, 0, 0))
        score_text = font.render(f"Cars overtaken: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (width // 2 - 100, height // 2 - 40))
        screen.blit(score_text, (width // 2 - 130, height // 2 + 10))
        pygame.display.flip()

pygame.quit()
