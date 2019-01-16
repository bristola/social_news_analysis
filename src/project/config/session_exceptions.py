class NoSessionFoundException(Exception):

    def __init__(self):
        message = "There is no active session to add content. Please create a session using create_session() first."
        Exception.__init__(self, message)

class SessionExistsException(Exception):

    def __init__(self):
        message = "A session already exists. Please end the session with end_session() before creating a new one."
        Exception.__init__(self, message)
