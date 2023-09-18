import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from automation_project.scraper.scrape import scraper, scraper_social_for_business_email
from automation_project.detailsextraction.extractor import extract
from automation_project.mongo_util import MongoUtil
from autoproject.logger import ClickClickLogger


custom_logger = ClickClickLogger()

@csrf_exempt
def scrape_and_store(request):
    try:
        content = request.GET.get('content')
        url = f"https://www.google.com/localservices/prolist?g2lbs=AP8S6ENVYaPlUqcpp5HFvzYE-khspk5ZxM7UvCPm_mrThLHuOOuoVhvujWM4YXtq4ZMQsSh1MG2ABSTirzgWdxto0NPXtv1pZWmQ6kYBduBDBF9QJC4dd9HZd4niObLIbzEuBxwPcxvE&hl=en-NP&gl=np&cs=1&ssta=1&oq={content}&src=2&sa=X&q={content}&ved=0CAUQjdcJahgKEwjg8IiHroyBAxUAAAAAHQAAAAAQ4wI&scp=ChdnY2lkOnJlYWxfZXN0YXRlX2FnZW5jeRIAGgAqDEVzdGF0ZSBBZ2VudA%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D"
        if request.method == "POST":
            scraped_data = scraper(url)
            details = []
            for i, data in enumerate(scraped_data):
                scraped_data[i] = extract(data)
                scrape_data_with_email = scraped_data[i]
                scrape_data_with_email["Company Email"] = ""
                if scraped_data[i]['Company location'] != None:
                    facebook_search_term = scraped_data[i]['Company name'] + " " + scraped_data[i]['Company location']
                else:
                    facebook_search_term = scraped_data[i]['Company name']
                scrape_data_with_email["Company Email"] = scraper_social_for_business_email(facebook_search_term)
                details.append(scrape_data_with_email)
                break
            data = {
                "data": details
            }
            return_data = data
            save = MongoUtil().insert_data(details, content)
            custom_logger.log(f'Database save status"\t{save}', logging.INFO)
            
            final_response = {}
            final_response["data"] = []
            for scrapped_item in return_data["data"]:
                scrapped_item.pop("_id")
                final_response["data"].append(scrapped_item)
            return JsonResponse(final_response)
        else:
            custom_logger.log(f'Database save status\t{save}', logging.ERROR)
            return JsonResponse({"error": "Invalid request method"})
    except Exception as e:
        custom_logger.log(f'Database save status"\t{str(e)}', logging.ERROR)
        return JsonResponse({"error": "Something went wrong"})
    