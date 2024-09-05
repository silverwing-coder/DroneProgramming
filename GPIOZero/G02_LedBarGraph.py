from gpiozero import LEDBarGraph
from time import sleep
from signal import pause

graph = LEDBarGraph(5, 6, 13, 19, 26)
while True:
    graph.value = 1
    sleep(1)
    graph.value = 1/2
    sleep(1)
    graph.value = -1/2
    sleep(1)
    graph.value = -1/4
    sleep(1)
    graph.value = -1
    sleep(1)