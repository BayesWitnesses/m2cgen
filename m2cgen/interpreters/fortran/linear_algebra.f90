function add_vectors(v1, v2) result(res)
    implicit none
    double precision, dimension(:), intent(in) :: v1, v2
    double precision, dimension(size(v1)) :: res
    integer :: i

    do i = 1, size(v1)
        res(i) = v1(i) + v2(i)
    end do

end function add_vectors

function mul_vector_number(v1, num) result(res)
    implicit none
    double precision, dimension(:), intent(in) :: v1
    double precision, intent(in) :: num
    double precision, dimension(size(v1)) :: res
    integer :: i

    do i = 1, size(v1)
        res(i) = v1(i) * num
    end do

end function mul_vector_number
