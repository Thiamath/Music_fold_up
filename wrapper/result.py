class Summary:
    def __init__(self):
        self._moved = []
        self._errors = []

    def add_moved(self, file_name):
        self._moved.append(file_name)

    def add_error(self, error_file):
        self._errors.append(error_file)

    def __str__(self) -> str:
        return f'''
        Summary:
        \tMoved files: {len(self._moved)}
        \tError files: {len(self._errors)}
        '''
