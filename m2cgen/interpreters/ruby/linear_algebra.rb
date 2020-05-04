def add_vectors(v1, v2)
    v1.zip(v2).map { |x, y| x + y }
end
def mul_vector_number(v1, num)
    v1.map { |i| i * num }
end
