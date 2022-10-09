function score(input)
    local ml = {}
    if input[3] >= 2.45 then
        ml.var0 = -0.21995015
    else
        ml.var0 = 0.4302439
    end
    if input[3] >= 2.45 then
        ml.var1 = -0.19691855
    else
        ml.var1 = 0.29493433
    end
    if input[3] >= 2.45 then
        if input[4] >= 1.75 then
            ml.var2 = -0.20051816
        else
            ml.var2 = 0.36912444
        end
    else
        ml.var2 = -0.21512198
    end
    if input[3] >= 2.45 then
        if input[3] >= 4.8500004 then
            ml.var3 = -0.14888482
        else
            ml.var3 = 0.2796613
        end
    else
        ml.var3 = -0.19143805
    end
    if input[4] >= 1.6500001 then
        ml.var4 = 0.40298507
    else
        if input[3] >= 4.95 then
            ml.var4 = 0.21724138
        else
            ml.var4 = -0.21974029
        end
    end
    if input[3] >= 4.75 then
        if input[4] >= 1.75 then
            ml.var5 = 0.28692952
        else
            ml.var5 = 0.06272897
        end
    else
        if input[4] >= 1.55 then
            ml.var5 = 0.009899145
        else
            ml.var5 = -0.19659369
        end
    end
    return softmax({0.5 + ml.var0 + ml.var1, 0.5 + ml.var2 + ml.var3, 0.5 + ml.var4 + ml.var5})
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
