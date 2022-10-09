function score(input)
    local ml = {}
    if input[13] <= 9.845000267028809 then
        if input[6] <= 6.959500074386597 then
            if input[7] <= 96.20000076293945 then
                ml.var0 = 25.093162393162395
            else
                ml.var0 = 50.0
            end
        else
            ml.var0 = 38.074999999999996
        end
    else
        if input[13] <= 15.074999809265137 then
            ml.var0 = 20.518439716312056
        else
            ml.var0 = 14.451282051282046
        end
    end
    if input[13] <= 9.650000095367432 then
        if input[6] <= 7.437000036239624 then
            if input[8] <= 1.47284996509552 then
                ml.var1 = 50.0
            else
                ml.var1 = 26.7965317919075
            end
        else
            ml.var1 = 44.21176470588236
        end
    else
        if input[13] <= 17.980000495910645 then
            ml.var1 = 19.645652173913035
        else
            ml.var1 = 12.791919191919195
        end
    end
    return (ml.var0 + ml.var1) * 0.5
end
