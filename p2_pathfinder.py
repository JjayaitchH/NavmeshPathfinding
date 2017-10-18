from heapq import heappop, heappush
from math import sqrt

def find_path (source_point, destination_point, mesh):
    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    path = []
    boxes = {}
    detailed_points = {}
    
    #locates boxes containing boxes with dest and source. y1, x1 is origin
    a = locate_Box(source_point, mesh)
    b = locate_Box(destination_point, mesh)

    
    #Fillingn dictionaries and lists n shit
    detailed_points[a] = source_point
    f_detailed_points
    b_detailed_points
    
    #A* Stuff
    start_heuristic = calc_distance(source_point, destination_point)
    end_heuristic = calc_distance(destination_point, destination_point) #yeah, I know it's just 0
    queue = [(start_heuristic, a, 'destination')]
    heappush(queue, (end_heuristic, b, 'initial'))

    
    distances = {}
    distances[a] = 0
    f_distances = {} # f = forward
    b_distances = {} # b = backward

    f_backpointers = {} # f = forward
    b_backpointers = {} # b = backward
    backpointers = {}
    backpointers[a] = None

    while queue:
        current_dist, current_box, curr_goal = heappop(queue)

        if current_box in f_backpointers and current_box in b_backpointers:
            f_current_back_box = f_backpointers[current_box]
            b_current_back_box = b_backpointers[current_box]

            while f_current_back_box is not None:
                if f_backpointers[f_current_back_box] != None:
                    path.append((f_detailed_points[f_backpointers[f_current_back_box]],f_detailed_points[f_current_back_box]))
                f_current_back_box = f_backpointers[f_current_back_box]

            while b_current_back_box is not None:
                if b_backpointers[b_current_back_box] != None:
                    path.append((b_detailed_points[b_backpointers[b_current_back_box]],b_detailed_points[b_current_back_box]))
                b_current_back_box = b_backpointers[b_current_back_box]
                
            return path, boxes.keys()
        
        for adj_box in mesh['adj'][current_box]:
            closest_point = get_closest_point(detailed_points[current_box], adj_box)
            path_cost = current_dist + calc_distance(detailed_points[current_box], closest_point)
            boxes[adj_box] = closest_point
        
            if adj_box not in distances or path_cost < distances[adj_box]:
                #########################################################
                if curr_goal == 'destination': 
                    distances[adj_box] = path_cost
                    f_distances[adj_box] = path_cost
                    detailed_points[adj_box] = closest_point
                    f_detailed_points[adj_box] = closest_point
                    new_heuristic = calc_distance(closest_point, destination_point)
                    heappush(queue,((distances[adj_box] + new_heuristic), adj_box, 'destination'))
                    backpointers[adj_box] = current_box
                    f_backpointers[adj_box] = current_box
                elif curr_goal == 'initial':
                    distances[adj_box] = path_cost
                    b_distances[adj_box] = path_cost
                    detailed_points[adj_box] = closest_point
                    b_detailed_points[adj_box] = closest_point
                    new_heuristic = calc_distance(closest_point, destination_point)
                    heappush(queue, ((distances[adj_box] + new_heuristic), adj_box, 'initial'))
                    backpointers[adj_box] = current_box
                    b_backpointers[adj_box] = current_box
                #########################################################
                
    path.append((source_point,destination_point))
    return path, boxes.keys()

def locate_Box(point, mesh):
    for currBox in mesh['boxes']:
        if in_Bounds(point,currBox):
            print("BOX FOUND")
            return currBox
    return None

def in_Bounds(point, box):
    yBounds = False
    xBounds = False
    if box[0]<=point[0] and point[0]<=box[1]:
        yBounds = True
    if box[2]<=point[1] and point[1]<=box[3]:
        xBounds = True
    return yBounds and xBounds

#key is point, [0] is start point, [1] is destination point
def get_closest_point (point, targetBox):
    result_point = []
    if point[0] < targetBox[0]:
        result_point.append(targetBox[0])
    elif point[0] > targetBox[1]:
        result_point.append(targetBox[1])
    else:
        result_point.append(point[0])

    if point[1] < targetBox[2]:
        result_point.append(targetBox[2])
    elif point[1] > targetBox[3]:
        result_point.append(targetBox[3])
    else:
        result_point.append(point[1])
    return tuple(result_point)

def calc_distance( pointA, pointB):
    return sqrt((pointA[0]+pointB[0])**2+(pointA[1]+pointB[1])**2)