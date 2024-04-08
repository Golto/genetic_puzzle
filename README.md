# Informarions
- Author: Golto
- Date: 09/04/2024 [dd/mm/yyyy]
- Contribution: Thanks to Jaden VICAINE and Emma SARCHER for helping me with the constructive dynamic in `Problem.py`

# Genetic Algorithm for Puzzle Solving
### Introduction
This repository contains a Python implementation of a genetic algorithm designed to solve a puzzle problem. The puzzle involves fitting a set of pieces into a grid, with the aim to minimize the empty space — effectively maximizing the configuration's fitness.

### Problem Definition
The puzzle consists of a grid with dimensions 40x50 units and a set of 9 unique pieces, each with its own size and identifier. The goal is to place all pieces within the grid in an optimal arrangement with no overlaps and the least possible unused space.

### Genetic Algorithm Overview
The genetic algorithm approaches this problem by simulating a process of evolution. It maintains a population of configurations (Config) where each individual represents a potential solution. The fitness of each individual is inversely related to the amount of empty space when the pieces are placed on the grid. Higher fitness values correspond to better solutions.

The algorithm proceeds through a series of generations, each time performing selection, crossover, and mutation to produce new offspring configurations. Over time, the population evolves towards better solutions.

### Key Components
- Population: A group of potential solutions (configurations of pieces on the grid).
- Fitness: A measure of how well a configuration fills the grid, with less empty space correlating to higher fitness.
- Selection: A process to choose configurations for breeding based on their fitness.
- Crossover: A mechanism to combine two configurations, inheriting features from both to produce a new configuration.
- Mutation: Random changes introduced to configurations to maintain diversity and explore new solutions.

### Usage
A Jupyter notebook is provided for you to interact with and test the genetic algorithm. It's an excellent way to visualize the process and tweak parameters to see how they influence the outcome.

Using the Notebook
- Setup: Initialize the problem with the grid and pieces.
- Instantiate the Algorithm: Create a Genetic object with the desired parameters.
- Run: Execute the run method to start the evolution process.
- Observe: Monitor the output for each generation's best fitness.
- Visualize: Use the provided visualization tools to see the configuration of pieces on the grid.
