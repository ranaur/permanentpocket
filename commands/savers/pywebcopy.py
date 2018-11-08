import pywebcopy
import os

name = "pywebcopy"

def method(args, article):
    item_id = article["item_id"]
    url = article["given_url"]
    save_dir = os.path.join(args.output_dir, item_id)
    print("Saving article %s at %s" % (item_id, url))
    pywebcopy.save_webpage(project_url=url, project_folder=save_dir)



