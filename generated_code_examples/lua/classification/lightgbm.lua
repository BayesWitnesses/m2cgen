function score(input)
    if input[3] > 3.1500000000000004 then
        var0 = -1.1986122886681099
    else
        if input[2] > 3.35 then
            var0 = -0.8986122886681098
        else
            var0 = -0.9136122886681098
        end
    end
    if input[3] > 3.1500000000000004 then
        if input[3] > 4.450000000000001 then
            var1 = -0.09503010837903424
        else
            var1 = -0.09563272415214283
        end
    else
        if input[2] > 3.35 then
            var1 = 0.16640323607832397
        else
            var1 = 0.15374604217339707
        end
    end
    if input[3] > 1.8 then
        if input[4] > 1.6500000000000001 then
            var2 = -1.2055899476674514
        else
            var2 = -0.9500445227622534
        end
    else
        var2 = -1.2182214705715104
    end
    if input[4] > 0.45000000000000007 then
        if input[4] > 1.6500000000000001 then
            var3 = -0.08146437273923739
        else
            var3 = 0.14244886188108738
        end
    else
        if input[3] > 1.4500000000000002 then
            var3 = -0.0950888159264695
        else
            var3 = -0.09438233722389686
        end
    end
    if input[4] > 1.6500000000000001 then
        if input[3] > 5.3500000000000005 then
            var4 = -0.8824095771015287
        else
            var4 = -0.9121126703829481
        end
    else
        if input[3] > 4.450000000000001 then
            var4 = -1.1277829563828181
        else
            var4 = -1.1794405099157212
        end
    end
    if input[3] > 4.750000000000001 then
        if input[3] > 5.150000000000001 then
            var5 = 0.16625543464258166
        else
            var5 = 0.09608601737074281
        end
    else
        if input[1] > 4.950000000000001 then
            var5 = -0.09644547407948921
        else
            var5 = -0.08181864271444342
        end
    end
    return softmax({var0 + var1, var2 + var3, var4 + var5})
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
