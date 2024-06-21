# Or your preferred Airflow version
FROM apache/airflow:2.4.3  

# setthe airflow user
USER ${AIRFLOW_UID:-1000} 

RUN pip install confluent-kafka
