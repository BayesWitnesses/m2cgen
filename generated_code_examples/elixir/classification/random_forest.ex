defmodule Model do
    @compile {:inline, read: 2}
    defp read(bin, pos) do
        <<_::size(pos)-unit(64)-binary, value::float, _::binary>> = bin
        value
    end
    defp list_to_binary(list) do
        for i <- list, into: <<>>, do: <<i::float>>
    end
    def score(input) do
        input = list_to_binary(input)
        func0 = fn ->
            cond do read(input,3) <= 0.75 ->
                [1.0, 0.0, 0.0]
            true ->
                cond do read(input,2) <= 4.75 ->
                    [0.0, 1.0, 0.0]
                true ->
                    cond do read(input,2) <= 5.049999952316284 ->
                        cond do read(input,3) <= 1.75 ->
                            [0.0, 0.8333333333333334, 0.16666666666666666]
                        true ->
                            [0.0, 0.08333333333333333, 0.9166666666666666]
                        end
                    true ->
                        [0.0, 0.0, 1.0]
                    end
                end
            end
        end
        func1 = fn ->
            cond do read(input,3) <= 0.800000011920929 ->
                [1.0, 0.0, 0.0]
            true ->
                cond do read(input,0) <= 6.25 ->
                    cond do read(input,2) <= 4.8500001430511475 ->
                        [0.0, 0.9487179487179487, 0.05128205128205128]
                    true ->
                        [0.0, 0.0, 1.0]
                    end
                true ->
                    cond do read(input,3) <= 1.550000011920929 ->
                        [0.0, 0.8333333333333334, 0.16666666666666666]
                    true ->
                        [0.0, 0.02564102564102564, 0.9743589743589743]
                    end
                end
            end
        end
        mul_vector_number(add_vectors(func0.(), func1.()), 0.5)
    end
defp add_vectors(v1_list, v2_list) do
  for {a,b} <- Enum.zip(v1_list, v2_list), do: a+b
end

defp mul_vector_number(v1, num) do
  for i <- v1, do: i * num
end
end
