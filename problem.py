

# ===================================================================
#                           IMPORTS
# ===================================================================

import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as pltRectangle


# ===================================================================
#                           Vector2
# ===================================================================

class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def copy(self, other):
        self.x = other.x
        self.y = other.y
        return self
    
    def clone(self):
        return Vector2(self.x, self.y)
    
    def set(self, x, y):
        self.x = x
        self.y = y
        return self
    
    def __add__(self, u):
        self.x += u.x
        self.y += u.y
        return self
    
    def __sub__(self, u):
        self.x -= u.x
        self.y -= u.y
        return self
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    

# ===================================================================
#                           Piece
# ===================================================================

class Piece:

    def __init__(self, position: Vector2, width: int, height: int, isStanding: bool = True) -> None:
        self.position = position
        self.width = width
        self.height = height
        self.isStanding = isStanding
        self.id = None

    def copy(self, other):
        self.position.copy(other.position)
        self.width = other.width
        self.height = other.height
        self.isStanding = other.isStanding
        self.id = other.id
        return self
    
    def clone(self):
        return Piece(self.position, self.width, self.height, self.isStanding).setId(self.id)

    def setId(self, id: int):
        self.id = id
        return self

    def flip(self):
        self.isStanding = not self.isStanding
        return self
    
    def getPosition(self) -> Vector2:
        return self.position
    
    def setPosition(self, position: Vector2):
        self.position = position
        return self
    
    def getStandingSize(self) -> Vector2:
        return Vector2(self.width, self.height)
    
    def getSize(self) -> Vector2:
        """
        Return size relative to orientation
        """
        if self.isStanding:
            return self.getStandingSize()
        
        return Vector2(self.height, self.width)
    
    def getPlacement(self) -> tuple[Vector2, Vector2]:

        start = self.position
        end = start.clone() + self.getSize()

        return start, end
    
    def getArea(self) -> int:
        return self.width * self.height
    
    def isOverlapWith(self, other) -> bool:
        """
        TODO Actuellement, la vérification de superposition (isOverlapWith) dans checkConfiguration utilise une approche de force brute.
        Pour des configurations avec un grand nombre de pièces, cela pourrait devenir inefficace.
        Envisagez d'utiliser des structures de données spatiales, comme les arbres de quadrants ou les grilles de hachage spatial,
        pour réduire le nombre de vérifications nécessaires.
        """
        selfStart, selfEnd = self.getPlacement()
        otherStart, otherEnd = other.getPlacement()

        if selfEnd.x <= otherStart.x or selfStart.x >= otherEnd.x:
            return False
        
        if selfEnd.y <= otherStart.y or selfStart.y >= otherEnd.y:
            return False
            
        return True
    
    def plot(self, ax = None) -> None:

        if ax == None:
            print("Warning: Piece has not been plotted.")
            return
        
        size = self.getSize()
        width, height = size.x, size.y
        
        rect = pltRectangle((self.position.x, self.position.y), width, height, fill=True, facecolor='#ff4d4d', alpha = 0.5, edgecolor = "black")
        ax.add_patch(rect)

        rx, ry = rect.get_xy()
        cx = rx + rect.get_width()/2.0
        cy = ry + rect.get_height()/2.0

        ax.annotate(f"{self.id}", (cx, cy), color='black', weight='bold', fontsize=10, ha='center', va='center')
    
    def __repr__(self) -> str:
        return f"Piece( position: {self.position}, width: {self.width}, height: {self.height})"


# ===================================================================
#                           Config
# ===================================================================



class Config:

    def __init__(self, *pieces: Piece) -> None:
        self.pieces = list(pieces)

    def copy(self, other):
        self.pieces = []
        for piece in other.pieces:
            self.pieces.append(piece.clone())
        return self
    
    def clone(self):
        array = []
        for piece in self.pieces:
            array.append(piece.clone())
        return Config(*array)

    def add(self, piece: Piece):
        self.pieces.append(piece)
        return self

    def remove(self, index: int):
        self.pieces.pop(index)
        return self
    
    def length(self) -> int:
        return len(self.pieces)
    
    def findIndexFrom(self, piece):

        length = self.length()
        for index in range(length):
            if self[index].id == piece.id:
                return index
        return -1
    
    def isOverlap(self, piece: Piece) -> bool:
        """Vérifie si la pièce se superpose à une autre dans la configuration."""
        for placedPiece in self.pieces:
            if placedPiece.isOverlapWith(piece):
                return True
        return False
    
    def plot(self, ax = None):

        if ax == None:
            print("Warning: Config has not been plotted.")
            return

        pieces = self.pieces

        for piece in pieces:
            piece.plot(ax)
    
    def __getitem__(self, index):
        return self.pieces[index]

    def __repr__(self) -> str:
        return f"Config( pieces: {self.pieces} )"

    

# ===================================================================
#                           Grid
# ===================================================================


class Grid:

    def __init__(self, position: Vector2, width: int, height: int) -> None:
        self.position = position
        self.width = width
        self.height = height

    def getPlot(self):

        fig, ax = plt.subplots()

        gridrect = pltRectangle((self.position.x, self.position.y), self.width, self.height, fill=True, facecolor='#e0e0f0', edgecolor = "black")
        ax.add_patch(gridrect)

        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.axis('equal')

        return fig, ax

    def contains(self, piece: Piece) -> bool:
        """
        TODO : Dans la méthode contains de la classe Grid, vous utilisez start.x >= 0 et start.y >= 0 pour la validation.
        C'est efficace si la grille commence à (0, 0).
        Assurez-vous que cela correspond à vos besoins ou ajustez selon la position initiale de la grille.
        """
        start, end = piece.getPlacement()
        return start.x >= 0 and start.y >= 0 and end.x <= self.width and end.y <= self.height
        
    def checkConfiguration(self, config: Config) -> bool:
        # grid check
        for piece in config.pieces:
            if not self.contains(piece):
                return False

        # overlapping check
        length = config.length()
        for i in range(length):
            for j in range(i + 1, length):
                if config.pieces[i].isOverlapWith(config.pieces[j]):
                    return False

        # all checked
        return True
    
    def isValidPosition(self, position: Vector2, piece: Piece, config: Config) -> bool:
        
        tempPiece = piece.clone().setPosition(position)
        
        if not self.contains(tempPiece):
            return False
        
        return not config.isOverlap(tempPiece)

    def __repr__(self) -> str:
        return f"Grid( position: {self.position}, width: {self.width}, height: {self.height})"
    

# ===================================================================
#                           Problem
# ===================================================================

class Problem:

    def __init__(self, grid: Grid, pieces: list[Piece]) -> None:
        self.grid = grid
        self.pieces = pieces

    def show(self, config):
        fig, ax = self.grid.getPlot()

        isvalid = self.grid.checkConfiguration(config)
        print(f"Is configuration valid ?: {isvalid}")
        print(f"Score: {self.getEmptyArea(config)}")

        config.plot(ax)

        plt.show()

    def getMissingIndexes(self, config: Config) -> list[int]:
        # Initialize a list of indices representing all pieces
        indexes = list(range(len(self.pieces)))

        for config_piece in config.pieces:
            # Attempt to find the piece's index in the original list using its id
            for i, piece in enumerate(self.pieces):
                if piece.id == config_piece.id:
                    # If found, remove this index from the list of missing indexes
                    if i in indexes:
                        indexes.remove(i)

        return indexes
    
    def getEmptyArea(self, config: Config) -> int:

        emptyArea = self.grid.width * self.grid.height
        for piece in config.pieces:
            emptyArea -= piece.getArea()
        return emptyArea
    
    def getNotPlacedPieces(self, config: Config) -> list[Piece]:

        indexes = self.getMissingIndexes(config)
        return [self.pieces[index].clone() for index in indexes]
    
    def chooseRandomPiece(self, config: Config) -> Piece:

        notPlacedPieces = self.getNotPlacedPieces(config)
        piece = rd.choice(notPlacedPieces).clone()

        if Problem.randomBoolean():
            piece.flip()
        
        return piece
    
    def findPossiblePositions(self, config: Config, piece: Piece) -> list[Vector2]:
        positions = []
        
        for placedPiece in config.pieces:
            # get edges from placed pieces
            placedPos, placedSize = placedPiece.getPosition(), placedPiece.getSize()
            
            # adjacent position from placed pieces
            adjacentPositions = [
                Vector2(placedPos.x + placedSize.x, placedPos.y),  # Droite
                Vector2(placedPos.x - piece.getSize().x, placedPos.y),  # Gauche
                Vector2(placedPos.x, placedPos.y + placedSize.y),  # Haut
                Vector2(placedPos.x, placedPos.y - piece.getSize().y)   # Bas
            ]
            
            for pos in adjacentPositions:
                if self.grid.isValidPosition(pos, piece, config):
                    positions.append(pos)
        
        return positions
    
    
    def constructiveDynamic(self, config: Config) -> bool:

        length = config.length()
        max_length = len(self.pieces)

        if length == 0:
            piece = self.chooseRandomPiece(config)
            config.add(piece)
            return True

        if length == max_length:
            return False
        
        piece = self.chooseRandomPiece(config)
        possiblePositions = self.findPossiblePositions(config, piece)

        # Tri des vecteurs par ordre décroissant de leur abscisse, puis par ordre croissant de leur ordonnée en cas d'égalité
        sortedPositions = sorted(possiblePositions, key=lambda v: (v.x, v.y))
        
        if len(sortedPositions) > 0 :
            piece.setPosition(sortedPositions[0])
            config.add(piece)
            return True

        return False
    
    def destructiveDynamic(self, config: Config) -> bool:
        length = config.length()
        if length > 0:
            index = Problem.randomInteger(0, length)
            config.remove(index)
            return True
        return False
    
    def dynamic(self, config: Config, probability: float = 0.95) -> bool:
        sample = rd.uniform(0, 1)
        if sample < probability:
            return self.constructiveDynamic(config)
        return self.destructiveDynamic(config)

    def randomConfig(self) -> Config:

        config = Config()
        isPlaced = True
        while isPlaced:
            isPlaced = self.constructiveDynamic(config)
        return config
    
    # ------------------------------------
    @classmethod
    def randomInteger(cls, low: int, high: int) -> int:
        return int(np.random.uniform(0, 1) * (high - low) + low)
    
    @classmethod
    def randomBoolean(cls) -> bool:
        return np.random.choice([True, False])

    def randomPosition(self) -> Vector2:
        
        x_start = self.grid.position.x
        x_end = self.grid.position.x + self.grid.width

        y_start = self.grid.position.y
        y_end = self.grid.position.y + self.grid.height

        x = Problem.randomInteger(x_start, x_end)
        y = Problem.randomInteger(y_start, y_end)

        return Vector2(x, y)
    
    # ------------------------------------

    def metropolis(self, probability: float, temperature: float, itermax: int = 100) -> tuple[Config, int]:

        bestScore = None

        lastConfig = Config()

        # keep the best config. This config does not interfere with Metropolis.
        bestConfig = lastConfig.clone()
        
        for i in range(itermax):

            config = lastConfig.clone()
            
            self.dynamic(config, probability)

            jConfig = self.getEmptyArea(config)
            jLastConfig = self.getEmptyArea(lastConfig)
            
            u = np.random.uniform(0, 1)
            metropolisCriteria = u < np.exp(-(jConfig - jLastConfig) / temperature)

            if jConfig < jLastConfig or metropolisCriteria:
                lastConfig = config.clone()

            # Does not interfere with Metropolis.
            if jConfig < self.getEmptyArea(bestConfig):
                bestConfig = config.clone()
                bestScore = self.getEmptyArea(config)
                #print(f"New Best Score : J(config)={bestScore}, step:{i}/{itermax}")

        return (bestConfig, bestScore)
    
    # ------------------------------------

    def __repr__(self) -> str:
        return f"Problem( grid: {self.grid}, pieces: {self.pieces})"
