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

COMMON_FIELDS_RULE = f"""
        {COMMON_REACTION_ITEM_FIELDS},
        match_once INTEGER NOT NULL DEFAULT 0,
        priority INTEGER DEFAULT 0
"""

COMMON_CHECKS_RULE = f"""
    CHECK (match_once IN (0, 1))
"""