module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision :: var0
        double precision :: var1
        double precision :: score
        if (input(13) <= 9.845000267028809d0) then
            if (input(6) <= 6.959500074386597d0) then
                if (input(7) <= 96.20000076293945d0) then
                    var0 = 25.093162393162395d0
                else
                    var0 = 50.0d0
                end if
            else
                var0 = 38.074999999999996d0
            end if
        else
            if (input(13) <= 15.074999809265137d0) then
                var0 = 20.518439716312056d0
            else
                var0 = 14.451282051282046d0
            end if
        end if
        if (input(13) <= 9.650000095367432d0) then
            if (input(6) <= 7.437000036239624d0) then
                if (input(8) <= 1.47284996509552d0) then
                    var1 = 50.0d0
                else
                    var1 = 26.7965317919075d0
                end if
            else
                var1 = 44.21176470588236d0
            end if
        else
            if (input(13) <= 17.980000495910645d0) then
                var1 = 19.645652173913035d0
            else
                var1 = 12.791919191919195d0
            end if
        end if
        score = (var0 + var1) * 0.5d0
        return
    end function score
end module Model
