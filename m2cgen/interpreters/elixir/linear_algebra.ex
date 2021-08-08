defp add_vectors(v1, v2) do
  v1_list = for <<f::float <- v1>>, do: f
  v2_list = for <<f::float <- v2>>, do: f
  for {a,b} <- Enum.zip(v1_list, v2_list), into: <<>>, do: <<(a+b)::float>>
end

defp mul_vector_number(v1, num) do
  for <<f::float <- v1>>, into: <<>>, do: <<(f * num)::float>>
end
