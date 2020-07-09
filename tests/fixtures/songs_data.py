from statistics import mean

from munch import Munch

TEST_SONG_DATA = {
    "artist": "The Yousicians",
    "title": "Lycanthropic Metamorphosis",
    "difficulty": 14.6,
    "level": 13,
    "rating": [1, 2, 3, 4, 5],
    "released": "2016-10-26"
}
TEST_SONG_RATING_STATS = Munch(
    lowest=min(TEST_SONG_DATA['rating']),
    highest=max(TEST_SONG_DATA['rating']),
    average=mean(TEST_SONG_DATA['rating'])
)
DEFAULT_INITIAL_VERSION = 0
NON_EXISTING_SONG_ID = 12345
INVALID_VERSION = 'invalid version'
TEST_SONG_DATA_WITHOUT_RATING = {
    "artist": "The Yousicians",
    "title": "Lycanthropic Metamorphosis",
    "difficulty": 14.6,
    "level": 13,
    "rating": [],
    "released": "2016-10-26"
}
TEST_SONG_RATINGS = [1, 2, 3, 4, 5]
INVALID_SONG_RATINGS = ['abc', 0, 6]

INVALID_ARTIST = 123
INVALID_TITLE = 123
INVALID_DIFFICULTY = 'ABC'
INVALID_LEVEL = 'LEVEL'
INVALID_RELEASED = 123
INVALID_SONG_DATA = [
    (TEST_SONG_DATA, 'artist', INVALID_ARTIST),
    (TEST_SONG_DATA, 'title', INVALID_TITLE),
    (TEST_SONG_DATA, 'difficulty', INVALID_DIFFICULTY),
    (TEST_SONG_DATA, 'level', INVALID_LEVEL),
    (TEST_SONG_DATA, 'released', INVALID_RELEASED),
]

TEST_DATASET_SONGS = [
    {
        "artist": "The Yousicians",
        "title": "Lycanthropic Metamorphosis",
        "difficulty": 14.6,
        "level": 13,
        "released": "2016-10-26"
    },
    {
        "artist": "The Yousicians",
        "title": "A New Kennel",
        "difficulty": 9.1,
        "level": 9,
        "released": "2010-02-03"
    },
    {
        "artist": "Mr Fastfinger",
        "title": "Awaki-Waki",
        "difficulty": 15,
        "level": 13,
        "released": "2012-05-11"
    },
    {
        "artist": "The Yousicians",
        "title": "You've Got The Power",
        "difficulty": 13.22,
        "level": 13,
        "released": "2014-12-20"
    },
    {
        "artist": "The Yousicians",
        "title": "Wishing In The Night",
        "difficulty": 10.98,
        "level": 9,
        "released": "2016-01-01"
    },
    {
        "artist": "The Yousicians",
        "title": "Opa Opa Ta Bouzoukia",
        "difficulty": 14.66,
        "level": 13,
        "released": "2013-04-27"
    },
    {
        "artist": "The Yousicians",
        "title": "Greasy Fingers - boss level",
        "difficulty": 2,
        "level": 3,
        "released": "2016-03-01"
    },
    {
        "artist": "The Yousicians",
        "title": "Alabama Sunrise",
        "difficulty": 5,
        "level": 6,
        "released": "2016-04-01"
    },
    {
        "artist": "The Yousicians",
        "title": "Can't Buy Me Skills",
        "difficulty": 9,
        "level": 9,
        "released": "2016-05-01"
    },
    {
        "artist": "The Yousicians",
        "title": "Vivaldi Allegro Mashup",
        "difficulty": 13,
        "level": 13,
        "released": "2016-06-01"
    },
    {
        "artist": "The Yousicians",
        "title": "Babysitting",
        "difficulty": 7,
        "level": 6,
        "released": "2016-07-01"
    }
]

TEST_DATASET_DIFFICULTY_WITH_LEVEL = [
    (1, 0),
    (3, 2.0),
    (6, 6.0),
    (9, 9.7),
    (13, 14.1)
]

DATASET_AVERAGE_DIFFICULTY = 10.3

TEST_SEARCH_RESULTS = [
    ('YOUSICIANS', 10),
    ('yousicians', 10),
    ('awaki-waki', 1)
]

TEST_SEARCH_RESULTS_WITH_PAGESIZE = [
    ('YOUSICIANS', 5, 5, True),
    ('yousicians', 3, 3, True),
    ('awaki-waki', 5, 1, False)
]

TEST_GET_ALL_SONGS_WITH_PAGINATION = [
    (5, 5),
    (3, 3),
    (1, 1),
    (20, 11)
]
