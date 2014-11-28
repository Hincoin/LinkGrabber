import urllib2;
import urllib;
import re;


regex_str = "\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))";
def extract_links(extensions,html):
    
        base_string = "http[s]?://*.*\.";
        potential_downloads = [];
        for extension in extensions:
          cur_regex = base_string + extension;
          regex = re.compile(cur_regex);
          valid_links = regex.findall(html);
          print("Found " + str(len(valid_links)) + " links!");
          #trying to be fluent in pythonese
          potential_downloads.extend([ x for x in valid_links if x.split(".")[len(x.split("."))-1] in extensions]);

        return potential_downloads;



crawl_link = raw_input("Which website to crawl?\n");
dir_to_store  = raw_input("Directory to store? [Hit enter for default directory]\n");
if(len(dir_to_store) == 0):
    dir_to_store = "./";

extensions = raw_input("enter extensions (comma seperated)");
extension_list = [x for x in extensions.split(",")];

req = urllib2.Request(crawl_link,headers={'User-Agent': 'Mozilla/5.0'});
response = urllib2.urlopen(req);
html = response.read();
download_links = extract_links(extension_list,html);
print("Downloading " + str(len(download_links)) + " files!");
for file_name in download_links:
    print("downloading " + file_name + "  ....");
    print("saving as + " + dir_to_store + file_name.split("/")[len(file_name.split("/"))-1]);
    urllib.urlretrieve(file_name,dir_to_store + file_name.split("/")[len(file_name.split("/"))-1]);

print("Finished!");



