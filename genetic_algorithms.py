from collections import defaultdict
import random

def fitness(graph, path):
    """
    Оценка качества пути. Чем выше число используемых рёбер, тем лучше.
    """
    used_edges = set()
    graph_copy = {k: list(v) for k, v in graph.items()}
    score = 0

    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        
        if end in graph_copy.get(start, []):
            score += 1  # Увеличиваем балл, если ребро используется
            used_edges.add((start, end))
            graph_copy[start].remove(end)
    
    # Оценка качества пути на основе использованных рёбер
    return score / len(graph)  # Процент использованных рёбер

def crossover(path1, path2):
    """
    Пересечение двух путей для создания нового пути.
    """
    crossover_point = random.randint(1, len(path1) - 1)
    new_path = path1[:crossover_point] + path2[crossover_point:]
    return new_path

def mutate(path, graph):
    """
    Мутация: случайная замена вершины на другом месте в пути.
    """
    mutation_point = random.randint(0, len(path) - 1)
    new_node = random.choice(list(graph.keys()))
    path[mutation_point] = new_node
    return path

def generate_random_eulerian_path(graph):
    """
    Генерация случайного эйлерова пути, который может быть разной длины в зависимости от графа.
    Путь будет продолжаться, пока не будет использовано все возможные рёбра.
    """
    # Получаем все рёбра графа
    edges = []
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            edges.append((node, neighbor))

    # Если в графе нет рёбер, возвращаем пустой путь
    if not edges:
        return []

    # Случайная генерация пути
    path = []
    used_edges = set()  # Множество для отслеживания использованных рёбер
    
    # Начинаем с случайной вершины
    current_node = random.choice(list(graph.keys()))
    path.append(current_node)
    
    while len(used_edges) < len(edges):  # Пока не использованы все рёбра
        neighbors = graph.get(current_node, [])
        
        # Если у вершины нет доступных соседей, завершаем путь
        if not neighbors:
            break
        
        # Выбираем случайного соседа
        next_node = random.choice(neighbors)
        
        # Проверяем, что рёбро не было использовано
        while (current_node, next_node) in used_edges:
            next_node = random.choice(neighbors)  # Ищем новый соседний узел
        
        # Добавляем рёбро в использованные
        used_edges.add((current_node, next_node))
        
        # Добавляем вершину в путь
        path.append(next_node)
        
        # Переходим к следующей вершине
        current_node = next_node
    print(path)
    return path

def genetic_algorithm(graph, population_size=100, generations=10000):
    """
    Генетический алгоритм для поиска эйлерова пути в графе.
    """
    population = []
    for _ in range(population_size):
        path = generate_random_eulerian_path(graph)
        print(path)
        population.append(path)

    for generation in range(generations):
        population.sort(key=lambda path: fitness(graph, path), reverse=True)
        if fitness(graph, population[0]) == 1.0:  # Если все рёбра использованы
            print(f"Эйлеров путь найден на поколении {generation + 1}: {population[0]}")
            return population[0]
        
        new_population = population[:population_size // 2]
        
        while len(new_population) < population_size:
            parent1 = random.choice(new_population)
            parent2 = random.choice(new_population)
            child = crossover(parent1, parent2)
            if random.random() < 0.3:
                child = mutate(child, graph)
            new_population.append(child)
        
        population = new_population
    
    print("Эйлеров путь не найден.")
    return None

# Пример использования
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['C', 'A'],
        'C': ['A', 'B']
    }

    solution = genetic_algorithm(graph)
    if solution:
        print(f"Эйлеров путь найден: {solution}")
    else:
        print("Эйлеров путь не найден.")
