import socket


class InetClient(BaseClient):
    def __init__(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        self.server = (host, port)
        super().__init__(timeout=60, buffer=1024)
        super().connect(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)


if __name__ == "__main__":
    cli = InetClient()
    cli.send()
