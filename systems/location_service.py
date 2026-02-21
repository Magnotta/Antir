from typing import List, Dict, Any


class Locality:
    def __init__(self, name: str, description: str = "", data: Dict[str, Any] | None = None):
        self.name = name
        self.description = description
        self.data = data or {}
        self.paths: List[Path] = []

    def connect_to(self, other: "Locality", **path_kwargs) -> Path:
        path = Path(self, other, **path_kwargs)
        self.paths.append(path)
        other.paths.append(path)
        return path

    def neighbors(self) -> List["Locality"]:
        return [path.other(self) for path in self.paths]

    def __repr__(self):
        return f"<Locality {self.name}>"


class Path:
    def __init__(
        self,
        a: "Locality",
        b: "Locality",
        *,
        distance: float | None = None,
        travel_time: float | None = None,
        description: str = "",
        data: Dict[str, Any] | None = None,
    ):
        if a is b:
            raise ValueError("A path must connect two different localities.")
        self.a = a
        self.b = b
        self.distance = distance
        self.description = description
        self.data = data or {}

    def other_end(self, locality: "Locality") -> "Locality":
        if locality is self.a:
            return self.b
        if locality is self.b:
            return self.a
        raise ValueError("Locality is not connected to this path.")

    def __repr__(self):
        return f"<Path {self.a.name} ↔ {self.b.name}>"
