
from pyhive import hive

class HiveAudioDataStore:
    def __init__(self, host: str, port: int, database: str, table_name: str):
        self.connection = hive.Connection(host=host, port=port, database=database)
        self.table_name = table_name

    def query_audio_data(self, audio_file_id: str, start_time: str, end_time: str) -> bytes:
        query = f"""
        SELECT audio_data
        FROM {self.table_name}
        WHERE audio_file_id = '{audio_file_id}' AND timestamp >= '{start_time}' AND timestamp <= '{end_time}'
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    def close(self):
        self.connection.close()