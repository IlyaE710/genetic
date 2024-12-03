import random
from pprint import pprint
from collections import defaultdict

# Функция для оценки приспособленности пути
def fitness(path, edges):
    used_edges = set()
    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        if edge not in edges:
            return float('-inf')  # Путь содержит недопустимое ребро
        used_edges.add(edge)
    return len(used_edges)  # Чем больше уникальных рёбер, тем лучше

# Инициализация случайной популяции
def initialize_population(size, start_node, graph, edges):
    population = []
    for _ in range(size):
        path = [start_node]
        current = start_node
        while len(path) < len(edges) + 1:  # Добавляем рёбра
            next_nodes = graph.get(current, [])
            if not next_nodes:
                break
            next_node = random.choice(next_nodes)
            path.append(next_node)
            current = next_node
        population.append(path)
    return population

# Кроссовер
def crossover(parent1, parent2):
    if len(parent1) - 2 == 0 or len(parent2) - 2 == 0:
        print(max(parent1, parent2))
        return max(parent1, parent2)
    cut1 = random.randint(1, len(parent1) - 2)
    cut2 = random.randint(1, len(parent2) - 2)
    child = parent1[:cut1] + parent2[cut2:]
    return child

# Мутация
# def mutate(path):
#     if len(path) > 2:
#         i = random.randint(0, len(path) - 2)
#         j = random.randint(0, len(path) - 2)
#         path[i], path[j] = path[j], path[i]
#         path.append(path[j])
#         if len(path) == 6 and path[0] == 'C':
#             print(path)

def mutate(path, graph):
    # Мутация увеличением или уменьшением длины пути
    action = random.choice(['increase', 'decrease', 'swap', 'reshuffle'])

    max_path_length = len(graph) + 2  # Максимальная длина пути

    if action == 'increase' and len(path) < max_path_length:  # Увеличиваем путь, если не достигли максимальной длины
        new_node = random.choice(list(graph.keys()))  # Случайная вершина
        path.append(new_node)
        print(f"Добавлена вершина {new_node}. Новый путь: {path}")
    
    elif action == 'decrease' and len(path) > len(graph):  # Уменьшаем путь, если он достаточно длинный
        path.pop()  # Удаляем последнюю вершину
        print(f"Удалена последняя вершина. Новый путь: {path}")
    
    elif action == 'swap':  # Меняем местами две случайные вершины
        if len(path) > 1:  # Нужно хотя бы 2 вершины для обмена
            i = random.randint(0, len(path) - 1)
            j = random.randint(0, len(path) - 1)
            path[i], path[j] = path[j], path[i]
            print(f"Обменены вершины {path[i]} и {path[j]}. Новый путь: {path}")
    
    elif action == 'reshuffle':  # Перемешиваем путь
        random.shuffle(path)
        print(f"Все перемешано. Новый путь: {path}")

    if len(path) > max_path_length:
        random.shuffle(path)
        path = path[:max_path_length]

        print(f"Длина пути больше максимальной. Обрезан путь до {max_path_length} вершин: {path}")
    
    if len(path) == 6 and path[0] == 'C':
        print(f"Особый путь: {path}")
    return path
# Генетический алгоритм
def genetic_algorithm(graph, start_node, population_size=100, generations=10000):
    edges = [(u, v) for u in graph for v in graph[u]]
    population = initialize_population(population_size, start_node, graph, edges)

    for generation in range(generations):
        # Оценка приспособленности
        population = sorted(population, key=lambda path: fitness(path, edges), reverse=True)
        best_fitness = fitness(population[0], edges)
        
        if best_fitness == len(edges) and (is_eulerian_path_in_graph(graph,  population[0])):  # Если покрыты все рёбра
            return population[0]
        # Отбор лучших особей
        next_generation = population[:population_size // 2]
        # Кроссовер и мутация
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(next_generation, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.6:  # Мутация с вероятностью 30%
                mutate(child, graph)
            next_generation.append(child)
        population = next_generation
    return None  # Если путь не найден

# Обычный алгоритм для нахождения эйлерова пути
def find_eulerian_path(graph):
    """
    Находит эйлеров путь или цикл в ориентированном графе.
    :param graph: Словарь, где ключ — вершина, значение — список исходящих вершин.
    :return: Список вершин в порядке обхода, либо None, если путь/цикл невозможен.
    """
    # Создаем копию графа, чтобы не изменять исходный
    graph = {node: edges[:] for node, edges in graph.items()}
    
    # Проверка на наличие эйлерова пути или цикла
    in_degrees = {node: 0 for node in graph}
    out_degrees = {node: len(edges) for node, edges in graph.items()}
    
    for node, edges in graph.items():
        for neighbor in edges:
            in_degrees[neighbor] = in_degrees.get(neighbor, 0) + 1

    start_node = None
    end_node = None
    
    for node in graph:
        out_degree = out_degrees[node]
        in_degree = in_degrees[node]
        if out_degree - in_degree == 1:
            if start_node is not None:  # Нельзя иметь больше одной вершины с превышением
                return None
            start_node = node
        elif in_degree - out_degree == 1:
            if end_node is not None:  # Нельзя иметь больше одной вершины с недостатком
                return None
            end_node = node
        elif in_degree != out_degree:
            return None

    # Если нет явного начала, выбираем произвольную вершину с ненулевой степенью
    if start_node is None:
        start_node = next((node for node in graph if out_degrees[node] > 0), None)
    
    # Алгоритм Хиєроніма
    stack = [start_node]
    path = []
    while stack:
        current = stack[-1]
        if out_degrees[current] > 0:
            next_node = graph[current].pop()
            out_degrees[current] -= 1
            stack.append(next_node)
        else:
            path.append(stack.pop())

    # Проверяем, что все рёбра были использованы
    if any(out_degrees[node] > 0 for node in graph):
        return None

    return path[::-1]  # Возвращаем путь в правильном порядке

def is_eulerian_path_in_graph(graph, path):
    """
    Проверяет, является ли переданный путь эйлеровым обходом в ориентированном графе.
    
    graph - это словарь, где ключи - вершины, а значения - список соседей (рёбер).
    path - список, представляющий путь в графе (порядок вершин).
    """
    
    # Проверяем, что путь не пустой и состоит из как минимум двух вершин
    if not path or len(path) < 2:
        return False
    
    used_edges = set()  # Множество для отслеживания использованных рёбер
    graph_copy = {k: list(v) for k, v in graph.items()}  # Копия графа для безопасного удаления рёбер
    
    # Проходим по пути и проверяем, что все рёбра правильно используются
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        
        # Проверяем, что существует ребро от start к end
        if end not in graph_copy.get(start, []):
            # print(f"Ошибка: нет рёбра {start} -> {end}")
            return False
        
        edge = (start, end)
        if edge in used_edges:
            # print(f"Ошибка: ребро {start} -> {end} уже использовано")
            return False
        
        used_edges.add(edge)
        graph_copy[start].remove(end)  # Убираем использованное ребро
    
    # Проверяем, что все рёбра из графа использованы
    for node, neighbors in graph_copy.items():
        if neighbors:
            # print(f"Ошибка: не все рёбра использованы для вершины {node}")
            return False
    
    # Проверка степеней входа и исхода для ориентированного графа
    in_degrees = defaultdict(int)
    out_degrees = defaultdict(int)
    
    for start, neighbors in graph_copy.items():
        for end in neighbors:
            out_degrees[start] += 1
            in_degrees[end] += 1
    
    start_nodes = 0
    end_nodes = 0
    
    for node in set(list(in_degrees.keys()) + list(out_degrees.keys())):
        in_deg = in_degrees[node]
        out_deg = out_degrees[node]
        
        if in_deg == out_deg:
            continue
        elif in_deg + 1 == out_deg:
            start_nodes += 1
        elif out_deg + 1 == in_deg:
            end_nodes += 1
        else:
            print(f"Ошибка: Неверные степени для вершины {node}")
            return False
    
    return start_nodes <= 1 and end_nodes <= 1
