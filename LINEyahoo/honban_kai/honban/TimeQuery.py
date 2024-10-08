import Query

class TimeQuery(Query):
        def __init__(number,table,capacity,date,time,type) -> None:
            super().__init__(date,time,type)