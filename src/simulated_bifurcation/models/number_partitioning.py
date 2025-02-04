from typing import Dict, List, Union

import torch
from numpy import sum

from ..polynomial import SpinQuadraticPolynomial


class NumberPartitioning(SpinQuadraticPolynomial):

    """
    A solver that separates a set of numbers into two subsets, the
    respective sums of which are as close as possible.
    """

    def __init__(
        self, numbers: list, dtype: torch.dtype = torch.float32, device: str = "cpu"
    ) -> None:
        self.numbers = numbers
        tensor_numbers = torch.tensor(self.numbers, dtype=dtype, device=device).reshape(
            -1, 1
        )
        super().__init__(tensor_numbers @ tensor_numbers.t(), None, None, dtype, device)

    @property
    def partition(self) -> Dict[str, Dict[str, Union[List[int], int, None]]]:
        result = {
            "left": {"values": [], "sum": None},
            "right": {"values": [], "sum": None},
        }
        if self.sb_result is None:
            return result

        i_min = torch.argmin(self(self.sb_result.t())).item()
        best_vector = self.sb_result[:, i_min]

        left_subset = []
        right_subset = []
        for elt in range(len(self)):
            if best_vector[elt].item() > 0:
                left_subset.append(self.numbers[elt])
            else:
                right_subset.append(self.numbers[elt])
        result["left"]["values"] = left_subset
        result["left"]["sum"] = sum(left_subset)
        result["right"]["values"] = right_subset
        result["right"]["sum"] = sum(right_subset)
        return result
