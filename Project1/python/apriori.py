import pandas as pd

# Data Pre-processing
data = pd.read_csv("test.csv")
data.columns = ["Age", "Workclass", "Fnlwgt", "Education", "Education-num", "Maritial-status", "Occupation",
                 "Relationship", "Race", "Sex", "Capital-gain", "Capital-loss", "Hours-per-week", "Native-country",
                 "Income"]

data['Fnlwgt'] = "Fnlwgt " + pd.cut(data['Fnlwgt'], 10).astype(str)
data['Education-num'] = "Edu-num " + pd.cut(data['Education-num'], 10).astype(str)
data['Capital-gain'] = "Capital-gain " + pd.cut(data['Capital-gain'], 10).astype(str)
data['Capital-loss'] = "Capital-loss " + pd.cut(data['Capital-loss'], 10).astype(str)
data['Hours-per-week'] = "Hours" + pd.cut(data['Hours-per-week'], 10).astype(str)


def find_frequent_1_itemset(data, min_sup):
    supp_count = {}
    freq_itemset = []
    for row in data.values:
        for item in row:
            if item in supp_count:
                supp_count[item] += 1
            else:
                supp_count[item] = 1

    for key in supp_count:

        if supp_count[key] / data.shape[0] >= min_sup:
            freq_itemset.append(frozenset([key]))

    return freq_itemset


def apriori_gen(l, k):
    Ck = []
    for i in range(0, len(l)):
        for j in range(i + 1, len(l)):
            if list(l[i])[0:k-2] == list(l[j])[0:k-2]:
                Ck.append(frozenset(l[i]|l[j]))

    return Ck


def find_freq_set(data, candidate, min_sup):
    supp_count = {}
    freq_itemset = []
    for t in data.itertuples():
        for c in candidate:
            if c.issubset(set(t)):
                if c not in supp_count:
                    supp_count[c] = 1
                else:
                    supp_count[c] += 1

    for key in supp_count.keys():
        if supp_count[key]/data.shape[0] >= min_sup:
            freq_itemset.append(key)

    return freq_itemset


def has_infrequent_subset(c, Lk_1):
    c_temp = c
    for i in range(0, len(Lk_1)):
        c_temp.remove(c_temp[i])
        if c_temp in Lk_1:
            pass
        else:
            return True
        c_temp = c


def apriori(data, threshold):
    l1 = find_frequent_1_itemset(data, threshold)
    k = 2
    temp = []
    Lk = []
    Lk.append(l1)
    Ck = apriori_gen(l1, k)
    counter = 0
    while len(Ck) > 0:
        temp = find_freq_set(data, Ck, threshold)
        Lk.append(temp)
        k += 1
        Ck = apriori_gen(temp, k)

    for i in range(0, len(Lk)-1):
        print('Frequent', i + 1, '-Itemset:')
        for k in Lk[i]:
            print(k)
            counter += 1
        print("==========================")

    print("There are in total " + str(counter) + " frequent itemsets in the data, with min_sup = " + str(threshold) + ".")


if __name__ == "__main__":
    apriori(data, 0.23)