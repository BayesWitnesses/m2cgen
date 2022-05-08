def score(input)
    if input[12] >= 9.725
        if input[12] >= 19.23
            var0 = 3.5343752
        else
            var0 = 5.5722494
        end
    else
        if input[5] >= 6.941
            var0 = 11.1947155
        else
            var0 = 7.4582143
        end
    end
    if input[12] >= 5.1549997
        if input[12] >= 15.0
            var1 = 2.8350503
        else
            var1 = 4.8024607
        end
    else
        if input[5] >= 7.406
            var1 = 10.0011215
        else
            var1 = 6.787523
        end
    end
    0.5 + (var0 + var1)
end
