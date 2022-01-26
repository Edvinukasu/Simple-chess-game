import pygame

WIDTH = HEIGHT = 560
DIMENSION = 8
Square_Size = WIDTH // DIMENSION
MAX_FPS = 20
images = {}


# Game_state will hold the information about the starting board, which team has to play a move, move log and
# starting board)

class game_state():
    def __init__(self):
        # board is a 8x8 array. Each element is 2 characters long, first one for team and second one
        # for type (b/w R/N/B/Q/K/P
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteTurn = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.Start_Row][move.Start_Collum] = "--"
        self.board[move.End_Row][move.End_Collum] = move.Piece_Moved
        self.moveLog.append(move)  # Adds move the log so we can track it for undoing and for replays
        self.whiteTurn = not self.whiteTurn  # Swaps player turns


class move():
    # Dictionary maps game state board variable array to Chess notation
    Ranks_to_Rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    Rows_to_Ranks = {v: k for k, v in Ranks_to_Rows.items()}  # Reverses all the keys and values for each item in the
    # dictionary
    Files_to_Columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 0}
    Columns_to_Files = {v: k for k, v in Files_to_Columns.items()}

    def __init__(self, Start_Square, End_Square, board):
        self.Start_Row = Start_Square[0]
        self.Start_Collum = Start_Square[1]
        self.End_Row = End_Square[0]
        self.End_Collum = End_Square[1]
        self.Piece_Moved = board[self.Start_Row][self.Start_Collum]
        self.Piece_Captured = board[self.End_Row][self.End_Collum]

    def getChessNotation(self):
        return self.getRankFile(self.Start_Row, self.Start_Collum) + self.getRankFile(self.End_Row, self.End_Collum)

    def getRankFile(self, row, collum):
        return self.Columns_to_Files[collum] + self.Rows_to_Ranks[row]


def main():
    pygame.init()  # Initialises the display module and sets up the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SchChess")
    clock = pygame.time.Clock()
    gs = game_state()
    loadImages()  # Loads all the needed chess pieces once before the while loop
    Square_Selected = ()  # Variable to hold the last square selected, row and collum
    Player_Clicks = []  # Keeps track of player clicks
    running = True
    while running:  # Event while loop
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # A way to close the game
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Sets event for mouse button down
                location = pygame.mouse.get_pos()  # Assigns X, Y location of mouse to variable
                collum = location[0] // Square_Size
                row = location[1] // Square_Size
                if Square_Selected == (row, collum):  # Checks whether player selected the same square
                    Square_Selected = ()  # Clears selected square
                    Player_Clicks = []  # Clears player clicks
                else:
                    Square_Selected = (row, collum)
                    Player_Clicks.append(Square_Selected)  # Appends the first and second mouse clicks
                if len(Player_Clicks) == 2:  # After second click
                    makeMove = move(Player_Clicks[0], Player_Clicks[1], gs.board)
                    gs.makeMove(makeMove)  # Calls upon game_state class to make the move on the 2D array.
                    Square_Selected = ()  # Clears selected square
                    Player_Clicks = []  # Clears player clicks


def loadImages():  # Method to load all images, will only be used once since its an expensive process
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for p in pieces:
        images[p] = pygame.transform.scale(pygame.image.load("images/" + p + ".png"), (Square_Size, Square_Size))
    # Accessing images using images['bR']


def drawGameState(screen, gs):
    drawBoard(screen, gs.board)  # Used the draw the Game state on the board, and the pieces


def drawBoard(screen, board):
    colours = [pygame.Color("White"), pygame.Color(112, 128, 144)]
    for row in range(DIMENSION):
        for collum in range(DIMENSION):
            colour = colours[((row + collum) % 2)]
            pygame.draw.rect(screen, colour,
                             pygame.Rect(collum * Square_Size, row * Square_Size, Square_Size, Square_Size))
            piece = board[row][collum]
            if piece != "--":
                screen.blit(images[piece],
                            pygame.Rect(collum * Square_Size, row * Square_Size, Square_Size, Square_Size))


main()
