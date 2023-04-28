import numpy as np

csv_file = np.genfromtxt("data/amt1-figrim.csv", delimiter=",")


for x in csv_file:
    n_resp = x[0] + x[1] + x[2] + x[3]
    with_f = (x[0] - x[2]) / (n_resp)
    without_f = (x[0]) / (n_resp)

    with open("data/txt/with_f.txt", "a") as f:
        if with_f > 0:
            f.write(str(with_f) + "\n")

    with open("data/txt/without_f.txt", "a") as g:
        g.write(str(without_f) + "\n")
