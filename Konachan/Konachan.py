"""

requirements for plugin


* a plugin is a folder with plugin name, must not contain space in name

* folder must contain few things

  -a python script file same name as folder name with .py extention
  -an icon.png image in same folder as icon of that plugin

  -an info.config file
    +contains key pair value
      ~ name = full name eg with those have space in their name
      ~ website = valid url
      ~ version = v 0.0.1
      ~ isSyncable = 1           #if it can sync tags look at operation no. 2, 1 for yes, 0 for no, if 0 operation2 can be removed
      ~ canSearchTags = 1          # if it can search tags for sub string for auto complete, if 0, operation 3 can be skipped
      ~ description = any text

  -an seprate plugin setting info file, not settings itself but possible values of settings
    +contais key pair value example
      ~ format be like
      ~ setting name = setting type (can be 4 type  "range" "selector" "toggle" "input" range- selecting a numbers from range, selector type multiple value selection,, toggle on off, input-user can type any string and save it)
      ~ EG values
      ~ setting name = range, minvalue, maxvalue, selected value    #min max both included
      ~ setting name = selector, option_1, option_2, option_3, selected_option       #selected option must be in options else 1st option will be selected automatically
      ~ setting name = toggle, stringtowritebeforetoggle, 0 or 1               	#1 for on 0 for off
      ~ setting name = input, promot text, value        #if no value provided input value will be empty string
      ~ Password = password, prompttext value

================================================================================

note : return means print statement, so application read it from buffer

operations of plugin

1. should return list of images when called with "search" parameter eg: python Yande.py tag pageNum (also default argument, if no argumrnt provided should return home page results or can be empty)
2. sync args structure "python Yande.re sync" , should create a file name "tags.txt" in same folder which contains all the tags avaliable/ or possible search tags,
  - can be vary form hundred to million (but not too much as it impact search time later on, also)
    ~ each line in file contains "tagname, tagid, count, type"    #tagname should be all small, can have spaces, tagid must not be same for any 2, type can be any string, if all tags are of same type assign a character in type
  - Also crate one more file for tags info
    ~each line contains info about one tag type
      * comma seaprated line with 3 value
      * type{as same as in text file}, #edc3aa, TypeName   #color code for each type for showing them sepreately later on, TypeName can be Charecter whereas type can be "C"
3. fetchTags option- args eg "python Yande.re tags substring_for_search" returns upto 15 tags max tags for autofill

================================================================================


####look for script file for more info####


================================================================================


requirements for list of images

* each image data will be in "n" lines, with key value pair, seprated by =, not necessarily provide all fields but
some are compulsory *all field value are string *keys must be same as given

*All possible Fields
-ID * (!important , whenever program reads key ID it loads new image)
-name *
-type * (default jpeg,if empty)
-thumbnailLink * (valid url)
-sampleLink * (valid url)
-originalLink * (valid url)
-tags * (comma seprated string)
-safety * (Values={s,q,e} -> S-safe, Q-Questionable, E-Explicit)
-creatorID
-author
-source      #orignal source of image
-otherInfo (any key pair values)

* -> Compulsory Feilds

================================================================================
method to export - use print statement
look for code for specifics

================================================================================

"""

from requests import get
import json
import sys


def sync_tags():
    # creates tags.txt file and fill all the tags in it

    fd = open("tags.txt", "w")
    fd.flush()  # if something exist in file remove everything
    tags = json.loads(get("https://konachan.com/tag.json?limit=0").text)  # getting json file with all tags

    for tag in tags:  # for each tag
        if tag["count"] > 0:  # if tag have some images
            # write entry in file
            fd.write(tag["name"] + "," + str(tag["id"]) + "," + str(tag["count"]) + "," + str(tag["type"]) + "\n")
    fd.close()


def create_tag_info():
    # Generates tag info file which contains name and color for each tag type

    fd = open("tagsInfo.txt", "w")
    fd.flush()

    # writing entry for each type , here types are 0 - 5
    fd.write("1, Artist, yellow\n")
    fd.write("3, Character, green\n")
    fd.write("4, Circle, cyan\n")
    fd.write("2, Copyright, purple\n")
    fd.write("5, Faults, red\n")
    fd.write("0, General, pink\n")

    fd.close()


def get_tags(search_query):
    # return at max 15 tags that matches with search query can be first 15 or tags with most count, its up to function

    max_count = 15

    page = json.loads(get(f"https://konachan.com/tag.json?name={search_query}&limit={max_count}&order=count").text)
    for tag in page:
        if tag["count"] > 0:
            print(_get_tag(tag))


def _get_tag(tag):
    name = tag["name"]
    count = tag["count"]
    typ = tag["type"]
    color = ""

    if typ == 0:
        color = "pink"
    elif typ == 1:
        color = "yellow"
    elif typ == 2:
        color = "purple"
    elif typ == 3:
        color = "green"
    elif typ == 4:
        color = "cyan"
    elif typ == 5:
        color = "red"

    return name + "," + str(count) + "," + color


def get_images(search_tag, page_num):
    """
    Return the list of Images info by printing
    """

    # reading limit form file
    fd = open("settings.cfg", "r")
    line = fd.readline()
    limit = int(line.split(",").pop().strip())

    json_page = json.loads(get(f"https://konachan.com/post.json?limit={limit}&page={page_num}&tags={search_tag}").text)

    # for each image in json
    for image in json_page:
        # ID
        print("ID = ", image["id"])

        # Name
        print("name = yande.re%", str(image["id"]), ".jpg")

        # thumbnail Link
        print("thumbnailLink = ", image["preview_url"])

        # sample Link
        print("sampleLink = ", image["sample_url"])

        # original image Link
        print("originalLink = ", image["jpeg_url"])

        # tags
        print("tags = ", image["tags"].replace(" ", ",").replace("_", " "))

        # is safe image
        print("safe = ", image["rating"])

        # creator id
        print("creatorID = ", image["creator_id"])

        # author
        print("author = ", image["author"])

        # source
        print("source = ", image["source"])


def main():
    """
    search_tag = ""
    page_num = 1
    search_query = "veg"
    req = "sync"
    """
    
    req = sys.argv[1]

    if req == "search":
        search_tag = sys.argv[2]
        page_num = sys.argv[3]
        get_images(search_tag, page_num)

    elif req == "tags":
        search_query = sys.argv[2]
        get_tags(search_query)

    elif req == "sync":
        sync_tags()
        create_tag_info()


if __name__ == '__main__':
    main()
