import json

from .control_plane import ModelRouter, Node


def main():
    router = ModelRouter(
        [
            Node("inference-a", "http://192.0.2.10:8080", 8),
            Node("inference-b", "http://192.0.2.20:8080", 4),
        ]
    )
    first = router.route(6)
    router.mark_unhealthy(first.name)
    second = router.route(2)
    print(json.dumps({"first": first.name, "failover": second.name, "trace": router.trace}, indent=2))


if __name__ == "__main__":
    main()

