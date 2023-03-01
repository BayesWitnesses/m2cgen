module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision :: var0
        double precision :: var1
        double precision :: score
        if (input(13) > 9.725000000000003d0) then
            if (input(13) > 16.205000000000002d0) then
                var0 = 21.71499740307178d0
            else
                var0 = 22.322292901846218d0
            end if
        else
            if (input(6) > 7.418000000000001d0) then
                var0 = 24.75760617150803d0
            else
                var0 = 23.02910423871904d0
            end if
        end if
        if (input(6) > 6.837500000000001d0) then
            if (input(6) > 7.462000000000001d0) then
                var1 = 2.0245964808123453d0
            else
                var1 = 0.859548540618913d0
            end if
        else
            if (input(13) > 14.365d0) then
                var1 = -0.7009440524656984d0
            else
                var1 = 0.052794864734003494d0
            end if
        end if
        score = var0 + var1
        return
    end function score
end module Model
