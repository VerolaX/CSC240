import pandas as pd
import time
from itertools import combinations
from collections import OrderedDict

# data Pre-processing
df = pd.read_csv("adult.data.csv")
df = df.head(int(df.shape[0]*1))
df.columns = ["Age", "Workclass", "Fnlwgt", "Education", "Education-num", "Maritial-status", "Occupation",
                 "Relationship", "Race", "Sex", "Capital-gain", "Capital-loss", "Hours-per-week", "Native-country",
                 "Income"]
'''

df = df.astype(str)
'''
df['Fnlwgt'] = pd.cut(df['Fnlwgt'], 10).astype(str) + " Fnlwgt "
df['Education-num'] = pd.cut(df['Education-num'], 10).astype(str) + " Edu-num "
df['Capital-gain'] = pd.cut(df['Capital-gain'], 10).astype(str) + " Capital-gain"
df['Capital-loss'] = pd.cut(df['Capital-loss'], 10).astype(str) + " Capital-loss"
df['Hours-per-week'] = pd.cut(df['Hours-per-week'], 10).astype(str) + " Hours"


def partition_data(df, par): # load data and number of partitions
    avg_num = len(df) / float(par)
    result = []
    temp = 0

    while temp < len(df):
        result.append(df.iloc[int(temp):int(temp + avg_num)])
        temp += avg_num
    return result


def find_frequent_1_itemset(df, min_sup):
    sup_count = OrderedDict()
    freq_itemset = []
    if isinstance(df, list):
        for set in df:
            for item in set:
                if item in sup_count:
                    sup_count[item] += 1
                else:
                    sup_count[item] = 1
    else:
        for row in df.values:
            for item in row:
                if item in sup_count:
                    sup_count[item] += 1
                else:
                    sup_count[item] = 1

    for key in sup_count:

        if sup_count[key] / df.shape[0] >= min_sup:
            freq_itemset.append(frozenset([key]))

    return freq_itemset


def find_freq_set2(df, candidate, min_sup):
    sup_count = OrderedDict()
    freq_itemset = []
    for t in df.itertuples():
        for c in candidate:
            if set(c).issubset(set(t)):
                if c not in sup_count:
                    sup_count[c] = 1
                else:
                    sup_count[c] += 1

    for key in sup_count.keys():
        if sup_count[key]/df.shape[0] >= min_sup:
            freq_itemset.append(frozenset(key))

    return freq_itemset


def apriori_gen(l, k):
    Ck = []
    for i in range(0, len(l)):
        for j in range(i + 1, len(l)):
            if sorted(list(l[i]))[0:k-2] == sorted(list(l[j]))[0:k-2]:
                Ck.append(frozenset(l[i]|l[j]))
    return Ck


def find_freq_set(df, candidate, min_sup):
    sup_count = OrderedDict()
    freq_itemset = []
    for t in df.itertuples():
        for c in candidate:
            if c.issubset(set(t)):
                if c not in sup_count:
                    sup_count[c] = 1
                else:
                    sup_count[c] += 1

    for key in sup_count.keys():
        if sup_count[key]/df.shape[0] >= min_sup:
            freq_itemset.append(key)

    return freq_itemset


def improve(df, par, min_sup):
    par_data = partition_data(df, par)
    L = []
    for p in par_data:
        L.append(find_freq_set(p, par, min_sup))
    l1 = L[0]
    for l in range(1, len(L)):
        l1 += L[l]
    print(l1)
    freq_set = find_freq_set2(df, l1, min_sup)
    for l in range(1, len(freq_set) + 1):
        print("Frequent " + str(l) + "-Itemset")
        for t in freq_set:
            if len(t) == l:
                print(t)
        print("==========================")

    print("There are in total " + str(len(freq_set)) + " frequent itemsets in the df, with min_sup = " + str(min_sup) + ".")


def apriori(df, threshold):
    l1 = find_frequent_1_itemset(df, threshold)
    k = 2
    Lk = []
    Lk.append(l1)
    Ck = apriori_gen(l1, k)
    counter = 0
    while len(Ck) > 0:
        temp = find_freq_set(df, Ck, threshold)
        Lk.append(temp)
        k += 1
        Ck = apriori_gen(temp, k)

    for i in range(0, len(Lk)-1):
        print('Frequent', i+1, '-Itemset:')
        for k in Lk[i]:
            print(k)
            counter += 1
        print("==========================")

    print("There are in total " + str(counter) + " frequent itemsets in the df, with min_sup = " + str(threshold) + ".")




if __name__ == "__main__":
    start = time.time()
    apriori(df, 0.5)
    print("Time:", time.time() - start, "seconds.")