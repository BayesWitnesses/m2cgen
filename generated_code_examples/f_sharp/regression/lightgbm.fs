let score (input : double list) =
    let func0 =
        if input.[12] > 9.725000000000003 then
            if input.[12] > 16.205000000000002 then
                21.71499740307178
            else
                22.322292901846218
        else
            if input.[5] > 7.418000000000001 then
                24.75760617150803
            else
                23.02910423871904
    let func1 =
        if input.[5] > 6.837500000000001 then
            if input.[5] > 7.462000000000001 then
                2.0245964808123453
            else
                0.859548540618913
        else
            if input.[12] > 14.365 then
                -0.7009440524656984
            else
                0.052794864734003494
    func0 + func1
