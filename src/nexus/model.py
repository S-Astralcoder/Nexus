from dataclasses import dataclass


@dataclass
class ModelBase:
    model : str
    temperature : float | None = None
    top_p : float | None = None


