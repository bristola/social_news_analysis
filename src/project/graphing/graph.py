import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from math import pi

class Graphing:

    def __init__(self):
        pass


    def sentiment_totals_graph(self, data):
        plt.clf()
        plt.plot([1,2,3,4])
        return self.plot_to_base()


    def sentiment_groups_graph(self, data):
        plt.clf()
        plt.plot([4,3,2,1])
        return self.plot_to_base()


    def mood_totals_graph(self, data):

        # Test data
        data = {
            "happiness": 100,
            "anxiety": 73,
            "sadness": 90,
            "affection": 55,
            "aggression": 30,
            "expressive": 70,
            "glory": 39
        }

        plt.clf()

        categories = [mood for mood, amount in data.items()]
        values = [amount for mood, amount in data.items()]
        N = len(values)
        angles = [n / float(N) * 2 * pi for n in range(0, N)]

        ax = plt.subplot(111, projection='polar', clip_on=False)
        bars = ax.bar(angles, values, width=.885, bottom=0.0)

        colors = ["orange","k","b","m","r","g","y"]
        for value, category, angle, bar, color in zip(values, categories, angles, bars, colors):
            bar.set_color(color)
            bar.set_alpha(0.5)
            ax.text(angle, value+10, category, size=15, horizontalalignment="center", verticalalignment="center")

        ax.spines['polar'].set_visible(False)
        ax.get_xaxis().set_visible(False)
        m = max(values)
        ax.set_rlabel_position(0)
        ax.get_yaxis().set_ticks([m,3*m/4,m/2,m/4])

        plt.show()

        return self.plot_to_base()


    def emoticon_totals_graph(self, data):
        plt.clf()
        plt.plot([4,3,2,4])
        return self.plot_to_base()


    def plot_to_base(self):
        t = BytesIO()
        plt.savefig(t)
        encoded = base64.b64encode(t.getvalue())
        encoded_str = str(encoded)
        encoded_str = encoded_str[2:len(encoded_str)-1]
        return encoded_str


    def create_visualizations(self, data):
        graphs = list()
        graph_funcs = ["sentiment_totals_graph","sentiment_groups_graph","mood_totals_graph","emoticon_totals_graph"]
        for gf, d in zip(graph_funcs, data):
            viz = getattr(self, gf)
            graphs.append(viz(d))
        print(graphs[2])
        return graphs



if __name__ == '__main__':
    g = Graphing()
    g.create_visualizations(["One","Two","Three","Four"])
