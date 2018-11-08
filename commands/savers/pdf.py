import os
import pdfkit

name = "pdf"

def method(args, article):
    item_id = article["item_id"]
    url = article["given_url"]
    save_file = os.path.join(args.output_dir, item_id + ".pdf")
    if not os.path.isfile(save_file):
        print("Saving article %s at %s" % (item_id, save_file))
        try:
            options = {
                'quiet': ''
            }
            pdfkit.from_url(url, save_file, options)
        except Exception as e:
            print("  * error saving article %s: %s" % (item_id, str(e)))
            pass
    else:
        print("Skipping article %s because it does already exist at %s" % (item_id, save_file))



