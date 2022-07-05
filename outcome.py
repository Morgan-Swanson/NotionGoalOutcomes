import datetime as dt


class Outcome:

    def __init__(self, o):
        self.name = o['properties']['Name']['title'][0]['plain_text']
        self.id = o['id']
        self.start = o['created_time'].split('T')[0]
        try:
            self.end = o['properties']['End Date']['date']['start']
        except TypeError:
            self.end = None
        try:
            self.field = o['properties']['Tracker']['rich_text'][0]['plain_text']
        except IndexError:
            self.field = None
        try:
            self.operation = o['properties']['Metric']['select']['name']
        except TypeError:
            self.operation = None
        self.argument = o['properties']['Argument']['number']
        self.status = o['properties']['Status']['status']['name']
        self.progress = None


    def calculate(self, data):
        # Check that we have the necessary parameters
        if self.field and self.operation and self.status == 'Underway' and self.end:
            # Filter data based on date interval
            data = data.loc[self.start: self.end]
            # Caclulate result
            if self.operation == 'Count':
                self.progress = data[self.field].sum()
            if self.operation == 'Count Greater Than' and self.argument:
                self.progress = (data[self.field] > self.argument).sum()
        return self


    def push(self, notion):
        if self.progress:
            notion.pages.update(
                **{
                    "page_id": self.id,
                    "properties": {
                        "Completed": {
                            "number": int(self.progress)
                        },
                        "Last Update": {
                            "date": {
                                "start": dt.date.today().strftime('%Y-%m-%d')
                            }
                        }
                    }
                }
            )
            return self
        else:
            pass


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
