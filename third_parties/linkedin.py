import os
from http.client import responses

import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url, mock: bool = False):
    """Scrape information from LinkedIn profile,
    Manually scrape the information from the LinkedIm profile"""

    if mock:
        print("mock")
        linkedin_profile_url='https://gist.githubusercontent.com/Rushik-Ghuntala/d61bd84ede28bb8c8bc937692b40df0d/raw/79cff93721398fa2e5cdb71f9d5e8a54254fe6fc/rushik-ghuntala.json'
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
        print("response",response)
    else:
        print("else")
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )

    data = response.json()
    print("data1",data)

    # below logic is for removing empty fields from data's json
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    print("data2",data)
    return data

if __name__== '__main__':
    scrape_linkedin_profile(
        linkedin_profile_url='https://www.linkedin.com/in/rushik-ghuntala-4a165222a/', mock=True
    )