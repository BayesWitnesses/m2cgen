import numpy as np
def  score(input):
    if (input[3]) <= (0.8):
        var0 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[2]) <= (4.8500004):
            if (input[1]) <= (2.55):
                if (input[3]) <= (1.6):
                    var0 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var0 = np.asarray([0.0, 0.0, 1.0])
            else:
                var0 = np.asarray([0.0, 1.0, 0.0])
        else:
            if (input[3]) <= (1.75):
                if (input[0]) <= (6.95):
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
    if (input[3]) <= (0.8):
        var1 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[0]) <= (6.05):
            if (input[2]) <= (4.9):
                if (input[0]) <= (4.95):
                    var1 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var1 = np.asarray([0.0, 1.0, 0.0])
            else:
                var1 = np.asarray([0.0, 0.0, 1.0])
        else:
            if (input[3]) <= (1.75):
                if (input[1]) <= (3.05):
                    if (input[2]) <= (5.05):
                        var1 = np.asarray([0.0, 1.0, 0.0])
                    else:
                        var1 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var1 = np.asarray([0.0, 1.0, 0.0])
            else:
                var1 = np.asarray([0.0, 0.0, 1.0])
    if (input[2]) <= (2.6):
        var2 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[3]) <= (1.75):
            if (input[2]) <= (5.05):
                var2 = np.asarray([0.0, 1.0, 0.0])
            else:
                if (input[2]) <= (5.35):
                    if (input[1]) <= (2.75):
                        var2 = np.asarray([0.0, 1.0, 0.0])
                    else:
                        var2 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var2 = np.asarray([0.0, 0.0, 1.0])
        else:
            var2 = np.asarray([0.0, 0.0, 1.0])
    if (input[3]) <= (0.7):
        var3 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[2]) <= (4.8500004):
            if (input[3]) <= (1.6500001):
                var3 = np.asarray([0.0, 1.0, 0.0])
            else:
                if (input[1]) <= (2.85):
                    var3 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var3 = np.asarray([0.0, 1.0, 0.0])
        else:
            if (input[3]) <= (1.75):
                if (input[0]) <= (6.2):
                    if (input[1]) <= (2.65):
                        var3 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        var3 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var3 = np.asarray([0.0, 1.0, 0.0])
            else:
                var3 = np.asarray([0.0, 0.0, 1.0])
    if (input[3]) <= (0.7):
        var4 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[3]) <= (1.6500001):
            if (input[3]) <= (1.55):
                if (input[1]) <= (2.65):
                    if (input[3]) <= (1.3499999):
                        var4 = np.asarray([0.0, 1.0, 0.0])
                    else:
                        if (input[0]) <= (6.2):
                            var4 = np.asarray([0.0, 0.0, 1.0])
                        else:
                            var4 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var4 = np.asarray([0.0, 1.0, 0.0])
            else:
                if (input[2]) <= (5.45):
                    var4 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var4 = np.asarray([0.0, 0.0, 1.0])
        else:
            var4 = np.asarray([0.0, 0.0, 1.0])
    if (input[3]) <= (0.75):
        var5 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[3]) <= (1.75):
            if (input[3]) <= (1.3499999):
                var5 = np.asarray([0.0, 1.0, 0.0])
            else:
                if (input[2]) <= (5.05):
                    if (input[1]) <= (2.65):
                        if (input[2]) <= (4.7):
                            var5 = np.asarray([0.0, 0.0, 1.0])
                        else:
                            if (input[2]) <= (4.95):
                                var5 = np.asarray([0.0, 1.0, 0.0])
                            else:
                                var5 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        var5 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var5 = np.asarray([0.0, 0.0, 1.0])
        else:
            var5 = np.asarray([0.0, 0.0, 1.0])
    if (input[2]) <= (2.7):
        var6 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[3]) <= (1.75):
            if (input[0]) <= (7.0):
                if (input[2]) <= (4.9):
                    var6 = np.asarray([0.0, 1.0, 0.0])
                else:
                    if (input[1]) <= (2.65):
                        var6 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        if (input[3]) <= (1.55):
                            var6 = np.asarray([0.0, 0.0, 1.0])
                        else:
                            var6 = np.asarray([0.0, 1.0, 0.0])
            else:
                var6 = np.asarray([0.0, 0.0, 1.0])
        else:
            if (input[2]) <= (4.8500004):
                if (input[0]) <= (5.95):
                    var6 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var6 = np.asarray([0.0, 0.0, 1.0])
            else:
                var6 = np.asarray([0.0, 0.0, 1.0])
    if (input[3]) <= (0.8):
        var7 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[2]) <= (4.8500004):
            var7 = np.asarray([0.0, 1.0, 0.0])
        else:
            if (input[2]) <= (5.2):
                if (input[0]) <= (6.5):
                    if (input[2]) <= (5.05):
                        var7 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        if (input[1]) <= (2.75):
                            if (input[0]) <= (5.9):
                                var7 = np.asarray([0.0, 0.0, 1.0])
                            else:
                                var7 = np.asarray([0.0, 1.0, 0.0])
                        else:
                            var7 = np.asarray([0.0, 0.0, 1.0])
                else:
                    if (input[1]) <= (3.05):
                        var7 = np.asarray([0.0, 1.0, 0.0])
                    else:
                        var7 = np.asarray([0.0, 0.0, 1.0])
            else:
                var7 = np.asarray([0.0, 0.0, 1.0])
    if (input[2]) <= (4.8500004):
        if (input[0]) <= (5.45):
            if (input[3]) <= (0.8):
                var8 = np.asarray([1.0, 0.0, 0.0])
            else:
                var8 = np.asarray([0.0, 1.0, 0.0])
        else:
            var8 = np.asarray([0.0, 1.0, 0.0])
    else:
        if (input[3]) <= (1.75):
            if (input[2]) <= (5.3):
                if (input[0]) <= (6.15):
                    var8 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var8 = np.asarray([0.0, 1.0, 0.0])
            else:
                var8 = np.asarray([0.0, 0.0, 1.0])
        else:
            var8 = np.asarray([0.0, 0.0, 1.0])
    if (input[2]) <= (2.6):
        var9 = np.asarray([1.0, 0.0, 0.0])
    else:
        if (input[2]) <= (4.8500004):
            if (input[3]) <= (1.6500001):
                var9 = np.asarray([0.0, 1.0, 0.0])
            else:
                if (input[3]) <= (1.75):
                    var9 = np.asarray([0.0, 0.0, 1.0])
                else:
                    var9 = np.asarray([0.0, 1.0, 0.0])
        else:
            if (input[1]) <= (2.75):
                if (input[3]) <= (1.7):
                    if (input[3]) <= (1.55):
                        if (input[2]) <= (4.95):
                            var9 = np.asarray([0.0, 1.0, 0.0])
                        else:
                            var9 = np.asarray([0.0, 0.0, 1.0])
                    else:
                        var9 = np.asarray([0.0, 1.0, 0.0])
                else:
                    var9 = np.asarray([0.0, 0.0, 1.0])
            else:
                var9 = np.asarray([0.0, 0.0, 1.0])
    return ((((((((((var0) * (0.1)) + ((var1) * (0.1))) + ((var2) * (0.1))) + ((var3) * (0.1))) + ((var4) * (0.1))) + ((var5) * (0.1))) + ((var6) * (0.1))) + ((var7) * (0.1))) + ((var8) * (0.1))) + ((var9) * (0.1))
