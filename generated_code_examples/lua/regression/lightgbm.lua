function score(input)
    local ml = {}
    if input[13] > 9.725000000000003 then
        if input[13] > 16.205000000000002 then
            ml.var0 = 21.71499740307178
        else
            ml.var0 = 22.322292901846218
        end
    else
        if input[6] > 7.418000000000001 then
            ml.var0 = 24.75760617150803
        else
            ml.var0 = 23.02910423871904
        end
    end
    if input[6] > 6.837500000000001 then
        if input[6] > 7.462000000000001 then
            ml.var1 = 2.0245964808123453
        else
            ml.var1 = 0.859548540618913
        end
    else
        if input[13] > 14.365 then
            ml.var1 = -0.7009440524656984
        else
            ml.var1 = 0.052794864734003494
        end
    end
    return ml.var0 + ml.var1
end
