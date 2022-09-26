function score(input)
    if input[4] <= 0.75 then
        var0 = {1.0, 0.0, 0.0}
    else
        if input[3] <= 4.75 then
            var0 = {0.0, 1.0, 0.0}
        else
            if input[3] <= 5.049999952316284 then
                if input[4] <= 1.75 then
                    var0 = {0.0, 0.8333333333333334, 0.16666666666666666}
                else
                    var0 = {0.0, 0.08333333333333333, 0.9166666666666666}
                end
            else
                var0 = {0.0, 0.0, 1.0}
            end
        end
    end
    if input[4] <= 0.800000011920929 then
        var1 = {1.0, 0.0, 0.0}
    else
        if input[1] <= 6.25 then
            if input[3] <= 4.8500001430511475 then
                var1 = {0.0, 0.9487179487179487, 0.05128205128205128}
            else
                var1 = {0.0, 0.0, 1.0}
            end
        else
            if input[4] <= 1.550000011920929 then
                var1 = {0.0, 0.8333333333333334, 0.16666666666666666}
            else
                var1 = {0.0, 0.02564102564102564, 0.9743589743589743}
            end
        end
    end
    return mul_vector_number(add_vectors(var0, var1), 0.5)
end
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
