import functools

@total_ordering
class Work():

    def __init__(self, quality, agents):
        self._quality = quality
        self._authors = agents

    @property
    def Quality(self):
        return self._quality

    @property
    def NumberOfAuthors(self):
        return len(self._authors)

    @property
    def Authors(self):
        return self._authors

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.Quality == other.Quality)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.Quality < other.Quality)