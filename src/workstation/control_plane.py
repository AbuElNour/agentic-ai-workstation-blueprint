from dataclasses import dataclass


@dataclass
class Node:
    name: str
    endpoint: str
    capacity: int
    healthy: bool = True
    active_requests: int = 0


class ModelRouter:
    """Routes work to a healthy node and records recovery decisions."""

    def __init__(self, nodes: list[Node]):
        self.nodes = nodes
        self.trace: list[dict] = []

    def route(self, required_capacity: int = 1) -> Node | None:
        candidates = [
            node
            for node in self.nodes
            if node.healthy and node.capacity >= required_capacity
        ]
        if not candidates:
            self.trace.append({"step": "route.failed", "reason": "no healthy capacity"})
            return None
        selected = sorted(candidates, key=lambda node: (node.active_requests, -node.capacity, node.name))[0]
        selected.active_requests += 1
        self.trace.append({"step": "route.selected", "node": selected.name})
        return selected

    def mark_unhealthy(self, name: str) -> None:
        node = next(node for node in self.nodes if node.name == name)
        node.healthy = False
        self.trace.append({"step": "health.failed", "node": name})

    def recover(self, name: str) -> None:
        node = next(node for node in self.nodes if node.name == name)
        node.healthy = True
        node.active_requests = 0
        self.trace.append({"step": "health.recovered", "node": name})

