
import math
import turtle


# Define a function to create an edge between two points
def edge_maker(P0, P1, is_straight, color, curve_points=None):
  
  # If the edge is curved
  if is_straight == False:
    if curve_points:
      # Get the control points for the Bezier curve
      P2x= float(curve_points[0][0])
      P2y = float(curve_points[0][1])
      P3x = float(curve_points[1][0])
      P3y = float(curve_points[1][1])
    else:
      # Set default control points to (0, 0)
      P2x, P2y, P3x, P3y = 0, 0, 0, 0

    # Draw a Bezier curve using the control points and color
    curve_maker(P0[0], P0[1], P3x,  P3y , P2x, P2y, P1[0], P1[1], color)

  # If the edge is straight
  else:
    turtle.penup()
    turtle.goto(P0)
    turtle.pendown()
    turtle.color(color)
    turtle.goto(P1)
    

# Define a function to draw a curve using Bezier curve algorithm
def curve_maker(P0x, P0y, P1x, P1y, P2x, P2y, P3x, P3y, color):
  turtle.penup()
  turtle.goto((P0x, P0y))
  turtle.pendown()
  turtle.color(color)
  
  # Iterate over t values from 0 to 1 with a step of 0.05
  for t in range(0, 101, 5):
    t /= 100
    # Calculate x and y coordinates using the Bezier curve formula
    x = (1 - t) ** 3 * P0x + 3 * t * (1 - t) ** 2 * P1x + 3 * t**2 * (1 - t) * P2x + t**3 * P3x
    y = (1 - t) ** 3 * P0y + 3 * t * (1 - t) ** 2 * P1y + 3 * t**2 * (1 - t) * P2y + t**3 * P3y
    turtle.goto((x, y))
  
  turtle.goto((P3x, P3y))

# Define a function to draw a polygon using the given vertices, edges, colors, and curve points
def polygon_maker(vertices, edges, colors, curve_points):
  polygon_data = []

  # Iterate over each vertex and its corresponding edge and color
  for i in range(len(vertices)):
    P0 = vertices[i] 
    P1 = vertices[(i + 1) % len(vertices)]

    is_straight = not edges[i]
    color = colors[i]
    control = curve_points if not is_straight else None
    edge_maker(P0, P1, is_straight, color, control)

    # Append the polygon data to the list
    polygon_data.append({
      'Curved': not is_straight,
      'Coordinates': P0,
      'Color': color,
      'ControlPoints': control
    })
  
  turtle.penup()  

  return polygon_data

# Define a function to create patterns by transforming the given polygon
import turtle

# Define a function to create patterns by transforming the given polygon
def pattern_maker(vertices, edges, colors, curve_points, num_patterns):
    # Ask the user for transformation choice
    transform_choice = int(turtle.numinput("POLYGON MAKER", "Choice:\n 1. Translation\n2. Rotation\n3. Scaling"))

    if transform_choice == 1:
        trans_choice = turtle.textinput("POLYGON MAKER", "Enter your choice (Vertical/Horizontal)(y/n):")

    def apply_transformation(vertices, transform_choice):
        if transform_choice == 1:
            dist = int(turtle.numinput("POLYGON MAKER", "Translation distance:"))
            if trans_choice == 'y':
                vertices = translate(vertices, 0, dist)
            else:
                vertices = translate(vertices, dist, 0)
        elif transform_choice == 2:
            vertices = rotate(vertices, 360/num_patterns)
        elif transform_choice == 3:
            sc = int(turtle.numinput("POLYGON MAKER", "Scaling factor:"))
            vertices = transform_size(vertices, sc, sc)
        return vertices

    for i in range(num_patterns):
        polygon_data = polygon_maker(vertices, edges, colors, curve_points)
        vertices = apply_transformation(vertices, transform_choice)

# Define a function to save the polygon data to a file
def file_maker(file, polygon_data):
  for data in polygon_data:
    if data['Curved']:
      file.write(f"{data['Curved']} {data['Coordinates'][0]} {data['Coordinates'][1]} {data['ControlPoints'][0][0]} {data['ControlPoints'][0][1]} {data['ControlPoints'][1][0]}  {data['ControlPoints'][1][1]} {data['Color']}\n")
    else:
      file.write(f"{data['Curved']} {data['Coordinates'][0]} {data['Coordinates'][1]} {data['Color']}\n")

# Define a function to perform generic matrix multiplication
def generic_mat(m,v):
  v = [(x, y, 1) for x, y in v]

  transpose = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

  result = []
  for vertex in v:
    l = sum([a * b for a, b in zip(transpose[0], vertex)])
    m = sum([a * b for a, b in zip(transpose[1], vertex)])
    n = sum([a * b for a, b in zip(transpose[2], vertex)])
    result.append((l/n, m/n))

  return result

# Define a function to translate the vertices by the given distances
def translate(vertices, x_trans, y_trans):
  result = []
  # Perform translation for each vertex
  # END: be15d9bcejpp
  for vertex in vertices:
    result.append((vertex[0] + x_trans, vertex[1] + y_trans))
    
  return result

# Define a function to rotate the given vector by the specified angle
def rotate(v, angle):
  radians = math.radians(angle)
  return generic_mat([
    [math.cos(radians), -math.sin(radians), 0],
    [math.sin(radians), math.cos(radians), 0],
    [0, 0, 1]
  ], v)


# Define a function to reflect the given vector across the x-axis or y-axis
def reflect(v, x):
  return generic_mat([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
  ], v) if not x else generic_mat([
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
  ], v)


# Define a function to shear the given vector by the specified factor along the x-axis or y-axis
def shear(v, k, x):
  return generic_mat([
    [1, 0, 0],
    [k, 1, 0],
    [0, 0, 1]
  ], v) if not x else generic_mat([
    [1, 0, 0],
    [0, 1, 0],
    [0, k, 1]
  ], v)


# Define a function to transform the size of the given vector by scaling along the x-axis and y-axis
def transform_size(v, x_scale, y_scale):
  return generic_mat([
    [x_scale, 0, 0],
    [0, y_scale, 0],
    [0, 0, 1]
  ], v)
# Define the main function
def main():
  
  # Set up the turtle
  turtle.speed(0)
  turtle.hideturtle()
  
  # Ask the user for input option
  input_option = turtle.textinput("POLYGON MAKER", "File Input? (y/n)")

  # If the user chooses file input
  if input_option.lower() == 'y':
    # Ask for the file name
    file_name = turtle.textinput("POLYGON MAKER", "Enter the file name along with .txt extension:")
    opened = True
    try:
      # Open the file
      with open(file_name, 'r') as file:
        vertices = []
        edges = []
        colors = []
        curve_points = []

        # Read each line in the file
        for line in file:
          # If the line is empty and there are vertices, create a polygon
          if line.strip() == '' and len(vertices) > 0:
            polygon_maker(vertices, edges, colors, curve_points)
            continue
          # If the line is empty, reset the lists
          elif line.strip() == '':
            vertices = []
            edges = []
            colors = []
            curve_points = []
            continue

          # Split the line into data
          data = line.split()
          # If the edge is curved
          if data[0] == 'True':
            vertices.append((float(data[1]), float(data[2])))
            edges.append(True)
            colors.append(data[-1])
            curve_points.append((float(data[3]), float(data[4])))
            curve_points.append((float(data[5]), float(data[6])))
          # If the edge is straight
          else:
            vertices.append((float(data[1]), float(data[2])))
            edges.append(False)
            colors.append(data[3])
            curve_points.append(None)

        try:
          # Create the polygon using the data
          polygon_data = polygon_maker(vertices, edges, colors, curve_points)
        except:
          print("Please enter valid input!")
    except:
      print("File may be corrupted or does not exist!")
      main()

  # If the user chooses manual input
  else:
    opened = False

    # Ask for the number of sides of the polygon
    num_sides = int(turtle.numinput("POLYGON MAKER", "Sides of polygon? (INTEGER > 0):"))
    vertices = []
    # Ask for the coordinates of each vertex
    for i in range(num_sides):
      x = turtle.numinput(f"x {i+1}", f"Enter x  {i+1} coordinate:")
      y = turtle.numinput(f"y {i+1} ", f"Enter y {i+1} coordinate :")
      vertices.append((x, y))

    edges = []
    colors = []
    curve_points = []
    # Ask for the color and curvature of each edge
    for i in range(len(vertices)):
      color = turtle.textinput(f"POLYGON MAKER", f"Enter the color for the edge {vertices[i]} to {vertices[(i + 1) % len(vertices)]}: ")
      is_straight = not turtle.textinput(f"POLYGON MAKER", f"{vertices[i]} to {vertices[(i + 1) % len(vertices)]} curved? (y/n)").lower() == 'y'
      edges.append(not is_straight)
      colors.append(color)

      if not is_straight:
        x = turtle.numinput(f"POLYGON MAKER", f"Enter x control point for [{vertices[i]}, {vertices[(i + 1) % len(vertices)]}]: ")
        y = turtle.numinput(f"POLYGON MAKER", f"Enter y control point for [{vertices[i]}, {vertices[(i + 1) % len(vertices)]}]: ")
        curve_points.append((x, y))
        x = turtle.numinput(f"POLYGON MAKER", f"Enter x control point for [{vertices[i]} to {vertices[(i + 1) % len(vertices)]}]: ")
        y = turtle.numinput(f"POLYGON MAKER", f"Enter y control point for [{vertices[i]} to {vertices[(i + 1) % len(vertices)]}]: ")
        curve_points.append((x, y))
      else:
        curve_points.append(None)

  # Ask the user for transformation choice
  choice = turtle.textinput("POLYGON MAKER", "Transformation? (y/n)")
  if choice.lower() == 'y':
    transform_choice = int(turtle.numinput("Transformation choice", "Enter your choice: 1. Translation\n2.Rotation\n3.x reflection\n4.y reflection\n5.x shearing\n6.y shearing\n7.scaling"))
    if transform_choice == 1:
      dx = float(turtle.numinput("POLYGON MAKER", "x translation:"))
      dy = float(turtle.numinput("POLYGON MAKER", "y translation:"))
      vertices = translate(vertices, dx, dy)
    elif transform_choice == 2:
      angle = float(turtle.numinput("POLYGON MAKER", "rotation angle in degrees:"))
      vertices = rotate(vertices, angle)
    elif transform_choice == 3:
      vertices = reflect(vertices, True)
    elif transform_choice == 4:
      vertices = reflect(vertices, False)
    elif transform_choice == 5:
      k = float(turtle.numinput("POLYGON MAKER", "shearing factor:"))
      vertices = shear(vertices, k, True)
    elif transform_choice == 6:
      k = float(turtle.numinput("POLYGON MAKER", "shearing factor:"))
      vertices = shear(vertices, k, False)  
    elif transform_choice == 7:
      sx = float(turtle.numinput("POLYGON MAKER", "x scaling factor:"))
      sy = float(turtle.numinput("POLYGON MAKER", "y scaling factor:"))
      vertices = transform_size(vertices, sx, sy)

  # Ask the user if they want to create a pattern
  pattern = turtle.textinput('POLYGON MAKER',"pattern? (y/n)")
  if pattern.lower() == 'y':
    num_patterns = int(turtle.numinput("POLYGON MAKER", "number of patterns? (INTEGER > 0):"))
    pattern_maker(vertices, edges, colors, curve_points, num_patterns)

  try:
    # Create the polygon using the transformed data
    polygon_data = polygon_maker(vertices, edges, colors, curve_points)
  except:
    print("Try again please")

  # If the polygon was not opened from a file, save the data to a file
  if not opened:
    with open("polygon_output.txt", 'a') as output_file:
      output_file.write("\n")
      try:
        file_maker(output_file, polygon_data)
      except:
        pass

  # Ask the user if they want to create another polygon
  choice = turtle.textinput("POLYGON MAKER", "another polygon? (y/n)")
  if choice.lower() == 'y':
    main()
  else:
    turtle.bye()

# Call the main function
if __name__ == "__main__":
  main()

