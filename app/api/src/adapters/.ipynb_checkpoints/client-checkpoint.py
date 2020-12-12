import requests 
class Client: 
    def venue_search(query_params = {'ll': "40.7,-74", "query": "tacos"}):
        client_id = "ALECV5CBBEHRRKTIQ5ZV143YEXOH3SBLAMU54SPHKGZI1ZKE"
        client_secret = "3JX3NRGRS2P0KE0NSKPTMCOZOY4MWUU4M3G33BO4XTRJ15SM"
        date = "20190407"
        auth_params = {'client_id': client_id, 
                   'client_secret': client_secret,
                   'v': date}
        params = auth_params.copy()
        params.update(query_params)
        url = "https://api.foursquare.com/v2/venues/search"
        response = requests.get(url, params)
        return response.json()['response']['venues']