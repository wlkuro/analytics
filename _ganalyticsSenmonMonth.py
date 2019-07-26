# -*- coding: utf-8 -*-
from google.cloud import bigquery
import sys
import requests
import json
import pandas as pd
from pprint import PrettyPrinter


def query_list(path):
    args = sys.argv
    client = bigquery.Client()
    #max(if(customDimensions.index=87, customDimensions.value,null)) as region
    query_job = client.query("""
        WITH row_data AS (
            SELECT *
            FROM `189615029.ga_sessions_*`
            WHERE
              _TABLE_SUFFIX BETWEEN 
              FORMAT_DATE("%Y%m%d", DATE_TRUNC(DATE_SUB(CURRENT_DATE('Asia/Tokyo'), INTERVAL 1 MONTH), MONTH))
              AND FORMAT_DATE("%Y%m%d", DATE_SUB(DATE_TRUNC(CURRENT_DATE('Asia/Tokyo'), MONTH), INTERVAL 1 DAY))
        )
        SELECT
          COUNT(DATE(TIMESTAMP_SECONDS(visitStartTime + CAST((hits.time / 1000) AS int64)), 'Asia/Tokyo')) AS pageviews,
          hits.page.pageTitle AS pageTitle,
          hits.page.pagePath AS pagePath,
          (SELECT value FROM UNNEST(hits.customDimensions) WHERE index = 87) AS region
        FROM
          row_data,
          UNNEST(row_data.hits) hits
        WHERE
          REGEXP_CONTAINS(hits.page.pagePath, r"^{param}[a-z-.]*$")
        GROUP BY pagePath,pageTitle,region;
    """.format(param = path).strip())
    results = query_job.result()  # Waits for job to complete.
    list_df = pd.DataFrame({},columns=['title','pageviews','pagePath','region'] )
    for row in results:
      tmp_se = pd.Series( [row.pageTitle, row.pageviews, row.pagePath, row.region], index=list_df.columns )
      list_df = list_df.append( tmp_se, ignore_index=True )
    return list_df;

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
  kyoten_id=("spk","aoj","sdj","ibr","tyo","kij","mmj","ngo","toy","hkr","szo","osa","okj","izo","hij","ubj","tak","myj","kcz","fuk","ngs","kmj","oit","kmi","koj","oka")
  kyoten_name=("北海道発","青森発","東北発","北関東発","関東発","新潟発","富山発","石川・福井発","長野発","名古屋発","静岡発","関西発","山陰発","岡山発","広島発","山口発","香川・徳島発","松山発","高知発","福岡発","長崎発","熊本発","大分発","宮崎発","鹿児島発","沖縄発")
  path_i=('/asia/','/china/','/china/beijing/','/china/shanghai/','/china/dalian/','/china/hangzhou/','/china/chengdu/','/china/xian/','/china/jiuzhaigou/','/china/tibet/','/korea/','/korea/seoul/','/korea/busan/','/korea/jeju/','/taiwan/','/taiwan/taroko/','/taiwan/sunmoonlake/','/taiwan/taipei/','/taiwan/taichung/','/taiwan/tainan/','/taiwan/kaohsiung/','/hongkong/','/macau/','/thailand/','/thailand/chiangmai/','/thailand/bangkok/','/thailand/phuket/','/singapore/','/malaysia/','/philippines/','/asian-beach/','/vietnam/','/vietnam/hanoi/','/vietnam/halon/','/vietnam/hoian/','/vietnam/hochiminh/','/cambodia/','/laos/','/india/','/nepal/','/myanmar/','/srilanka/','/maldives/','/europe/','/france/','/france/arles/','/france/paris/','/france/montstmichel/','/france/loire/','/france/nice/','/france/provence/','/france/bordeaux/','/france/lyon/','/uk/','/uk/london/','/uk/lakedistrict/','/uk/cotswolds/','/uk/edinburgh/','/uk/stratford-upon-avon/','/ireland/','/italy/','/italy/roma/','/italy/venezia/','/italy/milano/','/italy/firenze/','/italy/napoli/','/italy/capri/','/italy/alberobello/','/italy/amalfi/','/italy/pisa/','/italy/sicilia/','/italy/matera/','/malta/','/greece/','/swiss/','/swiss/interlaken/','/swiss/grindelwald/','/swiss/stmoritz/','/swiss/geneve/','/swiss/zurich/','/swiss/basel/','/swiss/jungfrau/','/swiss/kleine-scheidegg/','/swiss/montblanc/','/germany/','/germany/rothenburg/','/germany/frankfurt/','/germany/neuschwanstein/','/germany/heidelberg/','/germany/berlin/','/germany/munchen/','/holland/','/holland/amsterdam/','/holland/keukenhof/','/holland/kinderdijk/','/holland/haag/','/belgium/','/belgium/antwerp/','/belgium/gent/','/belgium/bruxelles/','/belgium/bruges/','/spain/','/spain/barcelona/','/spain/madrid/','/spain/toledo/','/spain/mijas/','/spain/la-mancha/','/spain/segovia/','/spain/sevilla/','/spain/granada/','/spain/santiago/','/portugal/','/portugal/lisbon/','/portugal/porto/','/northern-eur/','/denmark/','/norway/','/sweden/','/finland/','/iceland/','/russia/','/east-eur/','/austria/','/czech/','/slovakia/','/hungary/','/poland/','/rumania/','/bulgaria/','/croatia-slovenia/','/austria/wien/','/austria/salzburg/','/austria/salzkammergut/','/austria/graz/','/austria/innsbruck/','/austria/hallstatt/','/baltic/','/africa/','/egypt/','/egypt/abusimbel/','/egypt/alexandria/','/egypt/cairo/','/egypt/giza/','/egypt/sinai/','/egypt/luxor/','/tunisia/','/morocco/','/south-africa/','/kenya/','/botswana/','/jinbabue-zanvia/','/tanzania/','/middle-east/','/turkey/','/turkey/istanbul/','/turkey/cappadocia/','/turkey/troy/','/turkey/pamukkale/','/jordan/','/israel/','/uae/','/iran/','/uzbekistan/','/north-america/','/america/','/america/la/','/america/lasvegas/','/america/grandcanyon/','/america/sanfrancisco/','/america/yosemite/','/america/seattle/','/america/ny/','/america/boston/','/america/orlando/','/america/alaska/','/america/yellowstone/','/america/washington/','/america/houston/','/canada/','/canada/vancouver/','/canada/rockies/','/canada/niagara/','/canada/toronto/','/canada/quebec/','/canada/montreal/','/canada/pei/','/canada/yellowknife/','/canada/victoria/','/canada/laurentian/','/latin-america/','/mexico/','/brazil/','/ecuador/','/venezuela/','/peru/','/peru/machupicchu/','/peru/nazca/','/peru/cuzco/','/peru/puno/','/peru/lima/','/argentina/','/oceania/','/australia/','/australia/sydney/','/australia/goldcoast/','/australia/cairns/','/australia/great-barrier-reef/','/australia/uluru/','/australia/melbourne/','/australia/perth/','/australia/tasmania/','/newzealand/','/newzealand/auckland/','/newzealand/queenstown/','/newzealand/christchurch/','/newzealand/teanau/','/newzealand/mountcook/','/newzealand/milfordsound/','/s-pacific/','/tahiti/','/newcaledonia/','/fiji/','/hawaii/','/hawaii/oahu/','/hawaii/bigisland/','/hawaii/maui/','/hawaii/kauai/','/micronesia/','/guam/','/saipan/')
  path_d=('/hokkaido/','/hokkaido/sapporo/','/hokkaido/hakodate/','/hokkaido/otaru/','/hokkaido/asahiyama/','/hokkaido/noboribetsu/','/hokkaido/furano/','/hokkaido/wakkanai/','/hokkaido/rishiri/','/hokkaido/shiretoko/','/hokkaido/niseko/','/hokkaido/obihiro/','/hokkaido/kushiro/','/tohoku/','/tohoku/aomori/','/tohoku/hirosaki/','/tohoku/oirase/','/tohoku/aomori-city/','/tohoku/tsugaru/','/tohoku/shirakami-aomori/','/tohoku/hachinohe/','/tohoku/hakkoda/','/tohoku/iwate/','/tohoku/tsunagi-oshuku/','/tohoku/appi/','/tohoku/ichinoseki/','/tohoku/hanamaki/','/tohoku/morioka/','/tohoku/hachimantai/','/tohoku/hiraizumi/','/tohoku/miyagi/','/tohoku/shiogama/','/tohoku/miyagi-zao/','/tohoku/akiu/','/tohoku/matsushima/','/tohoku/sendai/','/tohoku/naruko/','/tohoku/akita/','/tohoku/kakunodate/','/tohoku/tamagawa/','/tohoku/akita-chity/','/tohoku/towada/','/tohoku/oga/','/tohoku/tazawako/','/tohoku/nyuto/','/tohoku/shirakami-akita/','/tohoku/yamagata/','/tohoku/yamagata-city/','/tohoku/yamagata-zao/','/tohoku/sakata-tsuruoka/','/tohoku/tendo/','/tohoku/ginzan/','/tohoku/yonezawa/','/tohoku/fukushima/','/tohoku/aizuwakamatsu/','/tohoku/koriyama/','/tohoku/goshikinuma/','/tohoku/inawashiro/','/tohoku/bandai/','/tohoku/fukushima-city/','/kanto/','/kanto/ibaraki/','/kanto/tochigi/','/kanto/gunma/','/kanto/saitama/','/kanto/tokyo/','/kanto/chiba/','/kanto/kanagawa/','/chubu-hokuriku/','/chubu-hokuriku/yamanashi/','/chubu-hokuriku/niigata/','/chubu-hokuriku/toyama/','/chubu-hokuriku/takaoka/','/chubu-hokuriku/kurobe/','/chubu-hokuriku/toyama-city/','/chubu-hokuriku/alpine-route/','/chubu-hokuriku/ishikawa/','/chubu-hokuriku/kaga/','/chubu-hokuriku/kanazawa/','/chubu-hokuriku/yamanaka/','/chubu-hokuriku/noto/','/chubu-hokuriku/wakura/','/chubu-hokuriku/fukui/','/chubu-hokuriku/nagano/','/chubu-hokuriku/karuizawa/','/chubu-hokuriku/kamikochi/','/chubu-hokuriku/norikura/','/chubu-hokuriku/hakuba/','/chubu-hokuriku/yatsugatake/','/chubu-hokuriku/gifu/','/chubu-hokuriku/okuhida/','/chubu-hokuriku/gero/','/chubu-hokuriku/takayama/','/chubu-hokuriku/sekigahara/','/chubu-hokuriku/sirakawago/','/chubu-hokuriku/hida/','/chubu-hokuriku/shizuoka/','/chubu-hokuriku/izu/','/chubu-hokuriku/fuji/','/chubu-hokuriku/numazu-mishima/','/chubu-hokuriku/shizuoka-city/','/chubu-hokuriku/atami/','/chubu-hokuriku/hamamatsu/','/chubu-hokuriku/aichi/','/chubu-hokuriku/mie/','/chubu-hokuriku/ise/','/chubu-hokuriku/kumano/','/chubu-hokuriku/shima/','/chubu-hokuriku/futami-toba/','/kinki/','/kinki/shiga/','/kinki/kyoto/','/kinki/osaka/','/kinki/nara/','/kinki/hyogo/','/kinki/wakayama/','/sanin-sanyo/','/sanin-sanyo/tottori/','/sanin-sanyo/shimane/','/sanin-sanyo/okayama/','/sanin-sanyo/hiroshima/','/sanin-sanyo/yamaguchi/','/shikoku/','/shikoku/tokushima/','/shikoku/kagawa/','/shikoku/ehime/','/shikoku/kochi/','/kyushu/','/kyushu/fukuoka/','/kyushu/dazaifu/','/kyushu/hakata/','/kyushu/yanagawa/','/kyushu/fukuoka-city/','/kyushu/kita-kyushu/','/kyushu/saga/','/kyushu/imari-arita/','/kyushu/ureshino/','/kyushu/yoshinogari/','/kyushu/saga-city/','/kyushu/karatsu-yobuko/','/kyushu/takeo/','/kyushu/nagasaki/','/kyushu/iki/','/kyushu/unzen/','/kyushu/goto/','/kyushu/sasebo/','/kyushu/hirado/','/kyushu/nagasaki-city/','/kyushu/tsushima/','/kyushu/shimabara/','/kyushu/kumamoto/','/kyushu/aso/','/kyushu/kikuchi/','/kyushu/kumamoto-city/','/kyushu/kurokawa/','/kyushu/amakusa/','/kyushu/hitoyoshi/','/kyushu/oita/','/kyushu/oita-city/','/kyushu/yufuin/','/kyushu/hita/','/kyushu/beppu/','/kyushu/yabakei/','/kyushu/miyazaki/','/kyushu/miyazaki-city/','/kyushu/takachiho/','/kyushu/aoshima/','/kyushu/nichinan/','/kyushu/kagoshima/','/kyushu/amami/','/kyushu/yakushima/','/kyushu/sakurajima/','/kyushu/ibusuki/','/kyushu/kagoshima-city/','/kyushu/tanegashima/','/kyushu/chiran/','/kyushu/kirishima/','/okinawa/','/okinawa/naha/','/okinawa/onna/','/okinawa/nago/','/okinawa/churaumi/','/okinawa/ishigaki/','/okinawa/iriomote/','/okinawa/miyako/','/okinawa/yonaguni/')
  
  
  args = sys.argv

  analytics_arr_i = pd.DataFrame({},columns=['title','pageviews','pagePath','region'],dtype=str)
  for z in range(len(path_i)):
    temp = query_list(path_i[z])
    analytics_arr_i = pd.concat([analytics_arr_i, temp])
  
  for x in range(len(kyoten_id)):
    data_arr = analytics_arr_i[analytics_arr_i['region'].str.startswith(unicode(kyoten_name[x], 'utf-8'),na=False)]
    temp_data_arr = data_arr.groupby(['title','region']).agg({"pageviews": "sum"})
    data_arr = pd.merge(data_arr, temp_data_arr, on='title')
    data_arr = data_arr[data_arr['pagePath'].str.endswith('/')]
<<<<<<< HEAD
    append_json_to_file(data_arr.to_json(orient='records',force_ascii=True),'/home/mac/nuxt-express-template/static/data/inter/month/'+args[1]+kyoten_id[x]+'.json')
=======
    append_json_to_file(data_arr.to_json(orient='records',force_ascii=True),'./static/data/inter/month/'+args[1]+kyoten_id[x]+'.json')
>>>>>>> 6edfc938cd9b20ae6ce4065f8d67da831bf8789b

  analytics_arr_d = pd.DataFrame({},columns=['title','pageviews','pagePath','region'],dtype=str)
  for z in range(len(path_d)):
    temp = query_list(path_d[z])
    analytics_arr_d = pd.concat([analytics_arr_d, temp])
  
  for x in range(len(kyoten_id)):
    data_arr = analytics_arr_d[analytics_arr_d['region'].str.startswith(unicode(kyoten_name[x], 'utf-8'),na=False)]
    temp_data_arr = data_arr.groupby(['title','region']).agg({"pageviews": "sum"})
    data_arr = pd.merge(data_arr, temp_data_arr, on='title')
    data_arr = data_arr[data_arr['pagePath'].str.endswith('/')]
<<<<<<< HEAD
    append_json_to_file(data_arr.to_json(orient='records',force_ascii=True),'/home/mac/nuxt-express-template/static/data/dome/month/'+args[1]+kyoten_id[x]+'.json')
=======
    append_json_to_file(data_arr.to_json(orient='records',force_ascii=True),'./static/data/dome/month/'+args[1]+kyoten_id[x]+'.json')
>>>>>>> 6edfc938cd9b20ae6ce4065f8d67da831bf8789b
      
      
      
      
      
      
