# imports
from defs.dataset import read_dataset
from defs.utils import get_avg

# loaddataset
memcat = read_dataset("memcat")
lamem = read_dataset("lamem")
figrim = read_dataset("figrim")
semmem, sub_memcat = read_dataset("semmem")

# ================================================================================
# show data for testing
"""
print("show data for testing")
print(memcat)
print(lamem)
print(figrim)
print(figrim)
print(semmem)
print(sub_memcat)
"""

# ================================================================================
# show data length for test
"""
print("show data length for test")
print(len(memcat)) # 10,000
print(len(lamem)) # 18705
print(len(figrim)) # 3508
print(len(semmem)) # 1000
print(len(sub_memcat)) # 830
"""

# ================================================================================
# show average rank per dataset
print("show average rank per dataset")
print("memcat: ", get_avg(memcat))  # 0.7584507575119
print("lamem: ", get_avg(lamem))  # 0.7561177069767442
print("figrim: ", get_avg(figrim))  # 0.2543220050302166
print("semmem: ", get_avg(semmem))  # 0.519397881051
print("sub_memcat: ", get_avg(sub_memcat))  # 0.7631869337325301

# ================================================================================
# show average rank per dataset with top 20, 100
print("show average rank per dataset with top 20, 100")

memcat.sort(reverse=True)
print("memcat - top 20 avg: ", get_avg(memcat[:20]))  # 0.9823211413
print("memcat - top 100 avg: ", get_avg(memcat[:100]))  # 0.96887152905

lamem.sort(reverse=True)
print("lamem - top 20 avg: ", get_avg(lamem[:20]))  # 1.0
print("lamem - top 100 avg: ", get_avg(lamem[:100]))  # 0.99501054

figrim.sort(reverse=True)
print("figrim - top 20 avg: ", get_avg(figrim[:20]))  # 0.4358281506
print("figrim - top 100 avg: ", get_avg(figrim[:100]))  # 0.41440102638

semmem.sort(reverse=True)
print("semmem - top 20 avg: ", get_avg(semmem[:20]))  # 0.8089810852
print("semmem - top 100 avg: ", get_avg(semmem[:100]))  # 0.70043741526

sub_memcat.sort(reverse=True)
print("sub_memcat - top 20 avg: ", get_avg(sub_memcat[:20]))  # 0.96222432745
print("sub_memcat - top 100 avg: ", get_avg(sub_memcat[:100]))  # 0.92768297518

# ================================================================================
# show average rank per dataset with bottom 20, 100
print("show average rank per dataset with bottom 20, 100")

memcat.sort()
print("memcat - bottom 20 avg: ", get_avg(memcat[:20]))  # 0.2772746313
print("memcat - bottom 100 avg: ", get_avg(memcat[:100]))  # 0.33413000734

lamem.sort()
print("lamem - bottom 20 avg: ", get_avg(lamem[:20]))  # 0.30350655
print("lamem - bottom 100 avg: ", get_avg(lamem[:100]))  # 0.35774615

figrim.sort()
print("figrim - bottom 20 avg: ", get_avg(figrim[:20]))  # 0.0625904422
print("figrim - bottom 100 avg: ", get_avg(figrim[:100]))  # 0.09623285508

semmem.sort()
print("semmem - bottom 20 avg: ", get_avg(semmem[:20]))  # 0.34619235460000003
print("semmem - bottom 100 avg: ", get_avg(semmem[:100]))  # 0.38367694033

sub_memcat.sort()
print("sub_memcat - bottom 20 avg: ", get_avg(sub_memcat[:20]))  # 0.39491099685
print("sub_memcat - bottom 100 avg: ", get_avg(sub_memcat[:100]))  # 0.49993250842
