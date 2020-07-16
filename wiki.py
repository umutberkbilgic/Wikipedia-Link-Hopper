import requests
from requests.exceptions import HTTPError
import sys

link_goto = 1 # the order of the link that will be followed in the main body of the article
times = 20 # set how deep the link chain goes

# returns a two-tuple of the  given wiki page title and the first outgoing link in the description <p>
def get_title_and_second_href(url):
  response = requests.get(url)
  src = response.text

  title_end = src.find("</title>") - 12
  title = src[102 : title_end]

  target_url = "http://en.wikipedia.org" + ((((src.split('<div class="mw-parser-output">')[1]).split('<p>')[1]).split('<a href="')[link_goto]).split(' ')[0])[:-1]

  return (title, target_url)

# housekeeping
try:
  response = requests.get("http://en.wikipedia.org/wiki/Special:Random")
except HTTPError:
  print("Couldn't reach page.")
except:
  print("Unexpected error:", sys.exc_info()[0])
  print("Terminating ...")
else:
  status = "OK" if (response.status_code == 200) else str(response.status_code)
  # print("STATUS: " + str(status))

  if status != "OK":
    print("Server returned bad response.")
    print("Terminating ...")
    exit(0)

  else:
    # real deal
    # we need the initial calls to fucntions used in the main function above because
    #   special:random redirects and we need the url of the initial page.
    src = response.text

    title_end = src.find("</title>") - 12
    title = src[102 : title_end]

    title_url_offset = src.find('wgPageName":"') + 13
    title_url = src[title_url_offset : title_url_offset + len(title)]

    target_url = "http://en.wikipedia.org" + ((((src.split('<div class="mw-parser-output">')[1]).split('<p>')[1]).split('<a href="')[link_goto]).split(' ')[0])[:-1]

    print('------------------------------------\n')
    print(title)

    # print the title of the current page and change the target to the first href
    for i in range(0, times):
      results = get_title_and_second_href(target_url)
      print(results[0])
      target_url = results[1]


    
    
