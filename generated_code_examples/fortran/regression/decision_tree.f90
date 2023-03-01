module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision :: var0
        double precision :: score
        if (input(13) <= 9.724999904632568d0) then
            if (input(6) <= 7.437000036239624d0) then
                if (input(8) <= 1.4849499464035034d0) then
                    var0 = 50.0d0
                else
                    var0 = 26.681034482758605d0
                end if
            else
                var0 = 44.96896551724139d0
            end if
        else
            if (input(13) <= 16.085000038146973d0) then
                var0 = 20.284353741496595d0
            else
                var0 = 14.187142857142863d0
            end if
        end if
        score = var0
        return
    end function score
end module Model
