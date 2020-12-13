import json
import heapq
import time
from typing import List, Dict, Tuple, Optional

from models.storage.base import key_type, value_type, user_id_type
from models.storage.exceptions import UserNotFound
from core.config import STORAGE_PATH


class UsersStorage:

    def __init__(self, file_path: str = 'storage'):
        self.file_path = file_path
        self._users_data: Dict[user_id_type, Dict[key_type, value_type]] = {}
        self._ttl_values_heap: List[Tuple[float, user_id_type, key_type]] = []

    def save_data(self, user_id: user_id_type):
        """Save data to disk by user_id"""
        user_data = self._get_data_by_user_id(user_id)
        with open(
                f'{STORAGE_PATH}/{self.file_path}_{user_id}.json',
                'w'
        ) as f:
            json.dump(user_data, f)

    def get_value(self, key: key_type, user_id: user_id_type
                  ) -> Optional[value_type]:
        """Get value by user_id"""
        user_data = self._get_data_by_user_id(user_id)
        return user_data.get(key)

    def set_value(self, key: str, value: value_type, user_id: str,
                  nx: bool = False, xx: bool = False,
                  ttl: Optional[float] = None) -> Optional[value_type]:
        """Set value by user_id"""
        user_data = self._get_data_by_user_id(user_id)
        if nx and key in user_data or xx and key not in user_data:
            return
        if ttl is not None:
            ttl_time = time.time() + ttl
            heapq.heappush(self._ttl_values_heap, (ttl_time, user_id, key))
        user_data[key] = value
        return value

    def delete_values(self, keys: List[str], user_id: str) -> int:
        """Delete values by input keys"""
        user_data = self._get_data_by_user_id(user_id)
        count_deleted_values = 0
        for key in keys:
            if user_data.pop(key, None) is not None:
                count_deleted_values += 1
        return count_deleted_values

    def get_keys(self, user_id: user_id_type) -> List[key_type]:
        return list(self._get_data_by_user_id(user_id))

    def add_user(self, user_id: user_id_type):
        self._users_data[user_id] = {}

    def delete_if_ttl_is_gone(self):
        while (self._ttl_values_heap and
               self._ttl_values_heap[0][0] < time.time()):
            _, user_id, key = heapq.heappop(self._ttl_values_heap)
            user_data = self._users_data.get(user_id)
            if user_data is None:
                continue
            user_data.pop(key, None)

    def _get_data_by_user_id(self, user_id: user_id_type
                             ) -> Dict[key_type, value_type]:
        user_data = self._users_data.get(user_id)
        if user_data is None:
            raise UserNotFound(user_id)
        return user_data
