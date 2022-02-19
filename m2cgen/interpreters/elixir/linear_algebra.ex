defp add_vectors(v1_list, v2_list) do
  for {a,b} <- Enum.zip(v1_list, v2_list), do: a+b
end

defp mul_vector_number(v1, num) do
  for i <- v1, do: i * num
end
