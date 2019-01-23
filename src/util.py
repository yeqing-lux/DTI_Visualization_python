import nibabel as nib
import pickle
import numpy as np
import copy
import time
import vtk


def read(path, cos, FA):
    """
    Load NIfTI document and calculate Direction dictionary.
    Direction dictionary: A dictionary which stores the velocity, color and FA value of each voxel. In the form of:
      Direction dictionary = {key: the coordinate of voxel, value: [(Vx, Vy, Vz), (R,G,B), FA]}.
      Velocity = (Vx, Vy, Vz) is the principal eigen vector of tensor matrix.
      color: A tuple stores FA color coding of the voxel.
        color = (R, G, B) = FA * (Vx, Vy, Vz)
      FA value: A scalar between 0 and 1, which represents the anisotropy of the voxel.

    :param path: The path of NIfTI document.
    :param cos: Cosine threshold of fiber tracking.
    :param FA: FA value threshold of fiber tracking.

    :return: A list of fiber information.
        line_data = [fiber1, fiber2, ...]
        where fiber_i = [point1, point2, point3, ...]
        where point_i = [(x,y,z), (R,G,B)]
    """
    img = nib.load(path)  # load
    img_data = img.get_data()
    img_data = img_data.reshape(7, 148, 190, 160)# Reshape the size of input data. Temporarily only support test file. 
    #TODO: Modify the code to handle more files.
    
    Direction_dic = generate_direction_dic(img_data)
    line_data = initial_seed(500, Direction_dic, cos=cos, FA=FA)
    return line_data


def generate_direction_dic(img_data):
    """
    Generate direction dictionary from image data.

    Direction dictionary: A dictionary which stores the velocity, color and FA value of each voxel. In the form of:
        Direction dictionary = {key: the coordinate of voxel, value: [(Vx, Vy, Vz), (R,G,B), FA]}.
        Velocity = (Vx, Vy, Vz) is the principal eigen vector of tensor matrix.
        color: A tuple stores FA color coding of the voxel.
            color = (R, G, B) = FA * (Vx, Vy, Vz)
        FA value: A scalar between 0 and 1, which represents the anisotropy of the voxel.

    :param img_data: A NIfTI.get_data object, img_data[:][x][y][z] is the tensor matrix information of voxel (x,y,z)
    :return: Generated direction dictionary.
    """

    Direction_dic = {}

    start = time.time()
    shape = img_data.shape
    for x in range(shape[1]):
        for y in range(shape[2]):
            for z in range(shape[3]):
                # get D_vector from img_data and reconstruction tensor matrix.
                D_vector = img_data[:, x, y, z]
                D = np.array(
                    [[D_vector[1], D_vector[2], D_vector[3]],
                     [D_vector[2], D_vector[4], D_vector[5]],
                     [D_vector[3], D_vector[5], D_vector[6]]])

                eigen_value, eigen_vector = np.linalg.eig(D)
                eigen_value = np.abs(eigen_value)

                # calculate FA for each vixel
                eigen_value_average = eigen_value.sum() / 3
                if sum([i ** 2 for i in eigen_value]) != 0:
                    FA = 1.5 * sum([(i - eigen_value_average) ** 2 for i in eigen_value]) / sum(
                        [i ** 2 for i in eigen_value])
                    FA = np.sqrt(FA)
                else:
                    FA = 0

                # get the index of largest eigenvalue
                idx = np.argmax((np.abs(eigen_value)))
                color = FA * np.abs(eigen_vector[:, idx])
                Direction_dic[(x, y, z)] = [tuple(eigen_vector[:, idx]), tuple(color), FA]
               
    print(time.time() - start)

    return Direction_dic

# use pickle to load middle results
def write_in_pickle(data, path):
    output = open(path, 'wb')
    pickle.dump(data, output)
    output.close()


def load_pickle(path):
    pkl_file = open(path, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data


def initial_seed(N, Direction_dic, cos, FA):
  """
  Generate initial seeds and track fibers from each intial seed. We want the FA of initial seeds are larger than 0.8,
  in order to reduce some noise.

  :param N:  The number of initial seeds.
  :param Direction_dic: A dictionary which stores the velocity, color and FA value of each voxel. In the form of:
       Direction dictionary = {key: the coordinate of voxel, value: [(Vx, Vy, Vz), (R,G,B), FA]}.
       Velocity = (Vx, Vy, Vz) is the principal eigen vector of tensor matrix.
       color: A tuple stores FA color coding of the voxel.
         color = (R, G, B) = FA * (Vx, Vy, Vz)
       FA value: A scalar between 0 and 1, which represents the anisotropy of the voxel.

  :param cos: The cosine threshold of track.
  :param FA: The FA threshold of track.

  :return: A list of fiber information.
       line_data = [fiber1, fiber2, ...]
       fiber_i = [point1, point2, point3, ...]
       point_i = [(x,y,z), (R,G,B)]
  """

  data = []

  for i in range(N):
    randx, randy, randz = np.random.uniform(size=3) * [100.0, 140.0, 120.0] + 20
    if Direction_dic[(int(randx), int(randy), int(randz))][2] < 0.8:
      init_location = tuple((randx, randy, randz))

      # Use 'track' function to track each initial seed's fiber
      data = data + track(init_location, Direction_dic, threshold_cos=cos, threshold_FA=FA)
  return data


def track(init_location, para_dic, threshold_cos=0.3, threshold_FA=0.05):
    """
    Given initial location and the movement trend of each voxel,
    return a track list containing ordered points.

    @param init_location: a tuple of location (x, y, z)
    @param para_dic: {key: the coordinate of voxe, value: [(Vx, Vy, Vz), (R,G,B), FA]}
    @param threshold_FA: the decimal in (0~1)
    @param threshold_cos: the cos of the theta of two voxels

    @return: a list of track(fibers), each item is also a list,
             it's first item is a coordinate and the second is RGB.
             track = [point1, point2, point3, ...]
             point_i = [(x,y,z), (R,G,B)]
    """

    end_track_list = []
    successor_stack = []

    # the three dims
    x_lim, y_lim, z_lim = 147.0, 189.0, 159.0
    x0, y0, z0 = init_location
    voxe_x, voxe_y, voxe_z = int(x0), int(y0), int(z0)
    if float(int(x0)) == x0 or float(int(y0)) == y0 or float(int(z0)) == z0:
        return []
    V, RGB, FA = para_dic[(voxe_x, voxe_y, voxe_z)]
    Vx, Vy, Vz = V

    # initialized two direction
    for Vx, Vy, Vz in [(Vx, Vy, Vz), (-Vx, -Vy, -Vz)]:
        tx = (voxe_x - x0 + 1) / Vx if Vx > 0 else (x0 - voxe_x) / (abs(Vx) + 1e-10)
        ty = (voxe_y - y0 + 1) / Vy if Vy > 0 else (y0 - voxe_y) / (abs(Vy) + 1e-10)
        tz = (voxe_z - z0 + 1) / Vz if Vz > 0 else (z0 - voxe_z) / (abs(Vz) + 1e-10)
        t_end = min(tx, ty, tz)
        x1, y1, z1 = round(x0 + Vx * t_end, 2), round(y0 + Vy * t_end, 2), round(z0 + Vz * t_end, 2)
        if x1 in [x_lim, 0] or y1 in [y_lim, 0] or z1 in [z_lim, 0]:
            continue
        successor_stack.append([(voxe_x, voxe_y, voxe_z), [((x0, y0, z0), None), ((x1, y1, z1), RGB)], 0])

    if len(successor_stack) == 2:
        successor_stack[1][2] = 1

    # generate tracks via stack(employing list)
    while successor_stack:
        (voxe_x, voxe_y, voxe_z), temp_track, turned = successor_stack.pop()
        outset_x, outset_y, outset_z = temp_track[-1][0]
        X_is_int = float(int(outset_x)) == outset_x
        Y_is_int = float(int(outset_y)) == outset_y
        Z_is_int = float(int(outset_z)) == outset_z

        # find all possible next voxe
        if X_is_int and Y_is_int and Z_is_int:
            if int(outset_x) == voxe_x and int(outset_y) == voxe_y and int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(-1, 1)
                                 for j in range(-1, 1) for k in range(-1, 1) if i or j or k]
            elif int(outset_x) == voxe_x and int(outset_y) == voxe_y:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(-1, 1)
                                 for j in range(-1, 1) for k in range(0, 2) if i or j or k]
            elif int(outset_x) == voxe_x and int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(-1, 1)
                                 for j in range(0, 2) for k in range(-1, 1) if i or j or k]
            elif int(outset_y) == voxe_y and int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(0, 2)
                                 for j in range(-1, 1) for k in range(-1, 1) if i or j or k]
            elif int(outset_x) == voxe_x:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(-1, 1)
                                 for j in range(0, 2) for k in range(0, 2) if i or j or k]
            elif int(outset_y) == voxe_y:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(0, 2)
                                 for j in range(-1, 1) for k in range(0, 2) if i or j or k]
            elif int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(0, 2)
                                 for j in range(0, 2) for k in range(-1, 1) if i or j or k]
            else:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z + k) for i in range(0, 2)
                                 for j in range(0, 2) for k in range(0, 2) if i or j or k]
        elif X_is_int and Y_is_int:
            if int(outset_x) == voxe_x and int(outset_y) == voxe_y:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z) for i in range(-1, 1)
                                 for j in range(-1, 1) if i or j]
            elif int(outset_x) == voxe_x:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z) for i in range(-1, 1)
                                 for j in range(0, 2) if i or j]
            elif int(outset_y) == voxe_y:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z) for i in range(0, 2)
                                 for j in range(-1, 1) if i or j]
            else:
                possible_voxe = [(voxe_x + i, voxe_y + j, voxe_z) for i in range(0, 2)
                                 for j in range(0, 2) if i or j]
        elif X_is_int and Z_is_int:
            if int(outset_x) == voxe_x and int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x + i, voxe_y, voxe_z + j) for i in range(-1, 1)
                                 for j in range(-1, 1) if i or j]
            elif int(outset_x) == voxe_x:
                possible_voxe = [(voxe_x + i, voxe_y, voxe_z + j) for i in range(-1, 1)
                                 for j in range(0, 2) if i or j]
            elif int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x + i, voxe_y, voxe_z + j) for i in range(0, 2)
                                 for j in range(-1, 1) if i or j]
            else:
                possible_voxe = [(voxe_x + i, voxe_y, voxe_z + j) for i in range(0, 2)
                                 for j in range(0, 2) if i or j]
        elif Y_is_int and Z_is_int:
            if int(outset_y) == voxe_y and int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x, voxe_y + i, voxe_z + j) for i in range(-1, 1)
                                 for j in range(-1, 1) if i or j]
            elif int(outset_y) == voxe_y:
                possible_voxe = [(voxe_x, voxe_y + i, voxe_z + j) for i in range(-1, 1)
                                 for j in range(0, 2) if i or j]
            elif int(outset_z) == voxe_z:
                possible_voxe = [(voxe_x, voxe_y + i, voxe_z + j) for i in range(0, 2)
                                 for j in range(-1, 1) if i or j]
            else:
                possible_voxe = [(voxe_x, voxe_y + i, voxe_z + j) for i in range(0, 2)
                                 for j in range(0, 2) if i or j]
        elif X_is_int:
            possible_voxe = [(voxe_x - 1, voxe_y, voxe_z)] if int(outset_x) == voxe_x else [
                (voxe_x + 1, voxe_y, voxe_z)]
        elif Y_is_int:
            possible_voxe = [(voxe_x, voxe_y - 1, voxe_z)] if int(outset_y) == voxe_y else [
                (voxe_x, voxe_y + 1, voxe_z)]
        elif Z_is_int:
            possible_voxe = [(voxe_x, voxe_y, voxe_z - 1)] if int(outset_z) == voxe_z else [
                (voxe_x, voxe_y, voxe_z + 1)]
        else:
            raise Exception("No integer!!!")

        # select situable next voxel
        for next_voxe in possible_voxe:
            next_x, next_y, next_z = next_voxe
            delta_x, delta_y, delta_z = next_x - voxe_x, next_y - voxe_y, next_z - voxe_z
            if turned:
                current_V = -np.array(para_dic[(voxe_x, voxe_y, voxe_z)][0])
            else:
                current_V = para_dic[(voxe_x, voxe_y, voxe_z)][0]
            next_V, next_RGB, next_FA = para_dic[next_voxe]
            next_vx, next_vy, next_vz = next_V

            no_into = 0
            if next_FA <= threshold_FA:
                no_into = 1
            else:
                if next_vx * delta_x >= 0 and next_vy * delta_y >= 0 and next_vz * delta_z >= 0:
                    next_turn = 0
                    cos_value = np.dot(current_V, next_V)
                else:
                    next_vx, next_vy, next_vz = -np.array(next_V)
                    next_turn = 1
                    cos_value = np.dot(current_V, -np.array(next_V))

                if cos_value >= threshold_cos:
                    tx = (next_x - outset_x + 1) / next_vx if next_vx > 0 else (outset_x - next_x) / (
                        abs(next_vx) + 1e-10)
                    ty = (next_y - outset_y + 1) / next_vy if next_vy > 0 else (outset_y - next_y) / (
                        abs(next_vy) + 1e-10)
                    tz = (next_z - outset_z + 1) / next_vz if next_vz > 0 else (outset_z - next_z) / (
                        abs(next_vz) + 1e-10)
                    t_end = min(tx, ty, tz)
                    x1, y1, z1 = round(outset_x + next_vx * t_end, 2), round(outset_y + next_vy * t_end, 2), round(
                        outset_z + next_vz * t_end, 2)
                    possible_item = ((x1, y1, z1), next_RGB)
                    increased_track = copy.deepcopy(temp_track)
                    increased_track.append(possible_item)
                    if possible_item in temp_track or x1 in [x_lim, 0] or y1 in [y_lim, 0] or z1 in [z_lim, 0]:
                        end_track_list.append(increased_track)
                    else:
                        successor_stack.append([next_voxe, increased_track, next_turn])
                else:
                    no_into = 1
            if no_into:
                if end_track_list:
                    last_track = end_track_list[-1]
                    if set(temp_track).issubset(set(last_track)):
                        continue
                    elif set(last_track).issubset(set(temp_track)):
                        end_track_list[-1] = temp_track
                        continue
                    else:
                        end_track_list.append(temp_track)
                else:
                    end_track_list.append(temp_track)
    return end_track_list


def generate_volume_data(img_data):
    """
    Generate volume data from img_data.

    :param img_data: A NIfTI.get_data object, img_data[:][x][y][z] is the tensor matrix information of voxel (x,y,z)img_data:
    :return: vtkImageData object which stores volume render object.
    """
    dims = [148, 190, 160]  # size of input data. Temporarily only support test file. 
    #TODO: Modify the code to handle more files.
    
    image = vtk.vtkImageData()
    image.SetDimensions(dims[0] - 2 , dims[1] - 2 , dims[2] - 2 )
    image.SetSpacing(1, 1, 1)                          # set spacing
    image.SetOrigin(0, 0, 0)
    image.SetExtent(0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1)
    image.AllocateScalars(vtk.VTK_UNSIGNED_SHORT, 1)

    for z in range(0, dims[2]-1):
        for y in range(0, dims[1]-1 ):
            for x in range(0, dims[0]-1 ):
                scalardata = img_data[0][x][y][z]       # set confidence as each voxel's scalardata
                image.SetScalarComponentFromFloat(x, y, z, 0, scalardata)

    return image


def createLine(renderer, a=1.5, b=60, line_data=None,
               circle_actor=None, line_color=None):
    """
    A backend of GUI, which draws DTI fibers on the renderer.
    In this function, we set each fiber as a vtkLine object, which is formed by connecting every two adjacent points.
    Each segment of a line has its own color, which is FA color coding by default but can be changed to any color.
    A linear transformation is used when converting color contrast and brightness.

    :param renderer: A vtkRender object.
    :param a: Contrast parameter. The larger a is, the larger the contrast.
    :param b: Brightness parameter. The larger b is, the brighter the fibers are.
    :param line_data: A list of fiber information.
           line_data = [fiber1, fiber2, ...]
           fiber_i = [point1, point2, point3, ...]
           point_i = [(x,y,z), (R,G,B)]
    :param circle_actor: A vtkActor object, which stores ROI circle.
    :param line_color: The color of fiber lines.

    :return: None
    """
    # instantiate containers that store colors, points, and lines
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)       # RGB color
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()            # store all lines(each line is a fiber)

    count = 0                             # used to correspond the order of points with each line segment
    for line_item in line_data:
        if len(line_item) < 25:           # don't show lines that are really short
            continue

        for item in line_item:
            point = item[0]
            points.InsertNextPoint(point)

            if item[1] is not None:      # the first point of each line doesn't have color attribution
                if line_color is not None:
                    color = line_color   
                else:
                    color = [min(255, int(i * 255 * a + b)) for i in item[1]]
                colors.InsertNextTypedTuple(color)

        for i in range(len(line_item) - 1): # connect breakpoints on one fiber in order
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, count)
            line.GetPointIds().SetId(1, count + 1)
            count += 1
            lines.InsertNextCell(line)

        count += 1

    linesPolyData = vtk.vtkPolyData()   # store all the fibers(lines)
    linesPolyData.SetPoints(points)
    linesPolyData.SetLines(lines)
    linesPolyData.GetCellData().SetScalars(colors)

    # Create a mapper and actor for initial dataset
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(linesPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetLineWidth(2)
    actor.GetProperty().SetDiffuse(1)
    actor.GetProperty().SetDiffuseColor(1.0, 1.0, 1.0)
    actor.GetProperty().SetEdgeColor(1, 1, 1)
    actor.GetProperty().SetOpacity(.5)

    renderer.AddActor(actor)
    renderer.ResetCamera()

    # If there's a ROI circle actor, add it to renderer.
    if circle_actor is not None:
        renderer.AddActor(circle_actor)


def ROIsearch(data, center, r, indicator):
    """
    This equation screens all fibers, leaving only the fibers that pass through the ROI.

    :param data:      The original line_data which stores all the fiber.
    :param center:    The center coordinates of the ROI.
    :param r:         The radius of ROI.
    :param indicator: Indicates which plane the circle is on. (0: YZ plane, 1: XZ plane, 2: XY plane.

    :return: A list of fibers that pass through the ROI.
    """

    ROIdata = []
    for line in data:
        for i in range(len(line) - 1):
            # Find two points on the fiber just across the plane.
            if ((line[i][0][indicator] - center[indicator]) * (line[i + 1][0][indicator] - center[indicator])) <= 0:

                # Calculate the distance from the center of ROI to the point
                if sum((np.array(line[i][0]) - np.array(center)) ** 2) < (r + 1) ** 2:
                    ROIdata.append(line)

    return ROIdata


def ROI_circlePolyData(center, r, indicator):
    """
    Create a vtkActor object of ROI circle.

    :param center:    The center coordinates of the ROI.
    :param r:         The radius of ROI.
    :param indicator: Indicates which plane the circle is on. (0: YZ plane, 1: XZ plane, 2: XY plane.

    :return: A vtkActor object.
    """
    # Create points of the circle.
    circle_data = []
    for i in range(180):
        circle_data.append([r * np.cos(float(i * np.pi / 90)), r * np.sin(float(i * np.pi / 90))])
        circle_data[i].insert(indicator, 0)
        circle_data[i] = np.array(circle_data[i]) + np.array(center)

    circle_points = vtk.vtkPoints()      # store all the points on the circle
    circle = vtk.vtkCellArray()          # store all the line segments on the circle
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)

    for point in circle_data:
        circle_points.InsertNextPoint(point)

    for i in range(len(circle_data) - 1):
        line = vtk.vtkLine()
        # Connect two adjacent points with line segments
        line.GetPointIds().SetId(0, i)
        line.GetPointIds().SetId(1, i + 1)

        circle.InsertNextCell(line)
        colors.InsertNextTypedTuple([255, 0, 0])    # red color

    line = vtk.vtkLine()
    line.GetPointIds().SetId(0, len(circle_data) - 1)
    line.GetPointIds().SetId(1, 0)
    circle.InsertNextCell(line)
    colors.InsertNextTypedTuple([255, 0, 0])

    circlePolyData = vtk.vtkPolyData()
    circlePolyData.SetPoints(circle_points)
    circlePolyData.SetLines(circle)
    circlePolyData.GetCellData().SetScalars(colors)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(circlePolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetLineWidth(5)

    return actor


def slice(renderer, window, interactor, interactorStyle, indicator,
          img1=None, circle_actor=None, line_color=None):
    """
    This function is a vtk function, which visualizes the slice of a dimension. A vtkImageReslice object is used in
    visualization, which is a very useful tool in Medical Image Slice Visualization.

    :param renderer: A vtkRender object.
    :param window: A vtkRenderWindow object.
    :param interactor: A vtkRenderWindowInteractor object.
    :param interactorStyle: A vtkRenderWindowInteractorStyle object.
    :param indicator: Indicates the plane (i.e. XY, XZ, YZ)
    :param img1: The origin data which is loaded by library nibabel.
    :param circle_actor: A vtkActor object, which stores ROI circle.
    :param line_color: The color of fiber lines.

    :return: None
    """

    img1_data = img1.get_data()                                # obtain scale data
    img1_data = img1_data.reshape(7, 148, 190, 160)
    #TODO: Modify the code to handle more files.
    
    dims = img1_data.shape[1:]  # [124,124,73]                 # dimension

    spacing = (img1.header['pixdim'][1], img1.header['pixdim'][2], img1.header['pixdim'][3]) # set spacing

    image = vtk.vtkImageData()
    image.SetDimensions(dims[0], dims[1], dims[2])             # set dimensions
    image.SetSpacing(spacing[0], spacing[1], spacing[2])       # set spacing
    image.SetOrigin(0, 0, 0)                                   # set origin
    image.SetExtent(0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1)
    extent = [0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1]
    origin = [0, 0, 0]
    center = np.zeros((3, 1))                                  # calculate center which is important in reslice
    center[0] = origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1])
    center[1] = origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3])
    center[2] = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])

    if vtk.VTK_MAJOR_VERSION <= 5:
        image.SetNumberOfScalarComponents(1)                   # vtkImageData sclalarArray tuple'size
        image.SetScalarTypeToUnsignedShort()
    else:
        image.AllocateScalars(vtk.VTK_UNSIGNED_SHORT, 1)


    intRange = (-100, 900)
    max_u_short = 1000
    for z in range(dims[2]):
        for y in range(dims[1]):
            for x in range(dims[0]):
                scalardata = img1_data[0][x][y][z]
                if scalardata < intRange[0]:
                    scalardata = intRange[0]
                if scalardata > intRange[1]:
                    scalardata = intRange[1]
                scalardata = max_u_short * np.float(scalardata - intRange[0]) / np.float(intRange[1] - intRange[0])
                image.SetScalarComponentFromFloat(x, y, z, 0, scalardata)

    # Matrices for axial, coronal, sagittal view orientations
    axial = vtk.vtkMatrix4x4()
    axial.DeepCopy((1, 0, 0, center[0],
                    0, 1, 0, center[1],
                    0, 0, 1, center[2],
                    0, 0, 0, 1))

    coronal = vtk.vtkMatrix4x4()
    coronal.DeepCopy((1, 0, 0, center[0],
                      0, 0, 1, center[1],
                      0, -1, 0, center[2],
                      0, 0, 0, 1))

    sagittal = vtk.vtkMatrix4x4()
    sagittal.DeepCopy((0, 0, -1, center[0],
                       1, 0, 0, center[1],
                       0, -1, 0, center[2],
                       0, 0, 0, 1))

    # Extract a slice in the desired orientation
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(image)
    reslice.SetOutputDimensionality(2)
    reslice.SetInterpolationModeToLinear()

    # Set transform matrix corresponding to indicator
    if indicator == 0:
        reslice.SetResliceAxes(sagittal)
    elif indicator == 1:
        reslice.SetResliceAxes(axial)
    elif indicator == 2:
        reslice.SetResliceAxes(coronal)

    # Create a greyscale lookup table
    table = vtk.vtkLookupTable()
    table.SetRange(0, 2000)              # image intensity range
    table.SetValueRange(0.0, 1.0)        # from black to white
    table.SetSaturationRange(0.0, 0.0)   # no color saturation
    table.SetRampToLinear()
    table.Build()

    # Map the image through the lookup table
    color = vtk.vtkImageMapToColors()
    color.SetLookupTable(table)
    color.SetInputConnection(reslice.GetOutputPort())

    # Display the image
    actor = vtk.vtkImageActor()
    actor.GetMapper().SetInputConnection(color.GetOutputPort())

    renderer.AddActor(actor)

    # Create callbacks for slicing the image
    actions = {}
    actions["Slicing"] = 0
    def ButtonCallback(obj, event):
        if event == "LeftButtonPressEvent":
            actions["Slicing"] = 1
        else:
            actions["Slicing"] = 0

    def MouseMoveCallback(obj, event):
        (lastX, lastY) = interactor.GetLastEventPosition()
        (mouseX, mouseY) = interactor.GetEventPosition()
        if actions["Slicing"] == 1:
            deltaY = (mouseY - lastY) / 5
            reslice.Update()
            sliceSpacing = reslice.GetOutput().GetSpacing()[2]
            matrix = reslice.GetResliceAxes()

            # move the center point that we are slicing through
            center = matrix.MultiplyPoint((0, 0, sliceSpacing * deltaY, 1))
            matrix.SetElement(0, 3, center[0])
            matrix.SetElement(1, 3, center[1])
            matrix.SetElement(2, 3, center[2])
            window.Render()
        else:
            interactorStyle.OnMouseMove()

    interactorStyle.AddObserver("MouseMoveEvent", MouseMoveCallback)
    interactorStyle.AddObserver("LeftButtonPressEvent", ButtonCallback)
    interactorStyle.AddObserver("LeftButtonReleaseEvent", ButtonCallback)

