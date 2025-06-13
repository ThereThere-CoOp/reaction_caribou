COMMON_FIELDS = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE,
        label TEXT UNIQUE,
        description TEXT
    """

COMMON_REACTION_ITEM_FIELDS = f"""
        {COMMON_FIELDS},
        scope TEXT,
        parent TEXT
    """