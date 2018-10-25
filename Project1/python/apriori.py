import pandas as pd
import time
from itertools import combinations

# df Pre-processing
df = pd.read_csv("adult.data.csv")
df.columns = ["Age", "Workclass", "Fnlwgt", "Education", "Education-num", "Maritial-status", "Occupation",
                 "Relationship", "Race", "Sex", "Capital-gain", "Capital-loss", "Hours-per-week", "Native-country",
                 "Income"]

df['Fnlwgt'] = "Fnlwgt " + pd.cut(df['Fnlwgt'], 10).astype(str)
df['Education-num'] = "Edu-num " + pd.cut(df['Education-num'], 10).astype(str)
df['Capital-gain'] = "Capital-gain " + pd.cut(df['Capital-gain'], 10).astype(str)
df['Capital-loss'] = "Capital-loss " + pd.cut(df['Capital-loss'], 10).astype(str)
df['Hours-per-week'] = "Hours" + pd.cut(df['Hours-per-week'], 10).astype(str)


def find_frequent_1_itemset(df, min_sup):
    supp_count = {}
    freq_itemset = []
    for row in df.values:
        for item in row:
            if item in supp_count:
                supp_count[item] += 1
            else:
                supp_count[item] = 1

    for key in supp_count:

        if supp_count[key] / df.shape[0] >= min_sup:
            freq_itemset.append(frozenset([key]))

    return freq_itemset


def apriori_gen(l, k):
    Ck = []
    for i in range(0, len(l)):
        for j in range(i + 1, len(l)):
            if sorted(list(l[i]))[0:k-2] == sorted(list(l[j]))[0:k-2]:
                Ck.append(frozenset(l[i]|l[j]))

    return Ck


def find_freq_set(df, candidate, min_sup):
    supp_count = {}
    freq_itemset = []
    for t in df.itertuples():
        for c in candidate:
            if c.issubset(set(t)):
                if c not in supp_count:
                    supp_count[c] = 1
                else:
                    supp_count[c] += 1

    for key in supp_count.keys():
        if supp_count[key]/df.shape[0] >= min_sup:
            freq_itemset.append(key)

    return freq_itemset


def has_infrequent_subset(c, Lk_1):
    for s in combinations(c, len(c) - 1):
        if s not in Lk_1:
            return True
    return False


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
        print('Frequent', i + 1, '-Itemset:')
        for k in Lk[i]:
            print(k)
            counter += 1
        print("==========================")

    print("There are in total " + str(counter) + " frequent itemsets in the df, with min_sup = " + str(threshold) + ".")


if __name__ == "__main__":
    start = time.time()

    apriori(df, 0.23)

    print("Runtime:", round(time.time() - start, 2), "seconds.")