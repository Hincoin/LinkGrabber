import urllib2;
import urllib;
import re;
import os;
from urlparse import urlparse
from urlparse import urljoin
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
crawl_parse = urlparse(crawl_link);
protocol = protocol_regex.search(crawl_link).group(0); # get http or https
i = 1;
for file_n in download_links:

    file_name = urllib2.unquote(file_n);
    file_name_parse = urlparse(file_name);
    #destination file
    save_file_name = dir_to_store + file_name_parse[2].split("/")[len(file_name_parse[2].split("/"))-1];
    
    print("downloading file " + str(i) + "/" + str(len(download_links)));

    req_str = file_name;
    #check if it an external link
    
    if(not (file_name_parse[0] == 'http' or file_name_parse[0] == 'https')):

       
      #check if absoulute or relative filepath
      if(file_name_parse[2][0] == '/'): #asbolute path
          req_str = urljoin(crawl_parse[0] + "://" + crawl_parse[1] ,''.join(file_name_parse[2].split("/")[:-1]) + "/" +  urllib.quote(file_name_parse[2].split("/")[len(file_name_parse[2].split("/"))-1]));
          
      else: #relative
        req_str = urljoin(crawl_parse[0] + "://" + crawl_parse[1] + crawl_parse[2], ''.join(file_name_parse[2].split("/")[:-1]) + "/" + urllib.quote(file_name_parse[2].split("/")[len(file_name_parse[2].split("/"))-1]));
    Request = urllib2.Request(req_str,headers={'User-Agent' : 'Mozilla/5.0'});
    return_val = urllib2.urlopen(Request);
    with open(save_file_name,'wb') as local_file:
        local_file.write(return_val.read());
      
print("Finished!");



