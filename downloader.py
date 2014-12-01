import urllib2;
import urllib;
import re;
import os;
import threading;
import signal;
import sys;
import logging;
import multiprocessing;
from urlparse import urlparse
from urlparse import urljoin
from multiprocessing import Pool;

thread_array = [];

def signal_handler(signal,frame):
    global thread_array;
    for thread in thread_array:
        thread.__Thread__stop();
    sys.exit(0);

def download_iter(map_args):
    #download(map_args[0],map_args[1],map_args[2],map_args[3]);
    download(*map_args);
def download(crawl_link,dir_to_store,download_links,beginning,end):
    crawl_parse = urlparse(crawl_link);
    for iterator in range(beginning,end):
        file_n = download_links[iterator];
        file_name = urllib2.unquote(file_n);
        file_name_parse = urlparse(file_name);

        split_slash = file_name_parse[2].split("/");
        save_file_name = dir_to_store + split_slash[-1];
    
        logging.warning("Downloading file " + str(iterator + 1) + "/" + str(len(download_links)));

        req_str = file_name;
        #check if it an external link
    
        if(not (file_name_parse[0] == 'http' or file_name_parse[0] == 'https')):

          
          final_length = -1 *len(split_slash[-1]);
          
          #check if absoulute or relative filepath
          if(file_name_parse[2][0] == '/'): #asbolute path
              req_str = urljoin(crawl_parse[0] + "://" + crawl_parse[1] ,file_name_parse[2][:final_length] +  urllib.quote(split_slash[-1]));
          
          else: #relative
            req_str = urljoin(crawl_parse[0] + "://" + crawl_parse[1] + crawl_parse[2], file_name_parse[2][:final_length] +  urllib.quote(split_slash[-1]));

        logging.warning('URL: ' + req_str);
        Request = urllib2.Request(req_str,headers={'User-Agent' : 'Mozilla/5.0'});
        return_val = urllib2.urlopen(Request);
        with open(save_file_name,'wb') as local_file:
            local_file.write(return_val.read());
            

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
          
          potential_downloads.extend(valid_links);

        return potential_downloads;



def main():
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

    max_threads = multiprocessing.cpu_count(); 

    work_per_thread = 2; # 2 downloads per thread (maybe this is too little?)


    thread_pool = Pool(processes=max_threads);

    downloads_sent = 0;
    if((len(download_links) % work_per_thread) == 0): #divisible by work per thread
            
            for i in range(len(download_links)):
                    thread_array.append(thread_pool.apply_async(download,[crawl_link,dir_to_store,download_links,downloads_sent,downloads_sent+work_per_thread]));
                    downloads_sent += work_per_thread;
    else:

            remainder = len(download_links) % work_per_thread;
            for i in range(len(download_links)-remainder):
                    thread_array.append(thread_pool.apply_async(download,[crawl_link,dir_to_store,download_links,downloads_sent,downloads_sent+work_per_thread]));
                    downloads_sent += work_per_thread;
            thread_array.append(thread_pool.apply_async(download_iter,[crawl_link,download_links,downloads_sent,downloads_sent + (work_per_thread - remainder)]));


    thread_pool.close();
    thread_pool.join();



   
    print("Finished!");
if __name__ == '__main__':
    main();
    



