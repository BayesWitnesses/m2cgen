function add_vectors(v1, v2)
    local result = {}
    for i = 1, #v1 do
        result[i] = v1[i] + v2[i]
    end
    return result
end
function mul_vector_number(v1, num)
    local result = {}
    for i = 1, #v1 do
        result[i] = v1[i] * num
    end
    return result
end