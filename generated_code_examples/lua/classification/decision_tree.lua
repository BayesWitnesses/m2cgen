function score(input)
    if input[3] <= 2.449999988079071 then
        var0 = {1.0, 0.0, 0.0}
    else
        if input[4] <= 1.75 then
            if input[3] <= 4.950000047683716 then
                if input[4] <= 1.6500000357627869 then
                    var0 = {0.0, 1.0, 0.0}
                else
                    var0 = {0.0, 0.0, 1.0}
                end
            else
                var0 = {0.0, 0.3333333333333333, 0.6666666666666666}
            end
        else
            var0 = {0.0, 0.021739130434782608, 0.9782608695652174}
        end
    end
    return var0
end
