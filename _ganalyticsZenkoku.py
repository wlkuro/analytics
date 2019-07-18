from google.cloud import bigquery
import sys
import requests
import json
import pandas as pd
from pprint import PrettyPrinter


def query_list():
    args = sys.argv
    client = bigquery.Client()
    query_job = client.query("""
        WITH row_data AS (
            SELECT *
            FROM `189615029.ga_sessions_*`
            WHERE _TABLE_SUFFIX = FORMAT_DATE("%Y%m%d", DATE_SUB(CURRENT_DATE('Asia/Tokyo'), INTERVAL 1 DAY))
        )
        SELECT
          COUNT(visitId) AS visitCount,
          hits.page.pageTitle AS pageTitle,
          hits.page.pagePath AS pagePath,
          (SELECT value FROM UNNEST(hits.customDimensions) WHERE index = 87) AS region
        FROM
          row_data,
          UNNEST(row_data.hits) hits
        WHERE
          hits.page.pagePath = '{param}'
          
        GROUP BY pagePath,pageTitle,region;
        """.format(param = args[1]).strip())

    results = query_job.result()  # Waits for job to complete.
    list_df = pd.DataFrame({},columns=['title','region','visits','pagePath'] )
    for row in results:
      tmp_se = pd.Series( [row.pageTitle, row.region, row.visitCount, row.pagePath], index=list_df.columns )
      list_df = list_df.append( tmp_se, ignore_index=True )
#    print(list_df.to_json(orient='index',force_ascii=True))
    append_json_to_file(list_df.to_json(orient='records',force_ascii=True),'./static/data/'+args[2]+'/'+args[3]+'/'+args[4]+'.json')

def append_json_to_file(_dict, path_file):
    with open(path_file, 'ab+') as f:
      f.seek(0,2)
      if f.tell() == 0 :
        f.write(json.dumps([_dict]).encode())
      else :
        f.seek(-1,2)
        f.truncate()
        f.write(' , '.encode())
        f.write(json.dumps(_dict).encode())
        f.write(']'.encode())
    return f.close()

if __name__ == '__main__':
    query_list()
