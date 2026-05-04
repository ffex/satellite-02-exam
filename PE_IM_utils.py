# ==========================================================
# FILE: PE_IM_utils.py
# ==========================================================
"""
Shared constants and helper functions for the satellite domain.
"""

# ----------------------------------------------------------
# DIRECTIONS
# ----------------------------------------------------------
DIRECTIONS = [
    "N", "NE", "E", "SE",
    "S", "SW", "W", "NW"
]


def rotate_left(pos):
    """Rotate counterclockwise."""
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i - 1) % len(DIRECTIONS)]


def rotate_right(pos):
    """Rotate clockwise."""
    i = DIRECTIONS.index(pos)
    return DIRECTIONS[(i + 1) % len(DIRECTIONS)]


# ----------------------------------------------------------
# ACTION COSTS
# ----------------------------------------------------------
COST_ROTATE = 1
COST_TAKEPIC = 2
COST_SEND = 2

# ----------------------------------------------------------
# PHOTO FORMATS AND MEMORY SIZES
# ----------------------------------------------------------
# SD photos occupy 3 units, HD photos occupy 10 units.
PHOTO_SIZE_SD = 3
PHOTO_SIZE_HD = 10
PHOTO_SIZES = {
    "SD": PHOTO_SIZE_SD,
    "HD": PHOTO_SIZE_HD,
}

# ----------------------------------------------------------
# MEMORY LIMITS
# ----------------------------------------------------------
MAX_PHOTOS = 2
MAX_MEMORY_CAPACITY = 15


def normalize_photo_quality(quality):
    """Normalize a photo quality label to its canonical form."""
    if quality is None:
        return None
    q = str(quality).upper()
    if q not in PHOTO_SIZES:
        raise ValueError(f"Invalid photo quality: {quality}")
    return q


def photo_size(quality):
    """Return the memory size of a photo quality."""
    q = normalize_photo_quality(quality)
    return PHOTO_SIZES[q]


def memory_usage(memory):
    """
    Compute how much memory is used by the current photo list.
    Each item must be a tuple of the form (object_name, quality).
    """
    return sum(photo_size(quality) for _, quality in memory)


def can_store_photo(memory, quality):
    """
    Check whether a new photo can be stored while respecting both limits:
    - maximum number of photos
    - maximum memory capacity
    """
    return len(memory) < MAX_PHOTOS and memory_usage(memory) + photo_size(quality) <= MAX_MEMORY_CAPACITY
