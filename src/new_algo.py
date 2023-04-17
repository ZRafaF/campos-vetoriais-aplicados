import heapq


def dijkstra(matrix, start, goal):
    """Finds the shortest path between start and goal in a weighted 2D matrix"""
    rows, cols = len(matrix), len(matrix[0])
    heap = [(0, start)]
    visited = set()
    distances = {start: 0}
    predecessors = {start: None}

    while heap:
        current_distance, current = heapq.heappop(heap)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = predecessors[current]
            return list(reversed(path))

        if current in visited:
            continue

        visited.add(current)

        for row, col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbor = (current[0] + row, current[1] + col)

            if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                continue

            distance = matrix[neighbor[0]][neighbor[1]] + current_distance

            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current
                heapq.heappush(heap, (distance, neighbor))

    return None
