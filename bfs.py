from collections import deque


def bfs(graph, start, goal):
    # create a queue for BFS
    queue = deque([(start, [])])
    visited = set()

    # loop until the queue is empty
    while queue:
        # dequeue the first vertex and its path
        vertex, path = queue.popleft()

        # if the vertex has not been visited yet
        if vertex not in visited:
            # mark the vertex as visited
            visited.add(vertex)

            # if the vertex is the goal, return the path
            if vertex == goal:
                return path + [vertex]

            # add all the neighbors of the vertex to the queue
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [vertex]))

    # if the goal cannot be reached from the start, return None
    return None