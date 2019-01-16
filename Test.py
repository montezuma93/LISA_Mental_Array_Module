import numpy
from scipy.stats import norm
x = numpy.random.normal(6, 1, 3)
mean = numpy.mean(x)
print(int(round(mean)))

for i in range(9):
    print(round(norm.pdf(i, 6, 0.5),4)*100)