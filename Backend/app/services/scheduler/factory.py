from typing import Callable

from .base_cron import BaseCronJob, CronJobRegistry
class CronJobFactory:
    """Factory class for dynamically registering cron jobs."""
    # delcare a callback variable type
    add_cron_job: Callable[[Callable], None] = None

    @classmethod
    def register_jobs(cls):
        """Dynamically registers all cron jobs from the registry."""
        for job_cls in CronJobRegistry.get_registered_jobs():
            job_instance = job_cls()  # Create instance
            interval = job_instance.interval  # 🔥 Fetch interval dynamically

            if interval:
                cls.add_cron_job(job_instance.run, trigger="interval", seconds=interval)
                print(f"[CronJobFactory] Registered '{job_instance.name}' every {interval} seconds.")
            else:
                print(f"[CronJobFactory] Warning: No interval set for {job_instance.name}.")

    @classmethod
    def set_add_cron_job(cls, add_cron_job: Callable[[Callable], None]):
        """Set the add_cron_job callback."""
        cls.add_cron_job = add_cron_job
        print(f"[CronJobFactory] add_cron_job callback set.")
