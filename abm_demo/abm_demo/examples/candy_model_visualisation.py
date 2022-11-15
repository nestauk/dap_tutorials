import mesa

from argparse import ArgumentParser

from candy_model import *

def create_argparser():

    parser = ArgumentParser()

    parser.add_argument('--N', help="Number of agents", default=20, type=int)
    parser.add_argument('--width', default=10, type=int)
    parser.add_argument('--height', default=10, type=int)
    parser.add_argument('--init_candy', default=1, type=int)
    parser.add_argument('--init_sharer_prop', default=0.9, type=float)
    parser.add_argument('--mutation_rate', default=0.01, type=float)

    return parser

if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()

    def agent_portrayal(agent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "red",
                     "r": 0.1+(agent.wealth/args.N)}
        if agent.wealth > 0:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 1
        return portrayal


    grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    gini_chart = mesa.visualization.ChartModule(
        [{"Label": "Gini", "Color": "#0000FF"}], data_collector_name="datacollector"
    )
    prop_self_chart = mesa.visualization.ChartModule(
        [{"Label": "proportion_sharers", "Color": "#0000FF"}], data_collector_name="datacollector"
    )

    server = mesa.visualization.ModularServer(
        CandyModel,
        [grid, gini_chart, prop_self_chart],
        "Candy exchange model",
        {
        "N": args.N,
        "width": args.width,
        "height": args.height,
        "init_candy": args.init_candy,
        "init_sharer_prop": args.init_sharer_prop,
        "mutation_rate": args.mutation_rate,
        }
    )
    server.port = 8521 # The default
    server.launch()
