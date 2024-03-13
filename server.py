from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Schelling


class VisualElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    #def render(self, model):
    #    return "Happy agents: " + str(model.happy)


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 10:
        #portrayal["Shape"] = "rect"
        #portrayal["Color"] = "#706e6e"   #ash
        portrayal["r"] = 0.7   
        #portrayal["Color"] = "#ffdcdcdc"   #peach
        portrayal["Color"] = "#706e6e" #ash
    elif agent.type == 3 or agent.type==4 or agent.type==6 or agent.type==2 or agent.type==5 or agent.type==7:
        portrayal["Color"] = "red" #red
    elif agent.type == 1:
        portrayal["Color"] = "green"
    elif agent.type == 8:
        portrayal["Color"] = "#3b0202"    #brownish red    
    elif agent.type == 9:
        portrayal["Color"] = "#0F0000"   #black
    elif agent.type ==11:
        portrayal["Color"] = "#E3CF57"   #yellow
    else:
        portrayal["Color"] = "blue"
        #portrayal["Color"] = ["#FF0000", "#FF9999"]
        #portrayal["stroke_color"] = "#00FF00"
        
    #if agent.model.resistance_gain > 0:
        
    '''    
    elif agent.type == 1:
        portrayal["Color"] = "green"
    elif agent.type == 2:
        portrayal["Color"] = "#d97373" #peach 
    elif agent.type == 3:
        portrayal["Color"] = "red" #red
    elif agent.type == 4:
        portrayal["Color"] = "red" #red
    elif agent.type == 5:
        portrayal["Color"] = "#d97373" #peach 
    elif agent.type == 6:
        portrayal["Color"] = "red" #red
    elif agent.type == 7:
        portrayal["Color"] = "#d97373" #peach 
    elif agent.type == 8:
        portrayal["Color"] = "#3b0202"    #brownish red    
    elif agent.type == 9:
        portrayal["Color"] = "#0F0000"   #black
        #portrayal["stroke_color"] = "#000000"
    else:
        portrayal["Color"] = "#706e6e"   #ash
    '''
    return portrayal


visual_element = VisualElement()
canvas_element = CanvasGrid(schelling_draw, 100, 100, 500, 500)
visual_chart = ChartModule([{"Label": "resistance_gain", "Color": "Green"},{"Label": "covid_death", "Color": "Black"},{"Label": "infected", "Color": "Red"},{"Label": "susceptible", "Color": "Blue"}])
visual_chart1 = ChartModule([{"Label": "newly_infected", "Color": "Red"}])
model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Agent density", 0.1, 0.1, 1.0, 0.1),
    "initial_outbreak": UserSettableParameter(
        "slider", "Initial outbreak fraction", 0.07, 0.01, 1.0, 0.01),
    "non_accesible_area_density":0.075,
    "social_distancing": UserSettableParameter('checkbox', 'Social Distancing', value=True),
    
    #"homophily": UserSettableParameter("slider", "Homophily", 3, 0, 8, 1),
}

server = ModularServer(
    Schelling, [canvas_element, visual_element, visual_chart,visual_chart1], "Schelling", model_params
)

