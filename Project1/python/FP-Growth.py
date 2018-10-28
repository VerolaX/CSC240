import pandas as pd
import time

# data Pre-processing
df = pd.read_csv("adult.data.csv")
df.columns = ["Age", "Workclass", "Fnlwgt", "Education", "Education-num", "Maritial-status", "Occupation",
                 "Relationship", "Race", "Sex", "Capital-gain", "Capital-loss", "Hours-per-week", "Native-country",
                 "Income"]

df['Fnlwgt'] = pd.cut(df['Fnlwgt'], 10).astype(str) + " Fnlwgt "
df['Education-num'] = pd.cut(df['Education-num'], 10).astype(str) + " Edu-num "
df['Capital-gain'] = pd.cut(df['Capital-gain'], 10).astype(str) + " Capital-gain"
df['Capital-loss'] = pd.cut(df['Capital-loss'], 10).astype(str) + " Capital-loss"
df['Hours-per-week'] = pd.cut(df['Hours-per-week'], 10).astype(str) + " Hours"


class TreeNode:
    def __init__(self, item, parent, count):
        self.item = item
        self.children = []
        self.parent = parent
        self.count = count


def find_frequent_1_itemset(df, min_sup):
    sup_count = {}
    for t in df:
        for item in t:
            if item not in sup_count:
                sup_count[item] = df[t]
            else:
                sup_count[item] += df[t]
    freq_itemset = {}
    for keys in sup_count:
        if sup_count[keys] >= min_sup:
            freq_itemset[keys] = sup_count[keys]
    return freq_itemset


def createtree(df, min_sup):
    freq_set = find_frequent_1_itemset(df, min_sup)
    sorted_item = sorted(freq_set, key=freq_set.get)  # ascending
    header = {}
    for i in sorted_item:
        header[i] = []
    root = TreeNode('Null', None, 1)
    for t in df:
        pattern = []
        for item in reversed(sorted_item):  # descend
            if item in set(t):
                pattern.append(item)
        updatetree(root, pattern, header, df[t])
    return root, header


def minetree(data, pref, freq_pattern, min_sup):
    root, header = createtree(data, min_sup)
    for item in header:
        freq = set(pref)
        freq.add(item)
        freq_pattern.append(freq)
        conditional_pattern = {}
        while header[item]:
            if header[item]:
                path = []
                prefix(header[item][0], path)
                if len(path) > 1:
                    conditional_pattern[frozenset(path[1:])] = header[item][0].count
                header[item].pop(0)
        minetree(conditional_pattern, freq, freq_pattern, min_sup)


def prefix(node, path):
    if node.parent:
        path.append(node.item)
        prefix(node.parent, path)


def updatetree(root, pattern, header, count):
    while pattern:
        item = pattern.pop(0)
        in_children = False
        # check if the current tree has a branch of each item
        for child in root.children:
            if child.item == item:
                child.count += count
                in_children = True
                root = child
        if not in_children:
            leaf = TreeNode(item, root, count)
            root.children.append(leaf)
            header[item].append(leaf)
            root = leaf


def run(df, min_sup):
    items = {}
    for t in df.itertuples():
        items[frozenset(t)] = 1

    freq_item = []
    minetree(items, set([]), freq_item, df.shape[0]*min_sup)
    s = sorted(freq_item,key=len)
    for l in range(1, len(s[-1]) + 1):
        print("Frequent " + str(l) + "-Itemset")
        for t in s:
            if len(t) == l:
                print(t)
        print("==========================")

    print("There are in total " + str(len(freq_item)) + " frequent itemsets in the df, with min_sup = " + str(min_sup) + ".")


if __name__ == "__main__":
    start = time.time()
    run(df, min_sup=0.5)
    print("Time:", time.time() - start, "seconds.")