defmodule Model do
    @compile {:inline, read: 2}
    defp read(bin, pos) do
        <<_::size(pos)-unit(64)-binary, value::float, _::binary>> = bin
        value
    end
    defp list_to_binary(list) do
        for i <- list, into: <<>>, do: <<i::float>>
    end
    defp binary_to_list(binary) do
        for <<f::float <- binary>>, do: f
    end
    def score(input) do
        input = list_to_binary(input)
        func0 = fn ->
            cond do (read(input,3)) <= (0.75) ->
                <<1.0::float, 0.0::float, 0.0::float>>
            true ->
                cond do (read(input,2)) <= (4.75) ->
                    <<0.0::float, 1.0::float, 0.0::float>>
                true ->
                    cond do (read(input,2)) <= (5.049999952316284) ->
                        cond do (read(input,3)) <= (1.75) ->
                            <<0.0::float, 0.8333333333333334::float, 0.16666666666666666::float>>
                        true ->
                            <<0.0::float, 0.08333333333333333::float, 0.9166666666666666::float>>
                        end
                    true ->
                        <<0.0::float, 0.0::float, 1.0::float>>
                    end
                end
            end
        end
        func1 = fn ->
            cond do (read(input,3)) <= (0.800000011920929) ->
                <<1.0::float, 0.0::float, 0.0::float>>
            true ->
                cond do (read(input,0)) <= (6.25) ->
                    cond do (read(input,2)) <= (4.8500001430511475) ->
                        <<0.0::float, 0.9487179487179487::float, 0.05128205128205128::float>>
                    true ->
                        <<0.0::float, 0.0::float, 1.0::float>>
                    end
                true ->
                    cond do (read(input,3)) <= (1.550000011920929) ->
                        <<0.0::float, 0.8333333333333334::float, 0.16666666666666666::float>>
                    true ->
                        <<0.0::float, 0.02564102564102564::float, 0.9743589743589743::float>>
                    end
                end
            end
        end
        result = mul_vector_number(add_vectors(func0.(), func1.()), 0.5)
        binary_to_list(result)
    end
defp add_vectors(v1, v2) do
  v1_list = for <<f::float <- v1>>, do: f
  v2_list = for <<f::float <- v2>>, do: f
  for {a,b} <- Enum.zip(v1_list, v2_list), into: <<>>, do: <<(a+b)::float>>
end

defp mul_vector_number(v1, num) do
  for <<f::float <- v1>>, into: <<>>, do: <<(f * num)::float>>
end
end
