import numpy as np
def  score(input):
    if (input[2]) <= (2.6):
        var0 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[2]) <= (4.8500004):
            if (input[3]) <= (1.6500001):
                var0 = np.asarray([0.0, 1.0, 0.0])
            else:
                if (input[1]) <= (3.1):
                    var0 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var0 = np.asarray([0.0, 1.0, 0.0])
        else:
            if (input[3]) <= (1.75):
                if (input[2]) <= (5.35):
                    if (input[3]) <= (1.55):
                        if (input[2]) <= (4.95):
                            var0 = np.asarray([0.0, 1.0, 0.0])
                        else:
                            var0 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        var0 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var0 = np.asarray([0.0, 0.0, 1.0])
            else:
                var0 = np.asarray([0.0, 0.0, 1.0])
    return var0
