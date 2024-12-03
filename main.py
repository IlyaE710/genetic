# main.py
from algorithms import find_eulerian_path, genetic_algorithm
from pprint import pprint

def main():
    graphs = [
        {'A': ['B'], 'B': ['C', 'D'], 'C': ['D'], 'D': ['A']},
        {'A': ['B', 'C'], 'B': ['C'], 'C': ['A'], 'D': ['E'], 'E': ['D']},
        {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['D'], 'D': ['A', 'C']},
        {'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']},
        {'A': ['B'], 'B': ['C'], 'C': ['A']},
        {'A': ['B'], 'B': ['C'], 'C': ['A', 'D'], 'D': ['B']}
    ]
    

    for graph in graphs:
        # Обычный алгоритм
        pprint(graph)
        result = find_eulerian_path(graph)
        print("Обычный алгоритм:")
        if result:
            print("Эйлеров путь или цикл найден:", " -> ".join(result))
        else:
            print("Эйлеров путь или цикл невозможен.")

        # Использование генетического алгоритма
        start_node = 'B'  # Начальная вершина
        result = genetic_algorithm(graph, start_node)
        print("Генетический алгоритм:")
        if result:
            print("Эйлеров путь найден:", " -> ".join(result))
        else:
            print("Эйлеров путь не найден")

if __name__ == "__main__":
    main()
