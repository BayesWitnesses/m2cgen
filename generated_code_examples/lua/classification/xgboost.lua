function score(input)
    if input[3] >= 2.45 then
        var0 = -0.21995015
    else
        var0 = 0.4302439
    end
    if input[3] >= 2.45 then
        var1 = -0.19691855
    else
        var1 = 0.29493433
    end
    if input[3] >= 2.45 then
        if input[4] >= 1.75 then
            var2 = -0.20051816
        else
            var2 = 0.36912444
        end
    else
        var2 = -0.21512198
    end
    if input[3] >= 2.45 then
        if input[3] >= 4.8500004 then
            var3 = -0.14888482
        else
            var3 = 0.2796613
        end
    else
        var3 = -0.19143805
    end
    if input[4] >= 1.6500001 then
        var4 = 0.40298507
    else
        if input[3] >= 4.95 then
            var4 = 0.21724138
        else
            var4 = -0.21974029
        end
    end
    if input[3] >= 4.75 then
        if input[4] >= 1.75 then
            var5 = 0.28692952
        else
            var5 = 0.06272897
        end
    else
        if input[4] >= 1.55 then
            var5 = 0.009899145
        else
            var5 = -0.19659369
        end
    end
    return softmax({0.5 + var0 + var1, 0.5 + var2 + var3, 0.5 + var4 + var5})
end
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
