import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import os
from matplotlib import font_manager as fm, rcParams
from matplotlib import rc
from math import pi
# from matplotlib.figure_manager import fontManager as fm

class Graphing:

    def __init__(self):
        pass


    def sentiment_totals_graph(self, data):
        plt.clf()

        data = [float(d) for d in data]

        range_pos = max([abs(d) for d in data])
        categories = ("Twitter", "News")

        fig, ax = plt.subplots(figsize=(20, 5))
        plt.subplots_adjust(left=0.1, right=0.9, top=.7, bottom=0.2)

        bars = ax.barh(range(0,len(data)), data, align='edge', height=.7, color="khaki")
        colors = ["darkred","forestgreen"]
        for bar, d, category in zip(bars, data, categories):
            bar.set_color(colors[0] if d < 0 else colors[1])
            ax.text(bar.get_x(), bar.get_y() - .05, category, fontsize=22, fontweight='bold', horizontalalignment='center')
        for i, v in enumerate(data):
            ax.text(v, i-.05, str("%.3f" % v), fontsize=22, horizontalalignment='center')
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xlim([range_pos * -1, range_pos])
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_title("Overall Sentiment", fontweight='bold', fontsize=30, y=1.25, horizontalalignment='center')

        return self.plot_to_base()


    def sentiment_groups_graph(self, data):
        plt.clf()

        plt.figure(figsize=(8, 4))
        objects = ("Very Negative","Negative","Neutral","Positive","Very Positive")
        bars = plt.bar(range(0, len(data)), data, align='center', alpha=0.8, width=.35)
        colors = ["darkred","indianred","khaki","palegreen","forestgreen"]
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        m = max(data)
        plt.yticks([m/2,m,m*3/2])
        plt.xticks(range(0,len(data)), objects)
        plt.xlabel("Sentiment")
        plt.ylabel("Number of Views")
        plt.title("Views in Different Sentiment Groups", fontweight='bold')

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
        out_data1 = list()
        for category, amount in twitter_data.items():
            out_colors.append(colors[category])
            out_categories.append(category)
            out_data1.append(amount)

        s1 = sum(out_data1)
        explode = (0.1, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        plt.subplots_adjust(wspace=.5)
        auto_pct_func = lambda pct : ('%1.1f' % pct) if pct > 7.5 else ''
        a1, b1, c1 = ax1.pie(out_data1, explode=explode, labels=[c if int(d)/s1*100 > 7.5 else '' for c, d in zip(out_categories, out_data1)], autopct=auto_pct_func,
                shadow=True, startangle=90, colors=out_colors)
        ax1.axis('equal')
        ax1.set_title("Twitter", y=1.1)

        out_data2 = list()
        for c in out_categories:
            out_data2.append(news_data[c])

        s2 = sum(out_data2)
        explode = (0.1, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        a2, b2, c2 = ax2.pie(out_data2, explode=explode, labels=[c if int(d)/s2*100 > 7.5 else '' for c, d in zip(out_categories, out_data2)], autopct=auto_pct_func,
                shadow=True, startangle=100, colors=out_colors)
        ax2.axis('equal')
        ax2.set_title("News", y=1.1)

        plt.suptitle("Mood Words", fontweight='bold', y=.97)

        plt.subplots_adjust(left=0.1, right=0.9, top=.8, bottom=0.3)

        custom = [plt.Line2D([0], [0], color=c, lw=4) for c in out_colors]
        s1 = sum(out_data1)
        s2 = sum(out_data2)
        labels = ["%s\nTwitter:%.2f%%\nNews:%.2f%%" % (category, t/s1*100, n/s2*100) for category, t, n in zip(out_categories, out_data1, out_data2)]

        ax1.legend(custom, labels, loc='lower left',ncol=4,bbox_to_anchor=(0, -.6, 0.25, 0.25))

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
        graph_funcs = ["sentiment_totals_graph","sentiment_groups_graph","mood_totals_graph"]
        for gf, d in zip(graph_funcs, data):
            viz = getattr(self, gf)
            graphs.append(viz(d))
        return graphs
