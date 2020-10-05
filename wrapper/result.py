class Summary:
    def __init__(self):
        self._processed = []
        self._errors = []

    def add_processed(self, file_name):
        self._processed.append(file_name)

    def add_error(self, error_file):
        self._errors.append(error_file)

    def __str__(self) -> str:
        report = f'''
Summary:
\tProcessed files: {len(self._processed)}
\tError files: {len(self._errors)}
'''
        if self._errors:
            report += f'''
Errors:
{self._errors}
'''
        return report
