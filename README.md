<samp>Testing rust based library in python integrating rust for the cause:</samp>

# How to do ?
0. Install this sample data provided on [MySQL Sample Database (ZIP)](https://www.mysqltutorial.org/wp-content/uploads/2023/10/mysqlsampledatabase.zip)
0.1 unzip it, and  import into your local mysql db where you will be connecting it to FASTapi program-> 
``mysql -u root -p  < unzipedsampledb_path``
note: default is classicmodels database so use that accordingly on the program!

1. create a rust library folder by ``cargo new --lib rust_filter --vcs none`` 
with the following dependencies:
```
[dependencies]
pyo3 = { version = "0.18", features = ["extension-module"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

2. Created the library to be used on python for the imports using the maturin by running ``maturin develop``

3. On the main python file there is the dependencies I used ``requirements.txt`` and import the library that was created by maturin for using the specific logic for filteration and using wrapping up on api fastAPI based, and created one python only api there for data filteration on the ``main.py``

4. Run the program `uvicorn main:app --reload`

5. Check the api using postman or anything in this case i used a general CURL command for Testing:
- python `curl "http://localhost:8000/customers_python/?country=USA"`
- rust_library_with ``curl "http://localhost:8000/customers_rust/?country=USA"`` 

## why was it done?
1. for scaling cause rust can handle big data more securely and fast than python slop however in the low data python might seem slightly faster due to python+overhead on the rust library imported on python itself, [dll and  so is handled by maturin directly]
2. using multiple programming language for more flexibility and code quality


