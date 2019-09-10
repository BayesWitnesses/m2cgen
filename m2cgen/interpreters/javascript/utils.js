function dict_null_to_nan(input) {
    for (const [key, value] of Object.entries(input)) {
        if (value == null)
            input[key] = NaN;
    }
    return input;
}

function dict_to_value_array(input) {
    var output = [];
    for (const elem in input) {
        output.push(input[elem]);
    }
    return output;
}