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
