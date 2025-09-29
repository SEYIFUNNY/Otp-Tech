import os
import json
from datetime import datetime, timedelta

class OTPFilter:
    def __init__(self, cache_file='otp_cache.json', expire_minutes=30):
        self.cache_file = cache_file
        self.expire_minutes = expire_minutes
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def _cleanup_expired(self):
        current_time = datetime.now()
        expired_keys = []
        for key, entry in list(self.cache.items()):
            try:
                ts = entry.get('timestamp')
                entry_time = datetime.fromisoformat(ts) if ts else None
                if entry_time is None or (current_time - entry_time > timedelta(minutes=self.expire_minutes)):
                    expired_keys.append(key)
            except Exception:
                expired_keys.append(key)
        for k in expired_keys:
            self.cache.pop(k, None)
        if expired_keys:
            self._save_cache()

    def _generate_key(self, otp_data):
        otp = str(otp_data.get('otp', ''))
        phone = str(otp_data.get('phone', ''))
        service = str(otp_data.get('service', ''))
        return f"{otp}_{phone}_{service}"

    def is_duplicate(self, otp_data):
        self._cleanup_expired()
        key = self._generate_key(otp_data)
        return key in self.cache

    def add_otp(self, otp_data):
        key = self._generate_key(otp_data)
        self.cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'otp': str(otp_data.get('otp', '')),
            'phone': str(otp_data.get('phone', '')),
            'service': str(otp_data.get('service', '')),
        }
        self._save_cache()
