import numpy as np

input = [6.2, 2.8, 4.8, 1.8]


if (input[2]) <= (2.6):
    var2 = np.asarray([1.0, 0.0, 0.0])
else:
    if (input[2]) <= (4.8):
        if (input[0]) <= (4.95):
            if (input[3]) <= (1.35):
                var2 = np.asarray([0.0, 1.0, 0.0])
            else:
                var2 = np.asarray([0.0, 0.0, 1.0])
        else:
            var2 = np.asarray([0.0, 1.0, 0.0])
    else:
        if (input[1]) <= (2.75):
            if (input[3]) <= (1.7):
                if (input[2]) <= (5.35):
                    if (input[1]) <= (2.35):
                        var2 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        var2 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var2 = np.asarray([0.0, 0.0, 1.0])
            else:
                var2 = np.asarray([0.0, 0.0, 1.0])
        else:
            var2 = np.asarray([0.0, 0.0, 1.0])


print(var2)