module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision :: var0
        double precision :: var1
        double precision :: score
        if (input(13) >= 9.725d0) then
            if (input(13) >= 19.23d0) then
                var0 = 3.5343752d0
            else
                var0 = 5.5722494d0
            end if
        else
            if (input(6) >= 6.941d0) then
                var0 = 11.1947155d0
            else
                var0 = 7.4582143d0
            end if
        end if
        if (input(13) >= 5.1549997d0) then
            if (input(13) >= 15.0d0) then
                var1 = 2.8350503d0
            else
                var1 = 4.8024607d0
            end if
        else
            if (input(6) >= 7.406d0) then
                var1 = 10.0011215d0
            else
                var1 = 6.787523d0
            end if
        end if
        score = 0.5d0 + var0 + var1
        return
    end function score
end module Model
