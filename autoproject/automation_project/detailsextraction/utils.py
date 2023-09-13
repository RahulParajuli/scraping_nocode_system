


def collect_business_names(scrapped_result:dict={}) -> list:
    """
    Collects all the business names from the business list page.
    """
    business_list = []
    
    try:
        for business in scrapped_result:
            if business('company_name', "") not in business_list and (business('company_name',"") != "null"):
                business_list.append(business.get('company_name', ''))
        return business_list
    except Exception as e:
        print(f"An error occurred while collecting business names: {str(e)}")
        return business_list
    