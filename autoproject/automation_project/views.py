import logging, json, os
import pandas as pd 
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from automation_project.scraper.scrape import scraper, scraper_social_for_business_email
from automation_project.detailsextraction.extractor import extract
from autoproject.logger import ClickClickLogger


custom_logger = ClickClickLogger()
@csrf_exempt
def scrape_and_store(request):
    # channel_layer = get_channel_layer()
    redirect("/")
    if os.path.exists("success/to_export.csv"): 
        os.remove("success/to_export.csv")
    if os.path.exists("success/temp.csv"): 
        os.remove("success/temp.csv")
    redirect('/')
    custom_logger.log(f'Triggered endpoint', logging.INFO)
    try:
        if request.method == "POST":
            limit = 0
            print(request.POST)
            content = request.POST.get("content")
            try:
                if not request.POST.get("limit"): 
                    limit = 0
                else:
                    limit =  int(request.POST.get("limit", 0))
            except Exception as e: 
                limit = 0
            url = f"https://www.google.com/localservices/prolist?g2lbs=AP8S6ENVYaPlUqcpp5HFvzYE-khspk5ZxM7UvCPm_mrThLHuOOuoVhvujWM4YXtq4ZMQsSh1MG2ABSTirzgWdxto0NPXtv1pZWmQ6kYBduBDBF9QJC4dd9HZd4niObLIbzEuBxwPcxvE&hl=en-NP&gl=np&cs=1&ssta=1&oq={content}&src=2&sa=X&q={content}&ved=0CAUQjdcJahgKEwjg8IiHroyBAxUAAAAAHQAAAAAQ4wI&scp=ChdnY2lkOnJlYWxfZXN0YXRlX2FnZW5jeRIAGgAqDEVzdGF0ZSBBZ2VudA%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D"
            scraped_data = scraper(url)

            details = []
            for i, data in enumerate(scraped_data):
                if (limit !=0) and ((i+1)>limit):
                    break
                custom_logger.log(f'Total scraps : {i}', logging.INFO)
    
                scraped_data[i] = extract(data)
                scrape_data_with_email = scraped_data[i]
                scrape_data_with_email["Company Email"] = ""
                if scraped_data[i]['Company location'] != None:
                    facebook_search_term = scraped_data[i]['Company name'] + " " + scraped_data[i]['Company location']
                else:
                    facebook_search_term = scraped_data[i]['Company name']
                scrape_data_with_email["Company Email"] = scraper_social_for_business_email(facebook_search_term)

                details.append(scrape_data_with_email)
            data = {
                "data": details
            }
            return_data = data
            #save = MongoUtil().insert_data(details, content)
            #custom_logger.log(f'Database save status"\t{save}', logging.INFO)
            
            final_response = {}
            final_response["data"] = []
            for scrapped_item in return_data["data"]:
                #scrapped_item.pop("_id")
                final_response["data"].append(scrapped_item)
                
            # write json as csv
            df = pd.DataFrame(final_response["data"])
            rows_list = []
            for index, row in df.iterrows():
                row_dict = row.to_dict()  # Convert the row to a dictionary if needed
                rows_list.append(list(row_dict.values()))
            df.to_csv("success/temp.csv", index=False)
        
            
            render(request, 'index.html', {'data': rows_list})
            return redirect('/')
        else:
            #custom_logger.log(f'Database save status\t{save}', logging.ERROR)
            return redirect('')
    except Exception as e:
        custom_logger.log(f'Database save status"\t{str(e)}', logging.ERROR)
        return JsonResponse({"error": e})
    
    
from django.shortcuts import render
@csrf_exempt
def default_view(request=None):
    import os
    # Your logic to retrieve data or perform any operations
    # csv_file_path = 'success/temp.csv'  # Update with your CSV file path
    # with open(csv_file_path, 'r', newline='') as file:
    #     reader = csv.reader(file)
    df = pd.DataFrame()
    if os.path.exists("success/to_export.csv"): 
        df = pd.read_csv("success/to_export.csv")
    elif os.path.exists("success/temp.csv"):  
        df = pd.read_csv("success/temp.csv")
    else : 
        return render(request, 'index.html', {"data" : []})
    # data = [x if x else ["Untraced"] for x in list(reader)]
    final_data = []
    for x in df.itertuples(index=False):
        data = []
        data.append(x[0])
        for vals in x[1:] : 
            if vals: 
                data.append(vals)
            else: 
                data.append("Untraced")
                
        final_data.append(data)
    return render(request, 'index.html', {"data" : final_data})


from django.http import FileResponse


@csrf_exempt
def download(request):
    file = "success/to_export.csv"
    fileopen = open(file, "rb")
    response = FileResponse(fileopen)
    response['Content-Disposition'] = 'attachment; filename="success/to_export.csv"'
    # os.remove("success/to_export.csv")
    return response
    
@csrf_exempt 
def process_data(request):
    data  =[]
    selected_rows = request.POST.get('selected_rows')
    # Process the selected rows here
    headers = ["Company name" ," Company number" , "Company location" ,"Company Email"]
    if selected_rows and eval(selected_rows): 
        data = eval(selected_rows)
        print(data)
        df = pd.DataFrame(data, columns = headers)
        df.to_csv("success/to_export.csv", index=False)
    else : 
        if os.path.exists("success/to_export.csv"): 
            os.remove("success/to_export.csv")
        if os.path.exists("success/temp.csv"): 
            os.remove("success/temp.csv")
    #     df = pd.DataFrame()
    #     df.to_csv("success/temp.csv", index=False)
    #     df.to_csv("success/to_export.csv", index=False)
    return redirect("/")

import csv 
def display_csv(request):
    csv_file_path = 'success/temp.csv'  # Update with your CSV file path
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return render(request, 'index.html', {'data': data})