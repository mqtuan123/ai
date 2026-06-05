import math
import heapq


def euclidean_distance(node1, node2):
    return math.sqrt(
        (node1["lat"] - node2["lat"]) ** 2 +
        (node1["lng"] - node2["lng"]) ** 2
    )


def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def find_shortest_path(graph, start_id, end_id):

    open_set = []

    heapq.heappush(open_set, (0, start_id))

    came_from = {}

    g_score = {
        node_id: float("inf")
        for node_id in graph
    }

    g_score[start_id] = 0

    f_score = {
        node_id: float("inf")
        for node_id in graph
    }

    f_score[start_id] = euclidean_distance(
        graph[start_id],
        graph[end_id]
    )

    while open_set:

        _, current = heapq.heappop(open_set)

        if current == end_id:
            return reconstruct_path(
                came_from,
                current
            )

        for neighbor in graph[current]["neighbors"]:

            tentative_g = (
                g_score[current]
                + euclidean_distance(
                    graph[current],
                    graph[neighbor]
                )
            )

            if tentative_g < g_score[neighbor]:

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score[neighbor] = (
                    tentative_g
                    + euclidean_distance(
                        graph[neighbor],
                        graph[end_id]
                    )
                )

                heapq.heappush(
                    open_set,
                    (
                        f_score[neighbor],
                        neighbor
                    )
                )

    return []