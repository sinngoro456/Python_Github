import Query

class ReserveQuery(Query):
        def __init__(date,time,type,number,table) -> None:
            super().__init__(date,time,type)
            self.number = number
            self.table = table