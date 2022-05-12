from datetime import datetime
from typing import Optional

from clepsydra import JobInfo
from clepsydra.api.storage import AsyncStorage, AT


class PostgresStorage(AsyncStorage):
    def mark_run_completed(self, job_id: str, started_at: datetime) -> AT:
        pass

    def mark_started(self, job_id: str, started_at: datetime) -> AT:
        pass

    def save_job(self, job: JobInfo) -> AT:
        pass

    def remove_job(self, job_id: str) -> AT:
        pass

    def schedule_next(self, job_id: str, next_start: datetime) -> AT:
        pass

    async def get_jobs(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
            limit: Optional[int] = None,
    ) -> list[JobInfo]:
        """
        Retrieves jobs with filtering in order of `next_start`
        """
        pass

    async def get_job(self, job_id: str) -> JobInfo:
        pass
