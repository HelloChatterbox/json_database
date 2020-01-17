class InvalidItemID(ValueError):
    """ ItemID is invalid """


class DatabaseNotCommitted(FileNotFoundError):
    """ Database has not been saved in yet """
