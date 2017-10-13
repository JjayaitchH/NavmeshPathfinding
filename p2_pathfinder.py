def find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    path = []    boxes = {}###This part enclosed in # symbols is the Dijkstra's solution professor provided#####################    for a, b in mesh['boxes']:        if a == source_point:            path.append(a)        if b == destination_point:            path.append(b)    queue = [(0, source_point)]    distances = {}    distances[source_point] = 0    backpointers = {}    backpointers[source_point] = None    while queue:        current_dist, current_node = heappop(queue)        if current_node == destination_point:            path = [current_node]            current_back_node = backpointers[current_node]            while current_back_node is not None:                path.append(current_back_node)                current_back_node = backpointers[current_back_node]            return path, boxes.keys()        for adj_node, adj_node_cost in adj(mesh, current_node):            pathcost = current_dist + adj_node_cost            if adj_node not in distances or pathcost < distances[adj_node]:                distances[adj_node] = pathcost                backpointers[adj_node] = current_node                heappush(queue, (pathcost, adj_node))###################################################################################################    return path, boxes.keys()