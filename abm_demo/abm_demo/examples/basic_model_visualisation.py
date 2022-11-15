import mesa

from argparse import ArgumentParser

from basic_model import *

def create_argparser():

    parser = ArgumentParser()

    parser.add_argument('--N', help="Number of agents", default=20, type=int)
    parser.add_argument('--width', default=10, type=int)
    parser.add_argument('--height', default=10, type=int)
    parser.add_argument('--init_wealth', default=1, type=int)

    return parser

if __name__ == '__main__':
    
    parser = create_argparser()
    args = parser.parse_args()

    def agent_portrayal(agent):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "red",
                     "r": 0.5}
        return portrayal

    grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    mean_wealth_chart = mesa.visualization.ChartModule(
        [{"Label": "Mean Wealth", "Color": "#0000FF"}], data_collector_name="datacollector"
    )

    server = mesa.visualization.ModularServer(
        BasicModel, [grid, mean_wealth_chart],
        "Basic wealth model", {"N": args.N, "width": args.width, "height": args.height, "init_wealth": args.init_wealth}
    )
    server.port = 8521 # The default
    server.launch()