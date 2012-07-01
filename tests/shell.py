from operator import attrgetter

from dogtail import tree
from dogtail import predicate

class Activity:
    def __init__(self, name=None, icon=None):
        self.name = name
        self.icon = icon

shell = tree.root.child(name="sugar-session", roleName="application")

# Complete the intro screen
done_button = shell.child(name="Done", roleName="push button")
done_button.click()

# Switch to the home list view
radio_button = shell.child(name="List view", roleName="radio button")
radio_button.click()

# Make a list of activities by iterating the table
activities = []

table = shell.child(name="", roleName="table")
cells = table.findChildren(predicate.GenericPredicate(roleName="table cell"))
for row in [cells[i:i+5] for i in range(0, len(cells), 5)]:
    activities.append(Activity(name=row[2].text, icon=row[1]))

activities.sort(key=attrgetter("name"))

# Launch and close all the activities
for activity in activities:
    print "Launching %s" % activity.name 

    activity.icon.click()

    # Some activities displays an object chooser, let's close it
    if activity.name in ["Read", "Image Viewer", "Jukebox"]:
        close_button = shell.child(name="Close", roleName="push button")
        close_button.click()

    activity = tree.root.child(name="sugar-activity", roleName="application")

    pred = predicate.GenericPredicate(name="Stop", roleName="push button")
    stop_buttons = activity.findChildren(pred)
    stop_buttons[-1].click()
