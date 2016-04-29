
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import curbside

# For use with Chrome only
#driver = webdriver.Chrome('/Users/wompy/Downloads/chromedriver')
driver = webdriver.Firefox()

def jobs_from_smartrecruiters():
    locations = {}
    state_mapping = {"CA":"California", "MA":"Massachusets"}
    driver.get('https://careers.smartrecruiters.com/Curbside1/')
    rows = driver.find_elements_by_class_name('title-list')
    
    for row in rows:
        locations[row.find_elements_by_tag_name('li')[0].text] = get_total(row)

    for location in locations.keys():
        locations[location.replace(location[-2:], state_mapping[location[-2:]])] = locations.pop(location)       
    return locations 

def get_total(row):
    return int(row.find_elements_by_tag_name('li')[1].text.split(' ')[0])

#https://github.com/hughdbrown/dictdiffer Used in the past for comparing dicts
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

if __name__ == '__main__':

    jobs = jobs_from_smartrecruiters()
    for location, total in jobs.items():
        print "{0}: {1}".format(location, total)
    curb_results = curbside.jobs_from_curbside()
    results = DictDiffer(jobs, curb_results)

    if jobs == curb_results:
        print "Jobs match"
        print jobs
    else:
        print "Added:", results.added()
        print "Changed:", results.changed()
        print "Missing:", results.removed()
