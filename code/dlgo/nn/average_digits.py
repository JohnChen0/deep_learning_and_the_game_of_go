# tag::avg_imports[]
import numpy as np
from load_mnist import load_data
from layers import sigmoid_double
# end::avg_imports[]


# tag::average_digit[]
def average_digit(data, digit):  # <1>
    filtered_data = [x[0] for x in data if np.argmax(x[1]) == digit]
    filtered_array = np.asarray(filtered_data)
    return np.average(filtered_array, axis=0)


train, test = load_data()
averages = []

# <1> We compute the average over all samples in our data representing a given digit.
# <2> We use the average eight as parameters for a simple model to detect eights.
# end::average_digit[]

# tag::display_digit[]
from matplotlib import pyplot as plt

for i in range(10):
    avg = average_digit(train, i)  # <2>
    if False:
        img = (np.reshape(avg, (28, 28)))
        plt.imshow(img)
        plt.show()
    averages.append(np.transpose(avg))
# end::display_digit[]

# tag::eval_eight[]
x_3 = train[2][0]    # <1>
x_18 = train[17][0]  # <2>

# <1> Training sample at index 2 is a "4".
# <2> Training sample at index 17 is an "8"

def predict(x, averages):  # <1>
    max = -1.0
    result = -1
    for i in range(10):
        cur = np.dot(averages[i], x)
        if cur > max:
            result = i
            max = cur
    return result

print('predict x_3 is %d' % predict(x_3, averages)) # 4
print('predict x_18 is %d' % predict(x_18, averages)) # 8


# tag::evaluate_simple[]
def evaluate(data, averages):
    total_samples = 1.0 * len(data)
    correct_predictions = 0
    for x in data:
        if predict(x[0], averages) == np.argmax(x[1]):
            correct_predictions += 1
    return correct_predictions / total_samples
# end::evaluate_simple[]


# tag::evaluate_example[]
print(evaluate(train, averages))
print(evaluate(test, averages))

# end::evaluate_example[]
