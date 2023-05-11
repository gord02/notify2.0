
def process_job_titles(titles):
    swe_intern_job = []
    seen = set()
    for title in titles:
        # job_name = title.contents[0]
        if wordScan(title) and title not in seen:
            swe_intern_job.append(title)
        seen.add(title)
    return swe_intern_job

def wordScan(title):
    if "Intern" in title and "Engineer" in title:
        return True


# testing:  
# test dec to bin on 0,1,2,3,4,5,6,7

# process number into binary and from each catergory, do specifc function call