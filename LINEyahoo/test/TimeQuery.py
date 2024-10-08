class Query:
    def __init__(number, table, capacity, date, time, type) -> None:
        super().__init__(date)
        self.date = date
        self.time = time
        self.type = type
