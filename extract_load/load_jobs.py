 
import dlt
import requests
import json

dlt.config["load.truncate_staging_dataset"] = True

params = [{
        "limit": 100, "occupation-field": "X82t_awd_Qyc" #Administration, ekonomi, juridik
    },
    {
        "limit": 100, "occupation-field": "j7Cq_ZJe_GkT" #Bygg och anläggning
    },
    {
        "limit": 100, "occupation-field": "apaJ_2ja_LuF" #Data/IT
    }
]

 
def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status() 
    return json.loads(response.content.decode("utf8"))
 
 
@dlt.resource(table_name= 'raw_jobs', write_disposition="append")
def jobsearch_resource(params):
    for param in params:
        """
        params should include at least:
          - "q": your query
          - "limit": page size (e.g. 100)
          - "occupation-field": the occupation field concept ID
        """
        url = "https://jobsearch.api.jobtechdev.se"
        url_for_search = f"{url}/search"
        limit = param.get("limit", 100)
        offset = 0
    
        while True:
            page_params = dict(param, offset=offset)
            data = _get_ads(url_for_search, page_params)
    
            hits = data.get("hits", [])
            if not hits:
                break
            
            for ad in hits:
                yield ad
    
            if len(hits) < limit or offset > 1900:
                break
            
            offset += limit

@dlt.source
def jobads_source():
    return jobsearch_resource(params) 
 