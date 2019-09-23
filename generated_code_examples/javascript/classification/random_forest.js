function score(input) {
    var var0;
    if ((input[3]) <= (0.8)) {
        var0 = [1.0, 0.0, 0.0];
    } else {
        if ((input[2]) <= (4.8500004)) {
            var0 = [0.0, 0.9795918367346939, 0.02040816326530612];
        } else {
            if ((input[3]) <= (1.75)) {
                if ((input[3]) <= (1.6500001)) {
                    var0 = [0.0, 0.25, 0.75];
                } else {
                    var0 = [0.0, 1.0, 0.0];
                }
            } else {
                var0 = [0.0, 0.0, 1.0];
            }
        }
    }
    var var1;
    if ((input[3]) <= (0.8)) {
        var1 = [1.0, 0.0, 0.0];
    } else {
        if ((input[0]) <= (6.05)) {
            if ((input[2]) <= (4.9)) {
                var1 = [0.0, 0.9032258064516129, 0.0967741935483871];
            } else {
                var1 = [0.0, 0.0, 1.0];
            }
        } else {
            if ((input[3]) <= (1.75)) {
                var1 = [0.0, 0.8, 0.2];
            } else {
                var1 = [0.0, 0.0, 1.0];
            }
        }
    }
    return addVectors(mulVectorNumber(var0, 0.5), mulVectorNumber(var1, 0.5));
}
function addVectors(v1, v2) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
function mulVectorNumber(v1, num) {
    let result = new Array(v1.length);
    for (let i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
