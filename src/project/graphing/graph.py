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

        twitter_data = data[0]

        news_data = data[1]

        plt.clf()

        colors = {
        "happiness": "springgreen",
        "anxiety": "slategrey",
        "sadness": "royalblue",
        "affection": "mediumorchid",
        "aggression": "firebrick",
        "expressive": "lightpink",
        "glory": "goldenrod"
        }

        out_colors = list()
        out_categories = list()
        out_data = list()
        for category, amount in twitter_data.items():
            out_colors.append(colors[category])
            out_categories.append(category)
            out_data.append(amount)

        explode = (0.1, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 6))
        plt.subplots_adjust(wspace=.5)
        ax1.pie(out_data, explode=explode, labels=out_categories, autopct='%1.1f%%',
                shadow=True, startangle=90, colors=out_colors)
        ax1.axis('equal')
        ax1.set_title("Twitter", y=.1)

        out_colors = list()
        out_categories = list()
        out_data = list()
        for category, amount in news_data.items():
            out_colors.append(colors[category])
            out_categories.append(category)
            out_data.append(amount)

        explode = (0.1, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        ax2.pie(out_data, explode=explode, labels=out_categories, autopct='%1.1f%%',
                shadow=True, startangle=100, colors=out_colors)
        ax2.axis('equal')
        ax2.set_title("News", y=.1)

        plt.suptitle("Mood Words", y=.8)

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
