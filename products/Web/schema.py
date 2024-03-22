from pathlib import Path
from ariadne import make_executable_schema
from Web.queries import query
from Web.types import product_type, datetime_scalar
from Web.mutations import mutation

schema = make_executable_schema(
    (Path(__file__).parent / Path("schema.gql")).read_text(), 
    [query, mutation, datetime_scalar,product_type]
)