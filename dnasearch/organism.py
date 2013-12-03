class Organism:
    """
    Represents an Organism in the database or given by the user in the query
    file.

    :ivar description: The description of the organism as provided by the
        database.
    :ivar sequence: The genome of the organism as a string.
    :ivar score: The similarity score of the organism if applicable.

    """

    def __init__(self, description, sequence, score = None):
        self.description = description
        self.sequence = sequence
        self.score = score

    def get_string(self):
        return "Organism(description = %s, sequence = %s, score = %s)" % (
            repr(self.description), repr(self.sequence), repr(self.score))

    def __repr__(self):
        return self.get_string()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
