import datetime

class Log:
    def __init__(self, id, username, action, description,
                 suspicious='No', seen='No'):
        self.id = id
        self.username = username
        self.action = action
        self.description = description
        self.suspicious = suspicious
        self.seen = seen            
        self.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')  
