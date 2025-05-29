from dataclasses import dataclass


@dataclass
class Cost:
    input_token: int
    output_token: int
    llm_model_name: str

    def __add__(self, other: "Cost") -> "Cost":
        return Cost(
            input_token=self.input_token + other.input_token,
            output_token=self.output_token + other.output_token,
            llm_model_name=other.llm_model_name,
        )

    @staticmethod
    def zero_cost() -> "Cost":
        return Cost(input_token=0, output_token=0, llm_model_name="")
