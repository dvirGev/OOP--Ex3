import pygame
from pygame import math
from pygame.constants import RESIZABLE
from DiGraph import DiGraph
#from GraphAlgo import GraphAlgo
from GraphAlgoInterface import GraphAlgoInterface


class GUI():
    def __init__(self, graphAlgo: GraphAlgoInterface) -> None:
        self.graphAlgo = graphAlgo
        self.minX = self.minY = float('inf')
        self.maxX = self.maxY = float('-inf')
        self.findMaxAndMin()
        self.unitX = 0
        self.unitY = 0
        pygame.init()
        pygame.font.init()

        self.backgroundColor = (34, 189, 173)
        self.nodeColor = (227, 77, 148)
        self.GAME_FONT = pygame.font.SysFont('comicsans', 15)
        self.screen = pygame.display.set_mode(
            [1000, 750], RESIZABLE)  # Set up the drawing window
        self.run()

    def run(self):
        # Run until the user asks to quit
        running = True
        while running:
            self.unitX = (self.screen.get_width() /
                          abs(self.maxX - self.minX) * 0.95)
            self.unitY = (self.screen.get_height() /
                          abs(self.maxY - self.minY) * 0.9)
            # Fill the background with white
            self.screen.fill(self.backgroundColor)
            # Did the user click the window close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw a solid blue circle in the center
            self.drawEdges()
            self.drawNodes()
            # Flip the display
            pygame.display.flip()
        # Done! Time to quit.
        pygame.quit()

    def drawNodes(self):
        for node in self.graphAlgo.graph.nodes.values():
            x = (node.location[0] - self.minX) * self.unitX + 25
            y = (node.location[1] - self.minY) * self.unitY + 25

            pygame.draw.circle(self.screen, self.nodeColor, (x, y), 20)
            # You can use `render` and then blit the text surface ...
            text_surface = self.GAME_FONT.render(
                str(node.key), 15, (255, 255, 255))
            self.screen.blit(text_surface, (x, y-10))

    def findMaxAndMin(self):
        for node in self.graphAlgo.graph.nodes.values():
            x = node.location[0]
            y = node.location[1]

            if(self.minX > x):
                self.minX = x
            elif(self.maxX < x):
                self.maxX = x
            if(self.minY > y):
                self.minY = y
            elif(self.maxY < y):
                self.maxY = y

    def drawEdges(self):
        allEdges = self.graphAlgo.graph.edges
        for edge in allEdges.keys():
            srcX = self.graphAlgo.graph.nodes[edge[0]].location[0]
            srcX = (srcX - self.minX) * self.unitX + 25
            srcY = self.graphAlgo.graph.nodes[edge[0]].location[1]
            srcY = (srcY - self.minY) * self.unitY + 25

            destX = self.graphAlgo.graph.nodes[edge[1]].location[0]
            destX = (destX - self.minX) * self.unitX + 25
            destY = self.graphAlgo.graph.nodes[edge[1]].location[1]
            destY = (destY - self.minY) * self.unitY + 25

            # pygame.draw.line(self.screen, (0, 0, 0),(srcX, srcY), (destX, destY), 3)
            self.arrow(self.screen, (0,0,0), (srcX, srcY), (destX, destY), 3)

    def arrow(screen, lcolor, tricolor, start, end, trirad, thickness=2):
        pygame.draw.line(screen, lcolor, start, end, thickness)
        rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi/2
        pygame.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation), end[1] + trirad * math.cos(rotation)), (end[0] + trirad * math.sin(rotation - 120*rad),end[1] + trirad * math.cos(rotation - 120*rad)), (end[0] + trirad * math.sin(rotation + 120*rad),end[1] + trirad * math.cos(rotation + 120*rad))))


if __name__ == '__main__':
    graphAlgo = GraphAlgo()
    graphAlgo.load_from_json("./data/A0.json")
    gui = GUI(graphAlgo)
