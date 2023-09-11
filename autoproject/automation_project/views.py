from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from automation_project.scraper.scrape import scraper
from automation_project.detailsextraction.extractor import extract

@csrf_exempt
def scrape_and_store(request):
    content = request.GET.get('content')
    url = f"https://www.google.com/localservices/prolist?g2lbs=AP8S6ENVYaPlUqcpp5HFvzYE-khspk5ZxM7UvCPm_mrThLHuOOuoVhvujWM4YXtq4ZMQsSh1MG2ABSTirzgWdxto0NPXtv1pZWmQ6kYBduBDBF9QJC4dd9HZd4niObLIbzEuBxwPcxvE&hl=en-NP&gl=np&cs=1&ssta=1&oq={content}&src=2&sa=X&q={content}&ved=0CAUQjdcJahgKEwjg8IiHroyBAxUAAAAAHQAAAAAQ4wI&scp=ChdnY2lkOnJlYWxfZXN0YXRlX2FnZW5jeRIAGgAqDEVzdGF0ZSBBZ2VudA%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D"
    if request.method == "POST":
        scraped_data = scraper(url)
        details = []
        for i, data in enumerate(scraped_data):
            scraped_data[i] = extract(data)
            details.append(scraped_data[i])
        data = {
            "data": details
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Invalid request method"})
    