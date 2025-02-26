from abc import ABC, abstractmethod
from utils.Config_loader import Config
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgress.config import getSession
from typing import Dict, Type
from utils.singleton import singleton

class BaseCronJob(ABC):
    """Abstract base class for all cron jobs."""

    __config_file__ = "./server/config_files/config.yaml"  # Default config file (can be overridden)

    def __init__(self, name: str, config_section: str, config_keys: list[str]):
        """
        Args:
            name (str): The job's unique name.
            config_section (str): The YAML config section to retrieve.
            config_keys (list[str]): The specific keys to retrieve from the section.
        """
        self.name = name
        self.config_section = config_section
        self.config_keys = config_keys
        self.config = self.load_config()
        self.interval = self.config.get(config_keys[0], 60)

    def load_config(self):
        """Loads job-specific configuration from YAML."""
        return Config.get_property(self.__config_file__, self.config_section, self.config_keys)

    @abstractmethod
    async def run(self, session: AsyncSession):
        """Job execution logic (to be overridden)."""
        pass

class CronJobRegistry:
    """Singleton storage for all registered cron jobs."""
    _jobs: Dict[str, Type[BaseCronJob]] = {}

    @classmethod
    def register(cls, job_cls: Type[BaseCronJob], name: str):
        """Registers a cron job class dynamically."""
        job_name = name
        if job_name not in cls._jobs:
            cls._jobs[job_name] = job_cls
            print(f"[CronJobRegistry] Registered job: {job_name}")

    @classmethod
    def get_registered_jobs(cls) -> list[Type[BaseCronJob]]:
        """Returns all registered cron job classes."""
        return list(cls._jobs.values())

def register_cron_job(name: str):
    """Decorator factory to auto-register cron jobs in the registry."""
    def decorator(cls: Type) -> Type:
        CronJobRegistry.register(cls, name)
        return cls  # Return the class unchanged
    return decorator