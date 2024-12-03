import random
from pprint import pprint

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
    cut1 = random.randint(1, len(parent1) - 2)
    cut2 = random.randint(1, len(parent2) - 2)
    child = parent1[:cut1] + parent2[cut2:]
    return child

# Мутация
def mutate(path):
    if len(path) > 2:
        i = random.randint(0, len(path) - 2)
        j = random.randint(0, len(path) - 2)
        path[i], path[j] = path[j], path[i]

# Генетический алгоритм
def genetic_algorithm(graph, start_node, population_size=50, generations=100):
    edges = [(u, v) for u in graph for v in graph[u]]
    pprint(edges)
    population = initialize_population(population_size, start_node, graph, edges)
    for generation in range(generations):
        # Оценка приспособленности
        population = sorted(population, key=lambda path: fitness(path, edges), reverse=True)
        best_fitness = fitness(population[0], edges)
        if best_fitness == len(edges):  # Если покрыты все рёбра
            return population[0]
        # Отбор лучших особей
        next_generation = population[:population_size // 2]
        # Кроссовер и мутация
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(next_generation, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.3:  # Мутация с вероятностью 30%
                mutate(child)
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
