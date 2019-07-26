
from google.cloud import bigquery
import sys
import requests
import pandas as pd
from pprint import PrettyPrinter


def query_list():
    args = sys.argv
    client = bigquery.Client()
    query_job = client.query("""
            WITH row_data AS (
                SELECT *
                FROM `189615029.ga_sessions_*`
            )
            SELECT SUM(totals.visits) AS visits,geoNetwork.region
            FROM row_data, UNNEST(row_data.hits) AS hits
            WHERE hits.page.pagePath = '{param}'
            GROUP BY geoNetwork.region;
        """.format(param = args[1]).strip())

    results = query_job.result()  # Waits for job to complete.
    list_df = pd.DataFrame({},columns=['region','visits'] )
    for row in results:
      tmp_se = pd.Series( [row.region, row.visits ], index=list_df.columns )
      list_df = list_df.append( tmp_se, ignore_index=True )
    print(list_df.to_json(orient='index',force_ascii=True))



def query_stackoverflow():
    args = sys.argv
    client = bigquery.Client()
    query_job = client.query("""
            WITH row_data AS (
                SELECT *
                FROM `189615029.ga_sessions_*`
            )
            SELECT SUM(totals.visits) AS visits,geoNetwork.region
            FROM row_data, UNNEST(row_data.hits) AS hits
            WHERE hits.page.pagePath = '{param}'
            GROUP BY geoNetwork.region;
        """.format(param = args[1]).strip())

        # WHERE EXISTS (
        #     SELECT 1 FROM UNNEST(hits) AS hit
        #     WHERE hit.page.pagePath = '/guide/kanto/');

        # SELECT *
        # FROM `189615029.ga_sessions_20190317`
        # WHERE EXISTS (
        #     SELECT 1 ,count(geoNetwork.region)
        #     FROM UNNEST(hits) AS hit
        #     WHERE hit.page.pagePath = '/kokunai/');

        # hits.page.pagePath = '/kakuyasu/kokunai/' group by geoNetwork.region
        # SELECT
        #   CONCAT(
        #     'https://stackoverflow.com/questions/',
        #     CAST(id as STRING)) as url,
        #   view_count
        # FROM `bigquery-public-data.stackoverflow.posts_questions`
        # WHERE tags like '%google-bigquery%'
        # ORDER BY view_count DESC
        # LIMIT 10""")

    results = query_job.result()  # Waits for job to complete.
    list_df = pd.DataFrame({},columns=['region','visits'] )
    for row in results:
      tmp_se = pd.Series( [row.region, row.visits ], index=list_df.columns )
      list_df = list_df.append( tmp_se, ignore_index=True )
#    pp = PrettyPrinter()
    print(list_df.to_json(orient='index',force_ascii=True))

if __name__ == '__main__':
    query_stackoverflow()
