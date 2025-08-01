use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Customer{
    pub customerNumber: i64,
    pub customerName: String,
    pub contactFirstName: Option<String>,
    pub contactLastName: Option<String>,
    pub phone: Option<String>,
    pub addressLine1: Option<String>,
    pub addressLine2: Option<String>,
    pub city: Option<String>,
    pub state: Option<String>,
    pub postalCode: Option<String>,
    pub country: String,
    pub salesRepEmployeeNumber: Option<i64>,
    pub credLimit: Option<f64>
}


#[pyfunction]
fn filter_customers(
        customer_json: String,
        country: Option<String>,
        limit: Option<usize>
    )->PyResult<String>{

        let  customers:Result<Vec<Customer>,_> = serde_json::from_str(&customer_json);
        
        match customers{
            Ok(mut customers)=>{
                if let Some(c) = country{
                    customers.retain(|cust| cust.country ==c);
                }

                if let Some(lim) = limit{
                    customers.truncate(lim);
                }

                let result = serde_json::to_string(&customers)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("error: {}", e)))?;

                Ok(result)
            }
            Err(_)=>{
                Err(PyErr::new::<pyo3::exceptions::PyValueError,_>("invalid json format"))
            }
        }
    }


#[pymodule]
fn rust_filter(py:Python, m:&PyModule)->PyResult<()>{
    m.add_function(wrap_pyfunction!(filter_customers, m)?)?;
    Ok(())
}

