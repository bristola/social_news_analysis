import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from matplotlib import rc
from math import pi
# from matplotlib.figure_manager import fontManager as fm

class Graphing:

    def __init__(self):
        # rc('font', family='LastResort')
        # fm.findfont('symbola')
        pass


    def sentiment_totals_graph(self, data):
        plt.clf()

        data = [-0.09159018091433064956,0.12406316863636363636]
        range_pos = max([abs(d) for d in data])
        categories = ("Twitter", "News")

        fig, ax = plt.subplots(figsize=(20, 2))
        plt.subplots_adjust(left=0.1, right=0.9, top=.7, bottom=0.2)

        bars = ax.barh(range(0,len(data)), data, align='edge', height=.7, color="khaki")
        colors = ["darkred","forestgreen"]
        for bar, d, category in zip(bars, data, categories):
            bar.set_color(colors[0] if d < 0 else colors[1])
            ax.text(bar.get_x(), bar.get_y() - .05, r'\textbf{%s}' % (category), fontweight='bold', horizontalalignment='center')
        for i, v in enumerate(data):
            ax.text(v, i-.05, str("%.3f" % v), horizontalalignment='center')
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xlim([range_pos * -1, range_pos])
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_title(r'\textbf{\underline{Overall Sentiment}}', fontweight='bold', fontsize=18, y=1.25, horizontalalignment='center')

        return self.plot_to_base()


    def sentiment_groups_graph(self, data):
        plt.clf()

        objects = ("Very Negative","Negative","Neutral","Positive","Very Positive")
        bars = plt.bar(range(0, len(data)), data, align='center', alpha=0.8)
        colors = ["darkred","indianred","khaki","palegreen","forestgreen"]
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        plt.xticks(range(0,len(data)), objects)
        plt.xlabel("Sentiment")
        plt.ylabel("Number of Views")
        plt.title("Views in Different Sentiment Groups")

        return self.plot_to_base()


    def mood_totals_graph(self, data):
        plt.clf()

        twitter_data = data[0]

        news_data = data[1]

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

        return self.plot_to_base()


    def emoticon_totals_graph(self, data):
        data = {
            '😂': 12,
            '🇺': 8,
            '🇸': 8,
            '🏻': 7,
            '👇': 6,
            '🥕': 6,
            '\U0001f92c': 5,
            '😡': 5,
            '\U0001f92a': 4,
            '🤔': 4
        }
        plt.clf()

        bars = plt.bar(range(0, len(data.values())), data.values(), align='center', alpha=0.8)
        plt.xticks(range(0,len(data)), data.keys(), fontname='Apple Color Emoji')
        plt.xlabel("Emotoicon")
        plt.ylabel("Number of Occurences")
        plt.title("Most Used Emoticons")

        plt.show()

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
        return graphs



if __name__ == '__main__':
    g = Graphing()
    g.create_visualizations(["One","Two","Three","Four"])
