module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input

        double precision, dimension(3) :: score
        score(:) = (/ 9.700311953536998d0 + input(1) * -0.4128360473754751d0 + input(2) * 0.9680426131053453d0 + input(3) * -2.498310603183548d0 + input(4) * -1.0723230787022542d0, 2.1575759475871163d0 + input(1) * 0.5400806228605453d0 + input(2) * -0.3245383349519669d0 + input(3) * -0.2034493200950831d0 + input(4) * -0.9338183426196143d0, -11.857887901124615d0 + input(1) * -0.12724457548509432d0 + input(2) * -0.6435042781533917d0 + input(3) * 2.7017599232786216d0 + input(4) * 2.006141421321863d0 /)
        return
    end function score
end module Model
