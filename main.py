
"""
This code defines several functions for transforming and drawing polygons using Turtle graphics. The functions include translation, rotation, scaling, reflection, and shearing. The code also includes a function for drawing Bezier curves and a function for drawing a pattern by repeatedly calling the draw_polygon function and applying a transformation to the vertices based on user input. Additionally, the code includes a function for saving the polygon data to a file. 
"""

import turtle
import math

def apply_matrix(matrix, vertices):
  """
  Applies a transformation matrix to a list of vertices.

  Args:
  - matrix (list of lists): The transformation matrix to apply.
  - vertices (list of tuples): The vertices to transform.

  Returns:
  - list of tuples: The transformed vertices.
  """
  vertices = [(x, y, 1) for x, y in vertices]

  matrix_t = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

  result = []
  for vertex in vertices:
    x = sum([a * b for a, b in zip(matrix_t[0], vertex)])
    y = sum([a * b for a, b in zip(matrix_t[1], vertex)])
    w = sum([a * b for a, b in zip(matrix_t[2], vertex)])
    result.append((x/w, y/w))

  return result

def translate(vertices, dx, dy):
  """
  Translates a set of vertices by a given amount in the x and y directions.

  Args:
  vertices (list): A list of tuples representing the vertices to be translated.
  dx (float): The amount to translate each vertex in the x direction.
  dy (float): The amount to translate each vertex in the y direction.

  Returns:
  list: A list of tuples representing the translated vertices.
  """
  result = []
  for vertex in vertices:
    result.append((vertex[0] + dx, vertex[1] + dy))
    
  return result

import math

def rotate(vertices, angle):
  """
  Rotate a set of vertices by a given angle (in degrees) around the origin (0, 0).

  Args:
  - vertices: a list of tuples representing the vertices to be rotated
  - angle: the angle (in degrees) by which to rotate the vertices

  Returns:
  - a new list of tuples representing the rotated vertices
  """
  radians = math.radians(angle)
  matrix = [
    [math.cos(radians), -math.sin(radians), 0],
    [math.sin(radians), math.cos(radians), 0],
    [0, 0, 1]
  ]

  return apply_matrix(matrix, vertices)

def reflect_x(vertices):
  """
  Reflects the given vertices about the x-axis.

  Args:
  vertices (list): A list of vertices, where each vertex is a tuple of x and y coordinates.

  Returns:
  list: A list of vertices, where each vertex is a tuple of x and y coordinates, after being reflected about the x-axis.
  """

  matrix = [
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
  ]

  return apply_matrix(matrix, vertices)

def reflect_y(vertices):
  """
  Reflects the given vertices about the y-axis.

  Args:
  vertices (list): A list of vertices in the form [(x1, y1), (x2, y2), ...]

  Returns:
  list: A list of vertices in the form [(x1', y1'), (x2', y2'), ...] where each vertex is reflected about the y-axis.
  """

  matrix = [
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
  ]

  return apply_matrix(matrix, vertices)

def shear_x(vertices, k):
  """
  Applies a shear transformation along the x-axis to the given vertices.

  Args:
  - vertices: A list of tuples representing the vertices of a polygon.
  - k: The shear factor.

  Returns:
  A list of tuples representing the transformed vertices.
  """

  matrix = [
    [1, k, 0], 
    [0, 1, 0],
    [0, 0, 1]
  ]

  return apply_matrix(matrix, vertices)

def shear_y(vertices, k):
  """
  Applies a shear transformation along the y-axis to the given vertices.

  Args:
  vertices (list): A list of vertices to apply the transformation to.
  k (float): The shear factor.

  Returns:
  list: The transformed vertices.
  """

  matrix = [
    [1, 0, 0],
    [k, 1, 0],
    [0, 0, 1]
  ]

  return apply_matrix(matrix, vertices)

def scale(vertices, sx, sy):
  """
  Scales the given vertices by the given factors in the x and y directions.

  Args:
  - vertices: a list of tuples representing the vertices to be scaled
  - sx: a float representing the scaling factor in the x direction
  - sy: a float representing the scaling factor in the y direction

  Returns:
  - a list of tuples representing the scaled vertices
  """

  matrix = [
    [sx, 0, 0],
    [0, sy, 0], 
    [0, 0, 1]
  ]

  return apply_matrix(matrix, vertices)


def draw_edge(P0, P1, is_curved, color, control_points=None):
  #global fill
  """
  Draws an edge between two points using turtle graphics.

  Args:
  - P0 (tuple): The starting point of the edge.
  - P1 (tuple): The ending point of the edge.
  - is_curved (bool): A flag indicating whether the edge should be curved or straight.
  - color (str): The color of the edge.
  - control_points (list of tuples, optional): A list of two tuples representing the control points for the Bezier curve. Only used if is_curved is True.

  Returns:
  - None
  """
  if is_curved:
    if control_points:
      P2x= float(control_points[0][0])
      P2y = float(control_points[0][1])
      P3x = float(control_points[1][0])
      P3y = float(control_points[1][1])
    else:
      P2x, P2y, P3x, P3y = 0, 0, 0, 0

    draw_bezier_curve(P0[0], P0[1], P3x,  P3y , P2x, P2y, P1[0], P1[1], color)

  else:
    # if fill:
    #   turtle.fillcolor("green")
    #   turtle.begin_fill()

    turtle.penup()
    turtle.goto(P0)
    turtle.pendown()
    turtle.color(color)
    turtle.goto(P1)
    
    # if fill:
    #   turtle.end_fill()

import turtle

def draw_bezier_curve(P0x, P0y, P1x, P1y, P2x, P2y, P3x, P3y, color):
  # global fill
  """
  Draws a Bezier curve using the given control points and color.

  Args:
  P0x (float): x-coordinate of the first control point
  P0y (float): y-coordinate of the first control point
  P1x (float): x-coordinate of the second control point
  P1y (float): y-coordinate of the second control point
  P2x (float): x-coordinate of the third control point
  P2y (float): y-coordinate of the third control point
  P3x (float): x-coordinate of the fourth control point
  P3y (float): y-coordinate of the fourth control point
  color (str): color of the curve to be drawn

  Returns:
  None
  """
  # if fill:
  #   turtle.fillcolor("green")
  #   turtle.begin_fill()
  turtle.penup()
  turtle.goto((P0x, P0y))
  turtle.pendown()
  turtle.color(color)
  # if fill:
  #   turtle.end_fill()
  
  for t in range(0, 101, 5):
    t /= 100
    x = (1 - t) ** 3 * P0x + 3 * t * (1 - t) ** 2 * P1x + 3 * t**2 * (1 - t) * P2x + t**3 * P3x
    y = (1 - t) ** 3 * P0y + 3 * t * (1 - t) ** 2 * P1y + 3 * t**2 * (1 - t) * P2y + t**3 * P3y
    turtle.goto((x, y))
  
  turtle.goto((P3x, P3y))

def draw_polygon(vertices, edges, colors, control_points):
  # global fill
  """
  Draws a polygon using Turtle graphics and returns a list of dictionaries containing information about each edge.

  Args:
  - vertices (list of tuples): The vertices of the polygon in clockwise order.
  - edges (list of bool): A list of booleans indicating whether each edge is curved or not.
  - colors (list of str): A list of colors for each edge.
  - control_points (list of tuples): A list of control points for each curved edge. If an edge is not curved, the corresponding value should be None.

  Returns:
  - polygon_data (list of dict): A list of dictionaries containing information about each edge. Each dictionary has the following keys:
    - 'Curved' (bool): Whether the edge is curved or not.
    - 'Coordinates' (tuple): The coordinates of the starting vertex of the edge.
    - 'Color' (str): The color of the edge.
    - 'ControlPoints' (tuple or None): The control points of the edge. If the edge is not curved, the value is None.
  """
  polygon_data = []

  for i in range(len(vertices)):
    P0 = vertices[i] 
    P1 = vertices[(i + 1) % len(vertices)]

    is_curved = edges[i]
    color = colors[i]
    control = control_points if is_curved else None
    draw_edge(P0, P1, is_curved, color, control)

    polygon_data.append({
      'Curved': is_curved,
      'Coordinates': P0,
      'Color': color,
      'ControlPoints': control
    })
  
  turtle.penup()  # Lift the pen to avoid drawing connecting lines between polygons

  return polygon_data


def draw_pattern(vertices, edges, colors, control_points, num_patterns):
    """
    Draws a pattern by repeatedly calling the draw_polygon function and applying a transformation to the vertices based on user input.

    Args:
    vertices (list): A list of vertices that define the polygon to be drawn.
    edges (list): A list of edges that connect the vertices.
    colors (list): A list of colors to fill the polygon with.
    control_points (list): A list of control points to adjust the shape of the polygon.
    num_patterns (int): The number of patterns to draw.

    Returns:
    None
    """
    print("Choose a transformation:")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    transform_choice = int(turtle.numinput("Transformation choice", "Enter your choice:"))

    if transform_choice == 1:
          trans_choice = int(turtle.numinput("Vertical or Horizontal", "Enter your choice (Vertical/Horizontal)(1/0):"))
   
    for i in range(num_patterns):
        polygon_data = draw_polygon(vertices, edges, colors, control_points)
        if transform_choice == 1:
          dist = int(turtle.numinput("Enter translation distance", "Enter translation distance:"))
          if trans_choice == 1:
              vertices = translate(vertices, 0, dist)
          else:
              vertices = translate(vertices, dist, 0)
        elif transform_choice == 2:
          vertices = rotate(vertices, 360/num_patterns)
        elif transform_choice == 3:
          sc = int(turtle.numinput("Enter scaling factor", "Enter scaling factor:"))
          vertices = scale(vertices, sc,sc)
   
def save_polygon_data(file, polygon_data):
  """
  Save the polygon data to a file.

  Args:
  - file: A file object to write the polygon data to.
  - polygon_data: A list of dictionaries containing the polygon data.

  Returns:
  - None
  """

  for data in polygon_data:
    if data['Curved']:
      file.write(f"{data['Curved']} {data['Coordinates'][0]} {data['Coordinates'][1]} {data['ControlPoints'][0][0]} {data['ControlPoints'][0][1]} {data['ControlPoints'][1][0]}  {data['ControlPoints'][1][1]} {data['Color']}\n")
    else:
      file.write(f"{data['Curved']} {data['Coordinates'][0]} {data['Coordinates'][1]} {data['Color']}\n")


import turtle

def main():
  """
  This function is the main entry point of the program. It prompts the user to input a polygon either from a file or manually, applies a transformation if requested, and then draws the polygon. It also gives the option to draw a pattern and save the polygon data to a file.
  """
  turtle.speed(0)
  turtle.hideturtle()
  
  input_option = turtle.textinput("File input", "Do you want to input from a file? (y/n)")

  if input_option.lower() == 'y':
    file_name = turtle.textinput("File name", "Enter the file name:")
    opened = True
    try:
      with open(file_name, 'r') as file:
        vertices = []
        edges = []
        colors = []
        control_points = []

      
        for line in file:
          if line.strip() == '' and len(vertices) > 0:
              # Draw the current polygon and reset data for the new polygon
              
              draw_polygon(vertices, edges, colors, control_points)
              continue
          elif line.strip() == '':
              vertices = []
              edges = []
              colors = []
              control_points = []
      
              continue

          data = line.split()
          if data[0] == 'True':
              vertices.append((float(data[1]), float(data[2])))
              edges.append(True)
              colors.append(data[-1])
              control_points.append((float(data[3]), float(data[4])))
              control_points.append((float(data[5]), float(data[6])))
          else:
              vertices.append((float(data[1]), float(data[2])))
              edges.append(False)
              colors.append(data[3])
              control_points.append(None)

  # Draw the last polygon in the file

        try:
          polygon_data = draw_polygon(vertices, edges, colors, control_points)
        except:
          print("Invalid Input")
    except:
      print("File not found")
      main()


  else:
    opened = False

    num_sides = int(turtle.numinput("Number of sides", "Enter number of sides of polygon:"))
    vertices = []
    for i in range(num_sides):
      x = turtle.numinput(f"Vertex {i+1} x", f"Enter x coordinate of vertex {i+1}:")
      y = turtle.numinput(f"Vertex {i+1} y", f"Enter y coordinate of vertex {i+1}:")
      vertices.append((x, y))

    edges = []
    colors = []
    control_points = []
    for i in range(len(vertices)):
      is_curved = turtle.textinput(f"Edge {i} curved?", f"Is edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]} curved? (y/n)").lower() == 'y'
      color = turtle.textinput(f"Edge {i} color", f"Enter the color for the edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]}: ")
      edges.append(is_curved)
      colors.append(color)

      if is_curved:
        x = turtle.numinput(f"Edge {i} control point P2x", f"Enter x coordinate of control point for edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]}: ")
        y = turtle.numinput(f"Edge {i} control point P2y", f"Enter y coordinate of control point for edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]}: ")
        control_points.append((x, y))
        x = turtle.numinput(f"Edge {i} control point P3x", f"Enter x coordinate of control point for edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]}: ")
        y = turtle.numinput(f"Edge {i} control point P3y", f"Enter y coordinate of control point for edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]}: ")
        control_points.append((x, y))
      else:
        control_points.append(None)

  choice = turtle.textinput("Transformation", "Do you want to apply a transformation? (y/n)")
  if choice.lower() == 'y':
    print("Choose a transformation:")
    print("1. Translation")
    print("2. Rotation")
    print("3. Reflection about x-axis")
    print("4. Reflection about y-axis")
    print("5. Shearing along x-axis")
    print("6. Shearing along y-axis")
    print("7. Scaling")
    transform_choice = int(turtle.numinput("Transformation choice", "Enter your choice:"))
    if transform_choice == 1:
      dx = float(turtle.numinput("X translation", "Enter x translation:"))
      dy = float(turtle.numinput("Y translation", "Enter y translation:"))
      vertices = translate(vertices, dx, dy)
    elif transform_choice == 2:
      angle = float(turtle.numinput("Rotation angle", "Enter rotation angle:"))
      vertices = rotate(vertices, angle)
    elif transform_choice == 3:
      vertices = reflect_x(vertices)
    elif transform_choice == 4:
      vertices = reflect_y(vertices)
    elif transform_choice == 5:
      k = float(turtle.numinput("Shearing factor", "Enter shearing factor:"))
      vertices = shear_x(vertices, k)
    elif transform_choice == 6:
      k = float(turtle.numinput("Shearing factor", "Enter shearing factor:"))
      vertices = shear_y(vertices, k)  
    elif transform_choice == 7:
      sx = float(turtle.numinput("X scaling factor", "Enter x scaling factor:"))
      sy = float(turtle.numinput("Y scaling factor", "Enter y scaling factor:"))
      vertices = scale(vertices, sx, sy)
  pattern = turtle.textinput('Pattern',"Do you want to draw a pattern: (y/n)")
  if pattern.lower() == 'y':
    num_patterns = int(turtle.numinput("Number of patterns", "Enter the number of patterns:"))
    draw_pattern(vertices, edges, colors, control_points, num_patterns)
  try:
    polygon_data = draw_polygon(vertices, edges, colors, control_points)
  except:
    print("Invalid input")

  if not opened:
    with open("output_file.txt", 'a') as output_file:
      output_file.write("\n")
      try:
        save_polygon_data(output_file, polygon_data)
      except:
        pass

  choice = turtle.textinput("Draw another", "Do you want to draw another polygon? (y/n)")
  if choice.lower() == 'y':
    main()
  else:
    turtle.bye()

main()