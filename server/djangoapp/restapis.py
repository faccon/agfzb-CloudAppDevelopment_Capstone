import os
import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load env
load_dotenv()

NLU_API_KEY = os.getenv('NLU_API_KEY')
NLU_URL = os.getenv('NLU_URL')


def get_request(url, api_key, nluText, dealer_Id, **kwargs):
    # Defining payload for url
    payload = {'dealerId': dealer_Id}
    print("GET from {} ".format(url))

    if api_key:
        print('in apikey')
        params = dict()
        params["text"] = nluText
        params["features"] = {
            "sentiment": {},
        }
        params["return_analyzed_text"] = ''

        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth('apikey', api_key))
    else:
        # no authentication GET
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def post_request(url, json_payload, **kwargs):

    response = requests.post(url, json=json_payload)

    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, None, None, None)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            if 'id' in dealer:
                dealer_doc = dealer
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function


def get_dealer_reviews_from_cf(url, dealerId):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    reviews = []
    # Call get_request with a URL parameter
    json_result = get_request(url, None, None, dealerId)

    if json_result:
        # Get the row list in JSON as dealers
        DealerReviews = json_result['docs']
        # DealerReviews = json.dumps(Dr)
        # For each dealer object
        # print(type(Dr))
        # for k,v in DealerReviews.items():
        #     print()
        # print(DealerReviews[0]['id'])
        for review in DealerReviews['docs']:
            review_doc = review
            if 'purchase_date' not in review:
                review_doc['purchase_date'] = ''
            # Create a CarDealer object with values in `doc` object
            deale_review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                            review=review_doc["review"], purchase_date=review_doc[
                                                "purchase_date"], car_make=review_doc["car_make"],
                                            car_model=review_doc["car_model"],
                                            car_year=review_doc["car_year"], id=review_doc["id"], sentiment=analyze_review_sentiments(review_doc["review"]))
            reviews.append(deale_review_obj)

    return reviews

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text


def analyze_review_sentiments(dealerreview):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    print(NLU_API_KEY)
    response = get_request(NLU_URL, NLU_API_KEY, dealerreview, None)
    return response['sentiment']['document']['label']
