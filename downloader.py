import urllib2;
import urllib;
import re;
import os;

protocol_regex = re.compile("http[s]?");


def extract_links(extensions,html):
    
        base_string = ".*\."; # matches the file names
        clean_html = re.compile("(\&lt\;).*?(\&gt\;)"); #cleans HTML tags
        potential_downloads = [];
        for extension in extensions:
          cur_regex = base_string + extension;
          regex = re.compile(cur_regex);
          valid_links = regex.findall(html);

          #clean the links that were found
          for i in range(len(valid_links)):
              valid_links[i] = valid_links[i].strip();
              valid_links[i] = re.sub(clean_html,'',valid_links[i]);
              valid_links[i] = re.sub('<a*.*href=','',valid_links[i]);
              valid_links[i] = valid_links[i].replace('"','');
              valid_links[i] = valid_links[i].replace('<a href=','');
              
          print("Found " + str(len(valid_links)) + " links!");
          
          #trying to be fluent in pythonese
          potential_downloads.extend([ x for x in valid_links if x.split(".")[len(x.split("."))-1] in extensions]);

        return potential_downloads;



crawl_link = raw_input("Which website to crawl?\n");
dir_to_store  = raw_input("Directory to store? [Hit enter for default directory]\n");
if(len(dir_to_store) == 0):
    dir_to_store = os.getcwd() + os.sep;

extensions = raw_input("enter extensions (comma seperated) and without '.', (i.e to match .pdf files just type pdf)\n");
extension_list = [x for x in extensions.split(",")];

req = urllib2.Request(crawl_link,headers={'User-Agent': 'Mozilla/5.0'}); #trolling websites to bypass some 403 Forbidden status codes

response = urllib2.urlopen(req);
html = response.read();
download_links = extract_links(extension_list,html);
print("Downloading " + str(len(download_links)) + " files!");

remove_http = re.sub("http[s]?://",'',crawl_link); # get the base without http

protocol = protocol_regex.search(crawl_link).group(0); # get http or https

for file_name in download_links:

    #destination file
    save_file_name = dir_to_store + file_name.split("/")[len(file_name.split("/"))-1];
    
    print("downloading " + file_name + "  ....");
    print("saving as " + save_file_name);


    #check if it an external link
    if(not file_name.startswith("http")):
        
      #check if absoulute or relative filepath
      if(file_name[0] == '/'): #asbolute path
          urllib.urlretrieve(protocol +"://" + remove_http.split("/")[0] + file_name,save_file_name);
          
      else: #relative
        urllib.urlretrieve(''.join(crawl_link.split("/")[:-1]) + file_name,save_file_name);
        
    else: # external link
      urllib.urlretrieve(file_name,save_file_name);
      
print("Finished!");



