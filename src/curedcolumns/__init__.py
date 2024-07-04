import importlib.metadata

# Load the package version number from the pyproject.toml file
# https://docs.python.org/3/library/importlib.metadata.html
__version__ = importlib.metadata.version('curedcolumns')
"curedcolumns package version"

from curedcolumns.iter_files import iter_files
from curedcolumns.get_s3_parquet_schema import get_s3_parquet_schema
