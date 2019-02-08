import numpy as np
def  score(input):
    if (input[3]) <= (0.8):
        var0 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[2]) <= (4.8500004):
            var0 = np.asarray([0.0, 0.9795918367346939, 0.02040816326530612])
        else:
            if (input[3]) <= (1.75):
                if (input[3]) <= (1.6500001):
                    var0 = np.asarray([0.0, 0.25, 0.75])
                else:
                    var0 = np.asarray([0.0, 1.0, 0.0])
            else:
                var0 = np.asarray([0.0, 0.0, 1.0])
    if (input[3]) <= (0.8):
        var1 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[0]) <= (6.05):
            if (input[2]) <= (4.9):
                var1 = np.asarray([0.0, 0.9032258064516129, 0.0967741935483871])
            else:
                var1 = np.asarray([0.0, 0.0, 1.0])
        else:
            if (input[3]) <= (1.75):
                var1 = np.asarray([0.0, 0.8, 0.2])
            else:
                var1 = np.asarray([0.0, 0.0, 1.0])
    return ((var0) * (0.5)) + ((var1) * (0.5))
