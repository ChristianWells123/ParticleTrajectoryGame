from cmath import sqrt
import sys, pygame, numpy, operator
pygame.init()

#EDITABLE VARIABLES
#==================
#the size of the screen in pixels.
size = width, height = 640, 480
#the color of the background. R, G, B.
background_color = 0, 0, 0
#the color of the trajectory line. R, G, B.
traj_color = 100, 0, 255
#The initial velocity of the trajectory.
launch_veloc = 40
#The gravitational constant of the trajectory.
gravity = 7
#Determines how finely to calculate the trajectory. 
#A lower number is a higher resolution.
time_resolution = .5
#The position in which to start the trajectory.
ball_start_pos = (width/2, 50)
#==================

screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    cursor_pos = pygame.mouse.get_pos()

    #The offset from the cursor to the ball position
    cursor_vector = tuple(map(operator.sub, ball_start_pos, cursor_pos))

    #The angle to use to shoot straight at the cursor
    #cursor_angle = numpy.arctan2(cursor_vector[1], cursor_vector[0])
    
    #reassign variables in order for the equation later to be readable
    x = cursor_vector[0]
    y = cursor_vector[1]
    v = launch_veloc
    launch_angle = 0

    #Do this to avoid dividing by zero
    if x == 0 and y < 0: 
        #straight down
        launch_angle = numpy.pi/2
    elif x == 0 and y >= 0: 
        #straight up
        launch_angle = 3*numpy.pi/2
    else: 
        #from https://en.wikipedia.org/wiki/Projectile_motion#Angle_%CE%B8_required_to_hit_coordinate_(x,_y)
        #Launch angle = arctan(v^2 - (sqrt(v^4 - g(gx^2 + 2vy)) / gx)
        launch_angle = numpy.arctan((v**2 - (sqrt((v**4) - 
                                    gravity*(gravity*(x**2) + 2*(y*(v**2))))))
                                    / (gravity * x)).real

    #If we are shooting backwards, flip the angle (i.e. add half a rotation)
    if x > 0: launch_angle = launch_angle + numpy.pi

    #Create a unit vector that points in the direction of our angle
    heading_vector = [0, 0]
    heading_vector[0] = numpy.cos(launch_angle)
    heading_vector[1] = numpy.sin(launch_angle)

    #Create a vector with our initial velocity of the ball's trajectory
    veloc_vector = [0, 0]
    veloc_vector[0] = heading_vector[0] * launch_veloc
    veloc_vector[1] = heading_vector[1] * launch_veloc

    x_veloc = veloc_vector[0]
    y_veloc = veloc_vector[1]

    #create a list of tuples in the trajectory to draw it
    line_points = []

    cur_line_point = [0, 0]

    #t represents the time in flight for the ball 
    t = 0

    #while the line is on screen (with some room for overflow)...
    while(cur_line_point[0] < width + 200 and cur_line_point[0] > -200
          and cur_line_point[1] < height + 200):
        #Basic particle motion equations:
        #x(t) = (initial x velocity)(t) + (initial x position)
        #y(t) = (1/2)(gravity constant)(t^2) + (initial y velocity)(t) + (initial y position)
        cur_line_point[0] = x_veloc*t + ball_start_pos[0]
        cur_line_point[1] = (1/2)*gravity*(t**2) + y_veloc*t + ball_start_pos[1]
        #increment t by the time resolution
        t = t + time_resolution
        line_points.append(tuple(cur_line_point))
    
    screen.fill(background_color)
    pygame.draw.circle(screen, traj_color, ball_start_pos, 3)
    pygame.draw.lines(screen, traj_color, False, line_points, 1)
    pygame.display.flip()
