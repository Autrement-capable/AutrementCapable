from pathlib import Path
from typing import Any, Dict, List
from os import getenv
import re

from yaml import safe_load, YAMLError

from ..utils.patterns import singleton

class Config:
    """Singleton class that loads and stores configuration files as dictionaries."""

    _config_data: Dict[str, Dict[str, Any]] = {}  # Stores loaded YAML configs
    __default_config_file__ = "./config/config.yaml"  # Default config file

    @classmethod
    def load_config(cls, file_path: str) -> Dict[str, Any]:
        """
        Loads a YAML configuration file and stores it in the class dictionary.

        Args:
            file_path (str): Path to the YAML configuration file.

        Returns:
            Dict[str, Any]: Parsed YAML content.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the YAML content is invalid.
        """
        file_path = str(Path(file_path).resolve())  # Normalize path
        if file_path in cls._config_data:
            return cls._config_data[file_path]  # Return cached config

        if not Path(file_path).exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                yaml_content = safe_load(file) or {}
                cls._eval_expressions(yaml_content)  # Evaluate expressions
                cls._convert_time_units(yaml_content)  # Convert time units
                cls._config_data[file_path] = yaml_content  # Cache config
                return yaml_content
        except YAMLError as e:
            raise ValueError(f"Invalid YAML format in {file_path}: {e}")

    @classmethod
    def get_property(cls, file_path: str | None, section: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        Retrieves specific configuration properties from a loaded YAML file.

        Args:
            file_path (str): Path to the YAML configuration file.
            section (str): The top-level section in the YAML file.
            keys (List[str], optional): A list of specific sub-properties to retrieve.

        Returns:
            Dict[str, Any]: The requested config values.

        Raises:
            KeyError: If the section or keys do not exist.
        """
        if not file_path:
            file_path = cls.__default_config_file__  # Use default config file if not provided
        config = cls.load_config(file_path)  # Load config if not already loaded
        section_data = config.get(section, {})

        if keys:
            result = {}
            for key in keys:
                if key in section_data:
                    result[key] = section_data[key]
                else:
                    raise KeyError(f"Key '{key}' not found in section '{section}'")
            return result
        return section_data  # Return the entire section if no keys provided

    @staticmethod
    def _eval_expressions(config: Dict[str, Any]):
        """
        Evaluate expressions in string values, e.g., "5 * 1024 * 1024"

        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        # Pattern for simple arithmetic expressions (digits, operators +, -, *, /, and whitespace)
        expr_pattern = re.compile(r'^\s*\d+(\s*[\+\-\*\/]\s*\d+)+\s*$')

        def process_value(value):
            if isinstance(value, str) and expr_pattern.match(value):
                try:
                    # Evaluate simple arithmetic expression
                    return eval(value, {"__builtins__": {}}, {})
                except:
                    # If evaluation fails, return the original string
                    return value
            return value

        def traverse_and_eval(d: Dict[str, Any]):
            """Recursively traverse dictionary and evaluate expressions."""
            for key, value in list(d.items()):  # Create a list to avoid dict size change during iteration
                if isinstance(value, dict):
                    traverse_and_eval(value)
                elif isinstance(value, list):
                    d[key] = [process_value(item) if not isinstance(item, dict) else traverse_and_eval(item) 
                             for item in value]
                else:
                    d[key] = process_value(value)
            return d

        traverse_and_eval(config)

    @staticmethod
    def _convert_time_units(config: Dict[str, Any]):
        """
        Converts time-related fields in the config to seconds.

        Args:
            config (Dict[str, Any]): Configuration dictionary.
        """
        time_units = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400, "months": 2592000}

        def convert_time(value):
            if isinstance(value, dict):
                total_seconds = sum(time_units.get(unit, 0) * count for unit, count in value.items() if unit in time_units)
                return total_seconds if total_seconds > 0 else value  # If no valid time keys, return original
            return value

        def traverse_and_convert(d: Dict[str, Any]):
            """Recursively traverse the dictionary and convert time fields."""
            for key, value in d.items():
                if isinstance(value, dict):
                    d[key] = convert_time(value)  # Convert time-related fields
                    traverse_and_convert(value)  # Recurse deeper

        traverse_and_convert(config)