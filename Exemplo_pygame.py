# Imported modules
import pygame as pg
import math
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from colordict import ColorDict

# Inicializing imported color dictionary as variable, reversed color dict also
COLOR = ColorDict()
reverse_colors = {tuple(val): name for name, val in COLOR.items()}


# Program constants
# Related to screen size
SCREEN_HEIGHT = 900
SCREEN_LENGTH = 1600
HALF_HEIGHT = SCREEN_HEIGHT // 2
HALF_LENGTH = SCREEN_LENGTH // 2

# Related to text
FONT_SIZE = 26

# Related to the cartesian grid/plane
NUMBER_OF_X_GRID_LINES = 20
PIXEL_SCALE = (SCREEN_HEIGHT/NUMBER_OF_X_GRID_LINES + 1)
HALF_NUMBER_X_GRID_LINES = NUMBER_OF_X_GRID_LINES // 2
N_OF_SAMPLES = 100
GRAPH_EXTRA_PADDING = 50

# Related to the grid scale
MIN_SCALE = 0.3
MAX_SCALE = 15
SCALE_STEP = 0.05


# Pygame setup/inicialization
pg.init()
screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
pg.key.set_repeat(300, 50)
FONT = pg.font.SysFont("times new roman", FONT_SIZE)
#subtitles_img = pg.image.load("Legenda_calc_grafica.png").convert_alpha()
clock = pg.time.Clock()

'''
Writing info on screen
'''


def write_on_screen(string: str, position: tuple, color: tuple):
    """
    Writes a string on the screen.
    Parameters: string:str, position:tuple, color:tuple(rgb)
    Does not have a return value.
    """
    #font = pg.font.Font(None, FONT_SIZE)
    text = FONT.render(string, True, color)
    textpos = (position[0], position[1] - 10)
    screen.blit(text, textpos)
    #-(len(string) * FONT_SIZE/5)


def default_screen_info(tuple_info: tuple):
    """
    Parameters: tuple_info:tuple
    Receives all the dinamic parameters and inside of it also has default values, collects them to write on screen.
    Basically a more general way of showing info instead of doing each one individually.
    Does not have a return value.
    """

    write_on_screen("Press INSERT to Restart", (10, 45 + FONT_SIZE), COLOR["white"])
    write_on_screen("João Marcelo G.N.C.Pereira", (SCREEN_LENGTH - 308, SCREEN_HEIGHT - 20), COLOR["white"])
    write_on_screen("DRE: 126047924", (SCREEN_LENGTH - 190, SCREEN_HEIGHT - 20 - FONT_SIZE), COLOR["white"])
    for info in tuple_info:
        write_on_screen(info[0], info[1], info[2])


'''
Drawing the default empty cartesian plane
'''


def draw_empty_plane(scale: float) -> None:
    """
    Draws the empty cartesian plane grid.
    :param: plane_scale:
    :return: None
    """
    #Drawing the grid depending on the plane scale
    #For the x-axis
    number_of_x_lines = HALF_NUMBER_X_GRID_LINES / scale
    for i in range(1, math.floor(number_of_x_lines) + 1):
        #draws the upper part
        pg.draw.line(screen, COLOR["gray"], (0, HALF_HEIGHT - (HALF_HEIGHT/number_of_x_lines * i)),
                                            (SCREEN_LENGTH, HALF_HEIGHT - (HALF_HEIGHT/number_of_x_lines * i)))
        #draws the lower part
        pg.draw.line(screen, COLOR["gray"], (0, HALF_HEIGHT + (HALF_HEIGHT / number_of_x_lines * i)),
                                            (SCREEN_LENGTH, HALF_HEIGHT + (HALF_HEIGHT / number_of_x_lines * i)))

    #For the y-axis
    number_of_y_lines = SCREEN_LENGTH/SCREEN_HEIGHT * number_of_x_lines
    for j in range(1, math.floor(number_of_y_lines) + 1):
        #draws the left part
        pg.draw.line(screen, COLOR["gray"], (HALF_LENGTH - (HALF_LENGTH/number_of_y_lines * j), 0),
                                            (HALF_LENGTH - (HALF_LENGTH/number_of_y_lines * j), SCREEN_HEIGHT))
        #draws the right part
        pg.draw.line(screen, COLOR["gray"], (HALF_LENGTH + (HALF_LENGTH/number_of_y_lines * j), 0),
                                            (HALF_LENGTH + (HALF_LENGTH/number_of_y_lines * j), SCREEN_HEIGHT))

    #Drawing the x-axis and y-axis
    pg.draw.circle(screen, COLOR['white'], (HALF_LENGTH, HALF_HEIGHT), 4)
    pg.draw.line(screen, COLOR["white"], (HALF_LENGTH, 0), (HALF_LENGTH, SCREEN_HEIGHT), 3)
    pg.draw.line(screen, COLOR["white"], (0, HALF_HEIGHT), (SCREEN_LENGTH, HALF_HEIGHT), 3)


'''
Converting screen coords <-> cartesian plane coords
'''


def create_point(coord_x, coord_y, scale) -> tuple:
    """
    Given a point with coords x, y and a scale, returns the coords to print it in the screen.
    That's because pygames uses an inverted y-axis, but also because the coords depend on the current scale.
    :param coord_x:
    :param coord_y:
    :param scale:
    :return :tuple
    """
    coord_x = HALF_LENGTH + (coord_x * scale * PIXEL_SCALE)
    coord_y = (HALF_HEIGHT - (coord_y * scale * PIXEL_SCALE))
    return math.floor(coord_x), math.floor(coord_y)


def screen_to_cartesian_point(coord_x, coord_y, scale) -> tuple:
    """
    Given a point of the screen with coords x, y and a scale, returns the coords the point has on the cartesian grid/grid.
    That's because pygames uses an inverted y-axis, but also because the coords depend on the current scale.
    :param coord_x:
    :param coord_y:
    :param scale:
    :return :tuple
    """
    new_coord_x = (coord_x - HALF_LENGTH) / (scale * PIXEL_SCALE)
    new_coord_y = -(coord_y - HALF_HEIGHT) / (scale * PIXEL_SCALE)
    return new_coord_x, new_coord_y


'''
Parses the function str and gives a list of points that represent the (x,y) coords of the points in a function
'''


def calculate_function_points(function_expression: str, scale, x):
    """
    Parses the function str and gives a list of points that represent the (x,y) coords of the points in a function
    :param function_expression:
    :param scale:
    :param x:
    :return:
    """
    func = parse_expr(function_expression, {"x": x})

    list_points = []
    list_lines = []
    delta_x = 0.2
    samples = SCREEN_LENGTH // (10 * delta_x)
    for i in range(0, math.ceil(2*samples) + 1):
        x_value = (i - samples) * delta_x
        if -HALF_LENGTH - GRAPH_EXTRA_PADDING <= x_value * PIXEL_SCALE * scale <= HALF_LENGTH + GRAPH_EXTRA_PADDING:
            try:
                result = func.subs({x: x_value})
                if -HALF_HEIGHT - GRAPH_EXTRA_PADDING <= result * PIXEL_SCALE * scale <= HALF_HEIGHT + GRAPH_EXTRA_PADDING:
                    list_points.append(create_point(x_value, result, plane_scale))
            except:
                list_lines.append(x_value)

    return list_points, list_lines


'''
If the scale is changed or the screen initialized, calculates/updates all of the points of all functions, using
calculate_function_points() for each function
'''


def update_function_points(functions, scale):
    """
    If the scale is changed or the screen initialized, calculates/updates all of the points of all functions, using
    calculate_function_points() for each function
    :param functions:
    :param scale:
    :return:
    """
    graphs = []
    for func in functions:
        list_points, list_lines = calculate_function_points(func[0], scale, x)
        graphs.append((list_points, list_lines, func[1]))
    return graphs


'''
Draws the functions, lines and points into the screen/cartesian plane
'''


def draw_graphs(functions_graphs: tuple, mouse=(0, 0), inverted=False):
    """
    Receives a tuple, where each element
    is another tuple, with (all graph points, all graph lines, color)
    :param functions_graphs:
    :param inverted:bool
    :param mouse:tuple
    :return:
    """
    #if inverted:
    #    for func in functions_graphs:
    #        for point in range(0, len(func[0]) - 1):
    #            derivative_color = list(COLOR[func[2]])
    #            derivative_color[0] = 255 - derivative_color[0]
    #            derivative_color[1] = 255 - derivative_color[1]
    #            derivative_color[2] = 255 - derivative_color[2]
    #            pg.draw.line(screen, derivative_color, func[0][point], func[0][point + 1], 2)
    #else:
    for func in functions_graphs:
        for point in range(0, len(func[0]) - 1):
            try:
                pg.draw.line(screen, COLOR[func[2]], func[0][point], func[0][point + 1], 2)
            except TypeError:
                pg.draw.line(screen, COLOR[func[2]], (mouse[0], 0), (mouse[0], SCREEN_HEIGHT), 2)

def draw_points(list_points, scale):
    """
    Each element consists of ("point", "x1", "y1", "color", "size")
    :param: list_points, scale:
    :return:
    """
    for point in list_points:
        point_coord = create_point(float(point[1]), float(point[2]), scale)
        pg.draw.circle(screen, COLOR[point[3]], point_coord, float(point[4]) * scale)


def draw_lines(list_lines, scale):
    """
    Each element consists of ("point", "x1", "y1", "x2", "y2", "color")
    :param: list_lines, scale:
    :return:
    """
    for line in list_lines:
        point_1_coord = create_point(float(line[1]), float(line[2]), scale)
        point_2_coord = create_point(float(line[3]), float(line[4]), scale)
        pg.draw.line(screen, COLOR[line[5]], point_1_coord, point_2_coord, 1)


'''
Draws the description of the functions, lines and points that are on screen
'''


def draw_functions_info(list_expressions):
    for i, info in enumerate(list_expressions):
        pg.draw.rect(screen, COLOR["darkgray"], pg.Rect(20, SCREEN_HEIGHT - ((i + 2) * FONT_SIZE) - 10, FONT_SIZE * len(info[0]) * 0.7, FONT_SIZE))
        pg.draw.rect(screen, COLOR["white"],
                     pg.Rect(20, SCREEN_HEIGHT - ((i + 2) * FONT_SIZE) - 10, FONT_SIZE * len(info[0]) * 0.7, FONT_SIZE), 1)
        write_on_screen(info[0], (30, SCREEN_HEIGHT - ((i + 2) * FONT_SIZE)), info[1])

        if i == len(list_expressions) - 1:
            write_on_screen("Functions:", (20, SCREEN_HEIGHT - ((i + 3) * FONT_SIZE)), COLOR["lightgray"])


def draw_lines_info(list_lines, n_lines):
    for i, info in enumerate(list_lines):
        text = f"({info[1]},{info[2]}) -> ({info[3]},{info[4]})"
        pg.draw.rect(screen, COLOR["darkgray"],
                     pg.Rect(SCREEN_LENGTH - FONT_SIZE * 8, ((i + 2) * FONT_SIZE) - 10, FONT_SIZE * len(text) * 0.5,
                             FONT_SIZE))
        pg.draw.rect(screen, COLOR["white"],
                     pg.Rect(SCREEN_LENGTH - FONT_SIZE * 8, ((i + 2) * FONT_SIZE) - 10, FONT_SIZE * len(text) * 0.5,
                             FONT_SIZE), 1)
        write_on_screen(text, (SCREEN_LENGTH - FONT_SIZE * 8, ((i + 2) * FONT_SIZE)), info[5])
        n_lines += 1
        if i == len(list_lines) - 1:
            write_on_screen("Lines:", (SCREEN_LENGTH - FONT_SIZE * 8, ((i + 1) * FONT_SIZE)), COLOR["lightgray"])
            n_lines += 1
    return n_lines


def draw_points_info(list_points, n_lines):
    for j, info in enumerate(list_points):
        if j == 0:
            write_on_screen("Points:", (SCREEN_LENGTH - FONT_SIZE * 8, ((n_lines + j + 1) * FONT_SIZE)), COLOR["lightgray"])
            n_lines += 1
        text = f"({info[1]},{info[2]}), Size: {info[4]}"
        pg.draw.rect(screen, COLOR["darkgray"],
                     pg.Rect(SCREEN_LENGTH - FONT_SIZE * 8, ((n_lines + j + 1) * FONT_SIZE) - 10,
                     FONT_SIZE * len(text) * 0.5, FONT_SIZE))
        pg.draw.rect(screen, COLOR["white"],
                     pg.Rect(SCREEN_LENGTH - FONT_SIZE * 8, ((n_lines + j + 1) * FONT_SIZE) - 10,
                             FONT_SIZE * len(text) * 0.5, FONT_SIZE), 1)
        write_on_screen(text, (SCREEN_LENGTH - FONT_SIZE * 8, ((n_lines + j + 1) * FONT_SIZE)), info[3])
    return n_lines


def write_expressions_on_screen(list_expressions: list, list_points, list_lines):
    #It is written the only one on the bottom left of the screen, doesnt need to account for other info
    draw_functions_info(list_expressions)

    #both lines and points are written in the top right corner, the n_lines takes into consideration where the last str was written on the screen
    n_lines = 0
    n_lines = draw_lines_info(list_lines, n_lines)
    n_lines = draw_points_info(list_points, n_lines)


'''
Calculates the derivative of all the functions active, given the list of functions, scale and variable x,tracks mouse position
'''


def calculate_derivative(list_expressions: list, scale, x):
    mouse_coord_x, mouse_coord_y = pg.mouse.get_pos()
    mouse_value_in_cartesian_plane = screen_to_cartesian_point(mouse_coord_x, mouse_coord_y, scale)
    pg.draw.circle(screen, COLOR["blue"], mouse_value_in_cartesian_plane, 2)

    list_derivatives = []
    list_points = []
    for i in list_expressions:
        func_original = parse_expr(i[0], {"x": x})
        y_original = func_original.subs({x: mouse_value_in_cartesian_plane[0]})

        new_expression = f"diff({i[0]})"
        func = parse_expr(new_expression, {"x": x})
        result = func.subs({x: mouse_value_in_cartesian_plane[0]})
        derivative_expression = f"{result}*(x - {mouse_value_in_cartesian_plane[0]}) + {y_original}"

        derivative_function = parse_expr(derivative_expression, {"x": x})
        # On the left part of the screen
        x1 = (0 - HALF_LENGTH) / (scale * PIXEL_SCALE)
        y1 = derivative_function.subs({x: x1})

        # On the right part of the screen
        x2 = (SCREEN_LENGTH - HALF_LENGTH) / (scale * PIXEL_SCALE)
        y2 = derivative_function.subs({x: x2})

        # IMPORTANTE:
        #list_derivatives.append((derivative_expression, i[1]))

        list_points.append([(create_point(x1, y1, scale), create_point(x2, y2, scale)), [], i[1]])
        #list_points.append(create_point(x_value, result, plane_scale))
    return list_points


# Creating dynamic variables
show_subtitles = False
running = True
dt = 0
sum_dt = 0
plane_scale = 2
delta_scale = 0
first_time = 1
graphs = tuple()
expressions = []
example_expressions = [("exp(x)", "blue"), ("sin(x)", "red"), ("diff(x**2, x)", "purple"), ("abs(x**2 - 10)", "green")]
example_expressions_2 = [('log(abs(x))', 'yellow'), ('atan(x)', 'orange')]
input_text = ""
new_expression = tuple()
added_expression = 0
list_lines = []
list_points = []
list_derivatives = []
graphs_derivatives = tuple
list_points_derivatives = []

while running:
    last_delta_scale = delta_scale
    delta_scale = 0
    # poll for events
    # pg.QUIT event means the user clicked X to close the window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEWHEEL:
            # The bigger the scale, the bigger the pixel. scaled_pixel = pixel_size * plane_scale
            plane_scale += event.y * SCALE_STEP
            if plane_scale < MIN_SCALE:
                plane_scale = MIN_SCALE
            elif plane_scale > MAX_SCALE:
                plane_scale = MAX_SCALE
            delta_scale = plane_scale - last_delta_scale

        elif event.type == pg.KEYDOWN:
            # Restarts program without having to exit
            if event.key == pg.K_INSERT:
                expressions = []
                list_lines = []
                list_points = []
                first_time = 1

            # removes last char written
            if event.key == pg.K_BACKSPACE:
                input_text = input_text[:-1]

            # Adds new expression if its correct and on its type
            elif event.key == pg.K_RETURN:
                new_expression: tuple = tuple(input_text.replace(" ", "").split(","))
                len_expression = len(new_expression)

                # If has 2 arguments, new expression is a function
                if len_expression == 2:
                    print("Adding expression:", new_expression)  # aqui você processa
                    expressions.append(new_expression)
                    added_expression = 1

                # If has 5 arguments and has the keyword point, add it to the points list
                elif len_expression == 5 and new_expression[0] == 'point':
                    """
                    (mode=point, x1, x2, color, size)
                    """
                    print("Adding point:", new_expression)
                    list_points.append(new_expression)
                    added_expression = 1

                # If has 6 arguments and has the keyword line, add it to the li list
                elif len_expression == 6 and new_expression[0] == 'line':
                    """
                    (mode=line, x1, y1, x2, y2, color)
                    """
                    print("Adding Line:", new_expression)
                    list_lines.append(new_expression)
                    added_expression = 1

                input_text = ""

            # If user presses tab key shwos subtitles
            elif event.key == pg.K_TAB:
                show_subtitles = not show_subtitles

            elif event.key == pg.K_PERIOD:
                expressions = example_expressions
            elif event.key == pg.K_SEMICOLON:
                expressions = example_expressions_2
            # any other char, continues input text
            elif event.unicode:
                input_text += event.unicode



    # fill the screen with a color to wipe away anything from last frame
    screen.fill(COLOR["black"])


    scale_info = (f"Scale: {plane_scale:.2f}", (10, 10), COLOR["white"])
    draw_empty_plane(plane_scale)

    # Define symbolic variables
    x, y = sp.symbols('x y', real=True)

    if delta_scale != 0 or first_time or added_expression:
        graphs = update_function_points(expressions, plane_scale)
        first_time = 0
        added_expression = 0
        list_points_derivatives = calculate_derivative(expressions, plane_scale, x)
        #graphs_derivatives = update_function_points(list_derivatives, plane_scale)
        draw_graphs(list_points_derivatives)
    #elif sum_dt % 3 == 0:
    list_points_derivatives = calculate_derivative(expressions, plane_scale, x)
    #graphs_derivatives = update_function_points(list_derivatives, plane_scale)
    mouse_coord_x, mouse_coord_y = pg.mouse.get_pos()
    mouse_x, mouse_y = screen_to_cartesian_point(mouse_coord_x, mouse_coord_y, plane_scale)
    m_x, m_y = create_point(mouse_x, mouse_y, plane_scale)
    draw_graphs(list_points_derivatives, (m_x, m_y))

    #draw_graphs(list_points_derivatives)

    draw_graphs(graphs)
    draw_points(list_points, plane_scale)
    draw_lines(list_lines, plane_scale)
    incomplete_input = input_text
    write_on_screen(f"INPUT: {incomplete_input}", (10, 40), COLOR["white"])

    write_expressions_on_screen(expressions, list_points, list_lines)
    tuple_info = (scale_info, )
    default_screen_info(tuple_info)

    if show_subtitles:
        # tela.blit(imagem, (posicao_X, posicao_Y))
        # Exemplo: colocando no canto superior direito
        screen.blit(subtitles_img, (SCREEN_LENGTH - 685, SCREEN_HEIGHT * 0.6))

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(45) / 1000
    sum_dt += dt * 1000
pg.quit()
