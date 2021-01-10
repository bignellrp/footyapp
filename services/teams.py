import heapq

def even_teams(game_players, n=2):
    teams = [[] for _ in range(n)]
    totals = [(0, i) for i in range(n)]
    heapq.heapify(totals)
    for obj in game_players:
        total, index = heapq.heappop(totals)
        teams[index].append(obj)
        heapq.heappush(totals, (total + obj[1], index))
    return tuple(teams)