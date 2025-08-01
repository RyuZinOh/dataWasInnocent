import json
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import Session, session
from typing import Optional
import rust_filter
import time
from decimal import Decimal
from sqlalchemy.sql.functions import count  

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:safal123@localhost/classicmodels"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
customers = Table("customers", metadata, autoload_with=engine)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  
    raise TypeError(" notserializable")

@app.get("/customers_rust/")
def get_customers_rust(
    country: Optional[str] = Query(None, description="filter by country"),
    limit: int = Query(10, gt=0, le=100, description="(1-100)")
):

    start_db = time.perf_counter()

    with Session(engine) as session:
        stmt = select(customers)
        if country:
            stmt = stmt.where(customers.c.country == country)
        stmt = stmt.limit(limit)
        result = session.execute(stmt).mappings().all()
        data = [dict(row) for row in result]

    end_db = time.perf_counter()
    db_duration_ms = (end_db - start_db) * 1000  # 
    print(f"SWL Query took {db_duration_ms:.2f} ms for country={country} limit={limit} by using rust library")

    data_json = json.dumps(data, default=decimal_default)  
    filtered_json = rust_filter.filter_customers(data_json, country, limit)

    filtered_data = json.loads(filtered_json)

    return {
        "count": len(filtered_data),
        "results": filtered_data,
        "timing": {
            "sql_query_ms": db_duration_ms
        }
    }





def filter_customers_python(c_j: str, country:Optional[str] = None)->str:
    try:
        customers = json.loads(c_j)
    except json.JSONDecodeError:
        raise ValueError("invalid format")

    if country is not None:
        customers = [cust for cust  in customers if cust.get('country')==country]
    
    try:
        r_j = json.dumps(customers)

    except (TypeError, ValueError) as e:
        raise ValueError(f"error: {e}")

    return r_j


# //using python only

@app.get("/customers_python/")
def get_customers_python(country:Optional[str] =  None):
    with Session(engine) as s:
        stmt = select(customers)
        res = s.execute(stmt).mappings().all()
        data = [dict(row) for row in res]


    data_json = json.dumps(data, default=decimal_default) 


    start = time.perf_counter()
    filtered_json = filter_customers_python(data_json, country)
    end = time.perf_counter()

    filtered_data  = json.loads(filtered_json)


    print(f"python took {(end-start)*1000:.2f}ms")



    return{

            "count": len(filtered_data),
            "results": filtered_data,
            "timing":{
                "filter_python_ms":(end-start) * 1000,
            }
    }











