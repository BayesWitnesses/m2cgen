function score(input)
    local ml = {}
    if input[13] >= 9.725 then
        if input[13] >= 19.23 then
            ml.var0 = 3.5343752
        else
            ml.var0 = 5.5722494
        end
    else
        if input[6] >= 6.941 then
            ml.var0 = 11.1947155
        else
            ml.var0 = 7.4582143
        end
    end
    if input[13] >= 5.1549997 then
        if input[13] >= 15.0 then
            ml.var1 = 2.8350503
        else
            ml.var1 = 4.8024607
        end
    else
        if input[6] >= 7.406 then
            ml.var1 = 10.0011215
        else
            ml.var1 = 6.787523
        end
    end
    return 0.5 + ml.var0 + ml.var1
end
