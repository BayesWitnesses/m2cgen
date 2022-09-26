function score(input)
    if input[13] > 9.725000000000003 then
        if input[13] > 16.205000000000002 then
            var0 = 21.71499740307178
        else
            var0 = 22.322292901846218
        end
    else
        if input[6] > 7.418000000000001 then
            var0 = 24.75760617150803
        else
            var0 = 23.02910423871904
        end
    end
    if input[6] > 6.837500000000001 then
        if input[6] > 7.462000000000001 then
            var1 = 2.0245964808123453
        else
            var1 = 0.859548540618913
        end
    else
        if input[13] > 14.365 then
            var1 = -0.7009440524656984
        else
            var1 = 0.052794864734003494
        end
    end
    return var0 + var1
end
