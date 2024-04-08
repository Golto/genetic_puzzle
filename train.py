
# ===================================================================
#                           IMPORTS
# ===================================================================

import numpy as np
import problem as pb

# ===================================================================
#                           PROBLEM DEFINITION
# ===================================================================

mainProblem = pb.Problem(
    grid = pb.Grid(pb.Vector2(0, 0), 40, 50),
    pieces = [
        pb.Piece(pb.Vector2(0, 0), 14, 27).setId(1),
        pb.Piece(pb.Vector2(0, 0), 8, 36).setId(2),
        pb.Piece(pb.Vector2(0, 0), 8, 9).setId(3),
        pb.Piece(pb.Vector2(0, 0), 6, 14).setId(4),
        pb.Piece(pb.Vector2(0, 0), 34, 5).setId(5),
        pb.Piece(pb.Vector2(0, 0), 18, 9).setId(6),
        pb.Piece(pb.Vector2(0, 0), 22, 9).setId(7),
        pb.Piece(pb.Vector2(0, 0), 18, 21).setId(8),
        pb.Piece(pb.Vector2(0, 0), 18, 15).setId(9),
    ]
)

# ===================================================================
#                           GENETIC ALGORITHM
# ===================================================================

class Genetic:

    def __init__(self, problem: pb.Problem, population_size: int, generations: int, tournament_size: int, mutation_rate: float = 0.1, dynamic_probability: float = 0.75) -> None:
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.dynamic_rate = dynamic_probability

    def createIndividual(self) -> pb.Config:
        return self.problem.randomConfig()
    
    def createPopulation(self) -> list[pb.Config]:
        return [self.createIndividual() for _ in range(self.population_size)]
    
    def fitness(self, individual: pb.Config) -> float:
        score = self.problem.getEmptyArea(individual)
        return 1 / (score + 1)
    
    def tournamentSelection(self, population: list[pb.Config]) -> pb.Config:
        contenders = np.random.choice(population, self.tournament_size, replace = True)
        contender_fitness = [self.fitness(individual) for individual in contenders]
        winner_index = np.argmax(contender_fitness)
        return contenders[winner_index]
    
    def crossover(self, parent1: pb.Config, parent2: pb.Config) -> pb.Config:
        return parent1.clone() # TODO
    
    def mutate(self, individual: pb.Config) -> pb.Config:
        probability = np.random.uniform(0, 1)
        if probability < self.mutation_rate:
            self.problem.dynamic(individual, self.dynamic_rate)
        return individual
    
    def run(self, isDebug: bool = True) -> tuple[pb.Config, list[float]]:

        population = self.createPopulation()
        
        best_fitness_history = []
        
        for generation in range(self.generations):
            new_population = []
            
            # children for next generation
            for _ in range(self.population_size // 2):
                parent1 = self.tournamentSelection(population)
                parent2 = self.tournamentSelection(population)
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                self.mutate(child1)
                self.mutate(child2)
                new_population.extend([child1, child2])
            
            # fitness of next generation
            new_fitnesses = [self.fitness(individual) for individual in new_population]
            
            population_fitness = sorted(zip(new_population, new_fitnesses), key=lambda x: x[1], reverse=False)
            population = [individual for individual, _ in population_fitness[:self.population_size]]
            
            best_fitness_history.append(population_fitness[0][1])
            
            if isDebug:
                print(f"Génération {generation + 1}: Meilleure fitness = {population_fitness[0][1]}")
        
        best_config = population[0]
        return best_config, best_fitness_history