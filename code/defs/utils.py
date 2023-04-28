import statistics
import os
import random


def get_avg(dataset):
    return statistics.mean(dataset)


def file_exists(file):
    return os.path.isfile(file)


def get_rank(lst):
    _rank = {v: i + 1 for i, v in enumerate(sorted(set(lst)))}
    return [_rank[v] for v in lst]


def partition(list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


def spearmanrank(dataset, number_of_splition):
    result_spearman_rank = []

    if len(dataset) % 2 != 0:
        dataset = dataset[1:]

    for _ in range(number_of_splition):
        # the data sets to be ranked
        splitted_list = partition(dataset, 2)

        set_1 = splitted_list[0]
        set_2 = splitted_list[1]

        # order the sets
        set_1_ord = sorted(set_1)
        set_2_ord = sorted(set_2)

        set_1_ranked = [
            [set_1[i], set_1_ord.index(set_1[i]) + 1]
            for i in range(len(set_1))
        ]
        set_2_ranked = [
            [set_2[i], set_2_ord.index(set_2[i]) + 1]
            for i in range(len(set_2))
        ]
        d = [set_1_ranked[i][1] - set_2_ranked[i][1] for i in range(len(set_1_ranked))]
        # calculate d^2
        d_sq = [i**2 for i in d]

        # sum d^2
        sum_d_sq = sum(d_sq)

        # calculate n^3 - n
        n_cu_min_n = len(set_1) ** 3 - len(set_1)

        # calculate r
        r = 1 - ((6.0 * sum_d_sq) / n_cu_min_n)

        result_spearman_rank.append(r)

    return result_spearman_rank


def make_new_folder(folder_name, parent_folder):
    path = os.path.join(parent_folder, folder_name)
    try:
        mode = 0o777
        os.mkdir(path, mode)
    except OSError as error:
        print(error)
