def score(input)
    if (input[2]) <= (2.45)
        var0 = [1.0, 0.0, 0.0]
    else
        if (input[3]) <= (1.75)
            if (input[2]) <= (4.95)
                if (input[3]) <= (1.6500001)
                    var0 = [0.0, 1.0, 0.0]
                else
                    var0 = [0.0, 0.0, 1.0]
                end
            else
                var0 = [0.0, 0.3333333333333333, 0.6666666666666666]
            end
        else
            var0 = [0.0, 0.021739130434782608, 0.9782608695652174]
        end
    end
    var0
end
