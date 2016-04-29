
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# For use with Chrome only
#driver = webdriver.Chrome('/Users/wompy/Downloads/chromedriver')

def jobs_from_curbside():
    locations = {}
    state_mapping = {"CA":"California", "MA":"Massachusets"}
   
    driver = webdriver.Firefox()
    driver.get('https://shopcurbside.com')
    driver.find_element_by_partial_link_text('Jobs').click()
    table = driver.find_element_by_id('jobsTable')
    tabled = table.find_element_by_tag_name('tbody')
    rows = tabled.find_elements_by_tag_name('tr')
    for row in rows:
        if row.find_elements_by_tag_name('td')[1].text in locations:
            locations[row.find_elements_by_tag_name('td')[1].text] += 1
        else:
            locations[row.find_elements_by_tag_name('td')[1].text] = 1

    for location in locations.keys():
        locations[location.replace(location[-2:], state_mapping[location[-2:]])] = locations.pop(location)       
    return locations 


    
if __name__ == '__main__':
    
    
    jobs = jobs_from_curbside()
    for location, total in jobs.items():
        print "{0}: {1}".format(location, total)
    
