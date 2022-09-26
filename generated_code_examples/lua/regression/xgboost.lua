function score(input)
    if input[13] >= 9.725 then
        if input[13] >= 19.23 then
            var0 = 3.5343752
        else
            var0 = 5.5722494
        end
    else
        if input[6] >= 6.941 then
            var0 = 11.1947155
        else
            var0 = 7.4582143
        end
    end
    if input[13] >= 5.1549997 then
        if input[13] >= 15.0 then
            var1 = 2.8350503
        else
            var1 = 4.8024607
        end
    else
        if input[6] >= 7.406 then
            var1 = 10.0011215
        else
            var1 = 6.787523
        end
    end
    return 0.5 + var0 + var1
end
