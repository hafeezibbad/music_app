from typing import Type, List, Tuple, Dict, Any, Union, Optional

from flask_mongoengine import BaseQuerySet
from mongoengine import Document, Q


def paginate_records(
        query_set: Type[BaseQuerySet],
        start: int = 0,
        page_size: int = 10
) -> Tuple[List[Type[Document]], str]:
    # FIXME: This only works for incremental Song_IDs
    all_songs = query_set.filter(Q(song_id__gte=start))[:page_size]
    if not all_songs:
        return [], ''

    last_index = query_set.order_by('-song_id').first().to_json()['song_id']
    next_anchor = ''
    if (start + page_size) < int(last_index):
        # There are more elements, so provide next anchor for other elements
        next_anchor = '?nextId={next_id}&pageSize={page_size}'.format(
            next_id=start + page_size, page_size=page_size
        )

    return all_songs, next_anchor


def get_string_field_filter(
        field_name: str,
        value: Union[int, str],
        strict: bool = False,
        case_sensitive: bool = False
) -> Dict[str, Any]:
    if strict is True:
        return {'{}'.format(field_name): value}

    comparison = "contains" if case_sensitive else "icontains"
    return {'{}__{}'.format(field_name, comparison): value}


def get_int_field_filter(
        field_name: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
) -> Dict[str, Any]:
    _filter = dict()
    _filter["{}__gte".format(field_name)] = min_value
    _filter["{}__lte".format(field_name)] = max_value

    return _filter
