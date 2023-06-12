import numpy as np
import matplotlib.pyplot as plt

def f(x, p):
    return 10000000 / (1 + np.exp(p * (x - 1000)))
    # return 200000 / (1 + np.exp(p * (x - 250))) + 700000 / (1 + np.exp(p * (x - 900)))


x = np.linspace(0, 500, 10000)

# plt.plot(x, f(x, -0.01), color='r')
# plt.plot(x, np.gradient(f(x, -0.015), x), color='b')
# plt.plot(x, np.gradient(8 * x, x), color='y')

plt.plot(x, f(x, -0.015), color='b')
plt.plot(x, 8 * x, color='y')

plt.show()

# if __name__ == '__main__':
#     read_file = open("/home/sqsq/Desktop/test.cc", "r")
#     lines = read_file.readlines()
#     print(lines[47])
#     lines[47] = "#define SQSQ_HOP                               114541\n"
#     read_file.close()

#     write_file = open("/home/sqsq/Desktop/test.cc", "w")
#     write_file.writelines(lines)
#     write_file.close()
