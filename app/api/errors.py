class ActionError(Exception):
    def __init__(self, errors, message):
        self.errors = errors
        self.message = message

not_found = ActionError(
    {'paste': 'no paste with given id was found'},
    'paste not found'
)
