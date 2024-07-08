import logging
import os
import pandas as pd
from django.shortcuts import redirect, render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from automation_project.scraper.scrape import scraper, scraper_social_for_business_email
from automation_project.detailsextraction.extractor import extract
from autoproject.logger import ClickClickLogger
import csv

custom_logger = ClickClickLogger()

@csrf_exempt
def scrape_and_store(request):
    custom_logger.log('Triggered endpoint', logging.INFO)
    
    try:
        if request.method == "POST":
            temp_file_path = "automation_project/gen_data/temp.csv"
            to_export_file_path = "automation_project/gen_data/to_export.csv"
        
            def clear_csv(file_path):
                if os.path.exists(file_path):
                    with open(file_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([]) 
            
            if os.path.exists(temp_file_path):
                if os.path.getsize(temp_file_path) > 0:
                    try:
                        df_temp = pd.read_csv(temp_file_path)
                        if not df_temp.empty:
                            clear_csv(temp_file_path)
                    except pd.errors.EmptyDataError:
                        pass
            else:
                pd.DataFrame().to_csv(temp_file_path, index=False)

            if os.path.exists(to_export_file_path):
                if os.path.getsize(to_export_file_path) > 0:
                    try:
                        df_export = pd.read_csv(to_export_file_path)
                        if not df_export.empty:
                            clear_csv(to_export_file_path)
                    except pd.errors.EmptyDataError:
                        pass
            else:
                pd.DataFrame().to_csv(to_export_file_path, index=False)
            
            limit = int(request.POST.get("limit", 0))
            content = request.POST.get("content")
            url = f"https://www.google.com/localservices/prolist?g2lbs=AP8S6ENVYaPlUqcpp5HFvzYE-khspk5ZxM7UvCPm_mrThLHuOOuoVhvujWM4YXtq4ZMQsSh1MG2ABSTirzgWdxto0NPXtv1pZWmQ6kYBduBDBF9QJC4dd9HZd4niObLIbzEuBxwPcxvE&hl=en-NP&gl=np&cs=1&ssta=1&oq={content}&src=2&sa=X&q={content}&ved=0CAUQjdcJahgKEwjg8IiHroyBAxUAAAAAHQAAAAAQ4wI&scp=ChdnY2lkOnJlYWxfZXN0YXRlX2FnZW5jeRIAGgAqDEVzdGF0ZSBBZ2VudA%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D"
            scraped_data = scraper(url)
            details = []
            for i, data in enumerate(scraped_data):
                if limit != 0 and i + 1 > limit:
                    break
                custom_logger.log(f'Total scraps : {i}', logging.INFO)
                scraped_data[i] = extract(data)
                scrape_data_with_email = scraped_data[i]
                scrape_data_with_email["Company Email"] = ""
                if scraped_data[i]['Company location'] is not None:
                    facebook_search_term = scraped_data[i]['Company name'] + " " + scraped_data[i]['Company location']
                else:
                    facebook_search_term = scraped_data[i]['Company name']
                scrape_data_with_email["Company Email"] = scraper_social_for_business_email(facebook_search_term)
                details.append(scrape_data_with_email)
            
            data = {"data": details}
            df = pd.DataFrame(data["data"])
            rows_list = [list(row.to_dict().values()) for index, row in df.iterrows()]
            df.to_csv(temp_file_path, index=False)
            
            return render(request, 'index.html', {'data': rows_list})
        else:
            return redirect('/')
    except Exception as e:
        custom_logger.log(f'Error: {str(e)}', logging.ERROR)
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def default_view(request=None):
    try:
        temp_file_path = "automation_project/gen_data/temp.csv"
        to_export_file_path = "automation_project/gen_data/to_export.csv"

        if not os.path.exists(temp_file_path):
            pd.DataFrame().to_csv(temp_file_path, index=False)

        if not os.path.exists(to_export_file_path):
            pd.DataFrame().to_csv(to_export_file_path, index=False)
        
        df = pd.DataFrame()
        if os.path.exists(to_export_file_path) and os.path.getsize(to_export_file_path) > 0:
            df = pd.read_csv(to_export_file_path)
        elif os.path.exists(temp_file_path) and os.path.getsize(temp_file_path) > 0:
            df = pd.read_csv(temp_file_path)
        
        if df.empty:
            return render(request, 'index.html', {"data": []})
        
        final_data = []
        for x in df.itertuples(index=False):
            data = [x[0]]
            for vals in x[1:]:
                data.append(vals if vals else "Untraced")
            final_data.append(data)
        
        return render(request, 'index.html', {"data": final_data})
    except Exception as e:
        custom_logger.log(f'Error in default_view: {str(e)}', logging.ERROR)
        return render(request, 'index.html', {"data": []})

@csrf_exempt
def download(request):
    try:
        file_path = "automation_project/gen_data/to_export.csv"
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            response = FileResponse(open(file_path, "rb"))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            return JsonResponse({"error": "No file available for download"}, status=404)
    except Exception as e:
        custom_logger.log(f'Error in download: {str(e)}', logging.ERROR)
        return JsonResponse({"error": str(e)}, status=500)

import json
@csrf_exempt
def process_data(request):
    try:
        if request.method == "POST":
            selected_rows = request.POST.get('selected_rows')
            headers = ["Company name", "Company number", "Company location", "Company Email"]

            if selected_rows:
                try:
                    data = json.loads(selected_rows)  # Use json.loads for safer data handling
                    df = pd.DataFrame(data, columns=headers)
                    df.to_csv("automation_project/gen_data/to_export.csv", index=False)
                    return JsonResponse({"message": "Data added to CSV successfully"}, status=200)
                except json.JSONDecodeError as e:
                    # Handle JSON parsing errors
                    custom_logger.log(f'JSON decoding error: {str(e)}', logging.ERROR)
                    return JsonResponse({"error": "Invalid data format"}, status=400)
                except Exception as e:
                    # Handle any other exceptions
                    custom_logger.log(f'Error while processing data: {str(e)}', logging.ERROR)
                    return JsonResponse({"error": str(e)}, status=500)
            else:
                # Handle the case where no data is provided
                if os.path.exists("automation_project/gen_data/to_export.csv"):
                    os.remove("automation_project/gen_data/to_export.csv")
                if os.path.exists("automation_project/gen_data/temp.csv"):
                    os.remove("automation_project/gen_data/temp.csv")
                
                return JsonResponse({"message": "No data to process, files removed"}, status=200)
        else:
            return JsonResponse({"error": "Invalid request method"}, status=405)
    except Exception as e:
        custom_logger.log(f'Unexpected error in process_data: {str(e)}', logging.ERROR)
        return JsonResponse({"error": str(e)}, status=500)

def display_csv(request):
    try:
        csv_file_path = 'automation_project/gen_data/temp.csv'
        if not os.path.exists(csv_file_path):
            pd.DataFrame().to_csv(csv_file_path, index=False)

        if os.path.getsize(csv_file_path) > 0:
            with open(csv_file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
            return render(request, 'index.html', {'data': data})
        else:
            return render(request, 'index.html', {"data": []})
    except Exception as e:
        custom_logger.log(f'Error in display_csv: {str(e)}', logging.ERROR)
        return render(request, 'index.html', {"data": []})
