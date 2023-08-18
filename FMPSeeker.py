import argparse
import itertools
import pandas as pd
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

parser = argparse.ArgumentParser(description="mainDBS and maskPath should be provided.")
parser.add_argument("--AlterationDBS", type=str, help="İlk float değeri girin")
parser.add_argument("--minSupports", nargs='+', default=None, type=float, help="Bir liste olarak tamsayıları girin")
parser.add_argument("--minTreshs", nargs='+', default=None, type=float, help="Bir liste olarak tamsayıları girin")
parser.add_argument("--maskDBS", type=str, help="İkinci float değeri girin")
args = parser.parse_args()

AltDBSPath = args.AlterationDBS
maskJsonName = args.maskDBS
minSupports = args.minSupports
minTreshs = args.minTreshs


def sortedKeys(ItemLs, FreqLs):
    returned = dict()
    for Item in ItemLs:
        returned[Item] = FreqLs[Item]

    sortedDict = dict(sorted(returned.items(), key=lambda x: x[1], reverse=True))
    return list(sortedDict.keys())


def find_pair(edge, df):
    try:
        nodeA = edge[0].split("|")[-1]
        nodeB = edge[1].split("|")[-1]
        return sum(1 for i in range(len(df) - 1) if df[nodeA][i] == 1 and df[nodeB][i] == 1)
    except:
        return 0


def drawTree(G, minSupport, minTresh):
    node_colors = ['blue' for _ in G.nodes()]

    # print(node_colors)
    for i, node in enumerate(G.nodes(data=True)):
        if node[1].get('case') == 'ANTE':
            node_colors[i] = 'red'

    labels = {node: node.split("|")[-1] for node in G.nodes()}

    # print(labels)
    pos = graphviz_layout(G, prog="twopi", args="")
    # print(pos)
    plt.figure(figsize=(15, 15))
    node_sizes = [AltDBS[node.split("|")[-1]].sum() if node != "NULL" else 1 for node in G.nodes]
    # print(node_sizes)
    nx.draw(G, pos, alpha=0.4, node_color=node_colors, with_labels=True, font_size=10, labels=labels,
            node_size=node_sizes)  # node_sizes=node_sizes

    """      --------     ENRICH EDGES       ----------     """

    edge_labels = {edge: find_pair(list(edge), AltDBS) for edge in G.edges}

    nx.draw_networkx_edge_labels(G, pos, alpha=1, edge_labels=edge_labels)
    plt.axis("equal")

    plt.show()
    minSupport, minTresh = str(minSupport).split(".")[-1], \
                           str(minTresh).split(".")[-1]

    if maskJsonName.split(".")[-1] == "json":
        name = maskJsonName.replace(".json", ".minSupport" + minSupport + "." + "minTresh" + minTresh + ".png")
    else:
        name = maskJsonName.replace(".tsv", ".minSupport" + minSupport + "." + "minTresh" + minTresh + ".png")

    nx.write_graphml(G, name.replace(".png", ".xml"))
    plt.savefig(name)


def buildTree(Pairs, minSupport, minTresh):
    G, AllAntes, AllCons = nx.DiGraph(), \
                           [list(Item["Ante"]) for Item in Pairs], \
                           [list(Item["Cons"]) for Item in Pairs]

    freqAntes, freqCons = Counter(list(itertools.chain.from_iterable(AllAntes))), \
                          Counter(list(itertools.chain.from_iterable(AllCons)))

    sortedAllAntes, sortedAllCons = [sortedKeys(Pairs, freqAntes) for Pairs in AllAntes], \
                                    [sortedKeys(Pairs, freqCons) for Pairs in AllCons]

    BranchesCollection = list()
    for IndexPair in range(len(sortedAllAntes)):
        Branch, counter = dict(), 0
        for Item in sortedAllAntes[IndexPair]:
            counter += 1
            Branch[Item] = {"case": "ANTE", "degree": counter}
        for Item in sortedAllCons[IndexPair]:
            counter += 1
            Branch[Item] = {"case": "CONS", "degree": counter}

        BranchesCollection.append(Branch)

    G = nx.DiGraph()
    for BranchSet in BranchesCollection:
        Branch = list(BranchSet.keys())
        G.add_edge('NULL', Branch[0])
        for i in range(len(Branch) - 1):
            node1, node2 = "|".join(Branch[:i + 1]), \
                           "|".join(Branch[:i + 2])

            G.add_edge(node1, node2)

            for Node in [node1, node2]:
                nx.set_node_attributes(G, {Node: BranchSet[Node.split("|")[-1]]})
    print(G)
    drawTree(G, minSupport, minTresh)


if __name__ == '__main__':

    try:
        AltDBS = pd.read_json(AltDBSPath)

    except:
        AltDBS = pd.read_csv(AltDBSPath).set_index("Unnamed: 0")
    try:
        maskJson = pd.read_json(maskJsonName).index.to_list()

    except:
        maskJsonFile = open(maskJsonName, "r")
        maskJson = maskJsonFile.read().rstrip("\n").split("\n")
        maskJsonFile.close()

    intersectMask = list(set(AltDBS.index.to_list()).intersection(set(maskJson)))
    print(intersectMask)
    AltDBS = AltDBS.loc[intersectMask]

    if minSupports is None or minTreshs is None:

        minSupports, minTreshs = [
                                     0.0005,
                                     0.001,
                                     0.003,
                                     0.005,
                                     0.01,
                                     0.03,
                                     0.05], [0.01,
                                             0.03,
                                             0.001,
                                             0.003,
                                             0.005,
                                             0.0001,
                                             0.0003
                                             ]

    else:
        print(minSupports, minTreshs)
        pass

    for minSupport in minSupports:
        for minTresh in minTreshs:
            try:
                from mlxtend.frequent_patterns.fpgrowth import fpgrowth

                FreqItems = fpgrowth(AltDBS, min_support=minSupport, use_colnames=True)

                # print(FreqItems)
                from mlxtend.frequent_patterns import association_rules

                AssociationDBS = association_rules(FreqItems, metric="confidence", min_threshold=minTresh)
                # print(AssociationDBS.columns)

                Ante, Cons, Pairs = AssociationDBS["antecedents"], \
                                    AssociationDBS["consequents"], list()
                for i in range(len(Ante)):
                    Pairs.append({"Ante": set(Ante[i]),
                                  "Cons": set(Cons[i])})

                buildTree(Pairs, minSupport, minTresh)

            except:
                pass