class Role:
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    LIBRARIAN = "LIBRARIAN"
    MEMBER = "MEMBER"

    ALL = [SUPER_ADMIN, ADMIN, LIBRARIAN, MEMBER]


class BookStatus:
    AVAILABLE = "AVAILABLE"
    ISSUED = "ISSUED"
    LOST = "LOST"
    DAMAGED = "DAMAGED"
    RESERVED = "RESERVED"

    ALL = [AVAILABLE, ISSUED, LOST, DAMAGED, RESERVED]


class TransactionStatus:
    ISSUED = "ISSUED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"

    ALL = [ISSUED, RETURNED, OVERDUE]


class QRType:
    BOOK = "book"
    MEMBER = "member"


# ID prefixes
BOOK_PREFIX = "BOOK"
MEMBER_PREFIX = "MEM"
TRANSACTION_PREFIX = "TRX"

# Padding length for numeric part of IDs
ID_PADDING = 6