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
    
    #A* Stuff
    queue = [(0, a)]
    
    distances = {}
    distances[a] = 0

    backpointers = {}
    backpointers[a] = None

    while queue:
        current_dist, current_box = heappop(queue)

        if current_box == b:
            #path = [(source_point,destination_point)]
            current_back_box = backpointers[current_box]
            path.append((detailed_points[current_box],destination_point))
            path.append((detailed_points[current_back_box],detailed_points[current_box]))

            while current_back_box is not None:
                if backpointers[current_back_box] != None:
                    path.append((detailed_points[backpointers[current_back_box]],detailed_points[current_back_box]))
                current_back_box = backpointers[current_back_box]
                
            return path, boxes.keys()
        
        for adj_box in mesh['adj'][current_box]:
            closest_point = get_closest_point(detailed_points[current_box], adj_box)
            path_cost = current_dist + calc_distance(detailed_points[current_box], closest_point)
            boxes[adj_box] = closest_point
        
            if adj_box not in distances or path_cost < distances[adj_box]:
                distances[adj_box] = path_cost
                detailed_points[adj_box] = closest_point
                new_heuristic = calc_distance(closest_point, destination_point)
                heappush(queue,((distances[adj_box] + new_heuristic), adj_box))
                backpointers[adj_box] = current_box

        """
        for adj_box in mesh['adj'][current_box]:
            closePoint = get_closest_point(detailed_points[current_box], adj_box)
            pathcost = current_dist + calc_distance(detailed_points[current_box], closePoint)
            
            if adj_box not in distances or pathcost < distances[adj_box]:
                boxes[adj_box] = closePoint
                detailed_points[adj_box] = closePoint
                distances[adj_box] = pathcost
                backpointers[adj_box] = current_box
                #path.append((detailed_points[current_box],detailed_points[adj_box]))
                heappush(queue, (pathcost, adj_box))
                """
                
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