function softmax(x)
    local size = #x
    local result = {}
    local max = x[1]
    for _, v in pairs(x) do
        if v > max then
            max = v
        end
    end
    local sum = 0.0
    for i = 1, size do
        result[i] = math.exp(x[i] - max)
        sum = sum + result[i]
    end
    for i = 1, size do
        result[i] = result[i] / sum
    end
    return result
end