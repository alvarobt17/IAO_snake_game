import os
import matplotlib.pyplot as plt

GENERATIONS_DIR = "generationLogs/"
GENERATION_FILE = GENERATIONS_DIR + "gen"

def showGenerationsGraph():
    """Function to show the distribution of the generations fitness"""
    generations = []
    fitness = []
    # Sort the files by generation
    files = sorted(os.listdir(GENERATIONS_DIR), key=lambda x: int(x[3:-4]))
    for file in files:
        with open(GENERATIONS_DIR + file, "r") as f:
            fitness_value = float(f.readline().split(": ")[1])
            generation = int(file[3:-4])
            
            fitness.append(fitness_value)
            generations.append(generation)

    plt.plot(generations, fitness)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.show()

def showPopulationGraph(generation):
    """Function to show the distribution of the population fitness"""
    fitness = []
    
    try:
        with open(GENERATION_FILE + str(generation) + ".txt", "r") as f:
            for line in f.readlines():
                if "Player" in line:
                    fitness_value = float(line.split(": ")[1])
                    fitness.append(fitness_value)
    except FileNotFoundError:
        print("\nGeneration file not found")
        return

    plt.hist(fitness, bins=20)
    plt.xlabel("Fitness")
    plt.ylabel("Number of players")
    plt.show()


if __name__ == "__main__":
    print("Select an option:")
    print("1. Show generations graph")
    print("2. Show population graph")
    option = input("\nOption: ")

    if option == "1":
        showGenerationsGraph()
    elif option == "2":
        generation = int(input("Insert the generation number: "))
        showPopulationGraph(generation)
    else:
        print("Invalid option")
