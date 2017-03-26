import time, uuid
from application import bq


def query_from_bigquery(query):
    """Run query into database and return the formatted result."""
    query_results = bq.run_sync_query(query)
    # it allows to use SQL syntax
    query_results.use_legacy_sql = False
    query_results.run()
    # fetch data in row_data
    (row_data, total_rows, page_token) = query_results.fetch_data()
    return row_data


def wait_for_job(job):
    while True:
        job.reload()
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError (job.errors)
            return
        time.sleep(1)


def query_async_from_bigquery(query):
    """Run asynchronous query into database and return the formatted result."""
    query_job = bq.run_async_query(str(uuid.uuid4()),query)
    # it allows to use SQL syntax
    query_job.use_legacy_sql = False
    query_job.begin()
    wait_for_job(query_job)
    query_results = query_job.results()

    # fetch data in row_data
    (row_data, total_rows, page_token) = query_results.fetch_data()
    return row_data
