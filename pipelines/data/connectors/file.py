"""Define data connector to interact with files."""

from pathlib import Path
from typing import Self

import pandas as pd

from pipelines.data.connectors.base import BaseConnector


class FileConnector(BaseConnector):
    """Define data connector to interact with files."""

    def __init__(self: Self) -> None:
        """Initialize data connector."""
        super().__init__()

    def read_dataframe(
        self: Self,
        name: str,
        **kwargs: dict,
    ) -> pd.DataFrame:
        """Read DataFrame.

        :param name: Name of data object to read from.
        :return: Retrieved DataFrame.
        """
        if "format" in kwargs:
            name = f"{name}.{kwargs['format']}"
        file_path = Path(name)

        if "path" in kwargs:
            file_path = str(kwargs["path"]) / file_path
        return pd.read_csv(file_path)

    def write_dataframe(
        self: Self,
        name: str,
        df: pd.DataFrame,
        **kwargs: dict,
    ) -> None:
        """Write DataFrame.

        :param name: Name of data object to write to.
        :param df: DataFrame to write.
        """
        if "format" in kwargs:
            name = f"{name}.{kwargs['format']}"

        file_path = Path(name)
        if "path" in kwargs:
            file_path = str(kwargs["path"]) / file_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        return df.to_csv(file_path, index=False)
