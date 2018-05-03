import time
from bs4 import BeautifulSoup
import threading
import requests
import os
import numpy as np

def get_html(url):        #该函数用于调取url地址下网页的结构
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()	
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error:get_html'

def get_content(url):      #该函数用于查询结构中含有特定字节的点
    html = get_html(url)
    
    soup = BeautifulSoup(html,'lxml')
    	
    imglist = soup.find('div',attrs = {'id':'watermark_box'}).findAll('img')
#    cam_loc = soup.find('font', attrs = {'color':'white'})
    img_src = imglist[0].attrs['src']
    return img_src

def mkdir_camloc(base_url,cameras):
    os.chdir(os.getcwd())
    camlocs = []
    for i,camera in enumerate(cameras): 
        url = base_url+str(camera)
        html = get_html(url)
        soup = BeautifulSoup(html,'lxml')
        cam_loc = soup.find('font', attrs = {'color':'white'})
        camloc = cam_loc.contents[0]
        mkdir('{}'.format(camloc))
        camlocs.append(camloc)
    return camlocs

def mkdir(path):    #创建文件夹用于保存图片
#    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    
    if not isExists:
    	print (path+' built')
    	os.makedirs(path)
    	return True
#    else:
#    	print (path+' already exits')
#    	return False


def main(base_url,cameras,camloc,start):   #通过筛选的src抽取图片并写入对应的文件夹
#    dura = time.time()-start
#    print(dura)
#    ct = time.ctime()
#    ctime = ct[11:13] + '.' + ct[14:16] + '.' + ct[17:19]
#    n = np.floor(dura/4)+1
    base_path = os.getcwd()
#    path = 'no%d_crawl'%n
#    mkdir(path)
#    os.chdir(path)
    for n in range(5):
        thiscamera = cameras[n]
        thiscamloc = camloc[n]
        for i,camera in enumerate(thiscamera): 
            url = base_url+str(thiscamera)
#            print('url acquired,begin to download camera signal: ',url)
            
            img_src = get_content(url)
            img = requests.get(img_src)
            ct = time.ctime()
            ctime = ct[11:13] + '.' + ct[14:16] + '.' + ct[17:19]
            
            path = '{}'.format(thiscamloc[i])
            os.chdir(path)
            
            with open('{}'.format(thiscamloc[i]) + '_{}'.format(ctime) + '.jpg', 'ab') as f:
                f.write(img.content)
                f.close()
            os.chdir(base_path)
    print('all the cameras signal have been saved.')


def crawl_timer():    #定时器
    print('crawling start!')
    main(base_url,cameras,camlocs,start);
#    main(base_url,cameras2,camloc2,start);
#    main(base_url,cameras3,camloc3,start);
#    main(base_url,cameras4,camloc4,start);
#    main(base_url,cameras5,camloc5,start);
#    main(base_url,cameras6,camloc6,start);
#    main(base_url,cameras7,camloc7,start);
#    main(base_url,cameras8,camloc8,start);
#    main(base_url,cameras9,camloc9,start);
#    main(base_url,cameras10,camloc10,start);
#    main(base_url,cameras11,camloc11,start);
#    main(base_url,cameras12,camloc12,start);
#    main(base_url,cameras13,camloc13,start);
    global timer 
    timer = threading.Timer(2,crawl_timer)
    timer.start() 
    time.sleep(2)
#    print(time.time())
    timer.cancel()

base_url = 'http://dotsignals.org/multiview2.php?listcam='
#cameras = []
cameras = [846,165,551,366,472] # 2nd Ave 
#cameras = [845,403,398,410,399] # 3rd Ave
#cameras.append([413,412,404]) # Lexington Ave 
#cameras.append([1087,528,407]) # Madison Ave
#cameras.append([415,523,1088,169,409]) # 5th ave 
#cameras6 = [509,511,173,171,414,473] # 6th Ave 
#cameras7 = [475,899,1101,421] # Broadway(times square)
#cameras8 = [510,891,416,1090,504] # 7th Ave
#cameras9 = [503,500,180,181,420] # 8th Ave 
#cameras10 =[229,506,502,508] # 9th Ave
#cameras11 =[531,419,412] # Park Ave
#cameras12 =[545,547,544,543] # 12nd Ave
#cameras13 =[542,406,170,501,178] # 34 st
# Brooklyn Bridge

#camlocs = []
#for n in range(5):
#    for i in range(len(cameras[n])):
camloc = mkdir_camloc(base_url, cameras)
#camlocs.append(camloc)
#camloc3 = mkdir_camloc(base_url, cameras3)
#camloc4 = mkdir_camloc(base_url, cameras4)
#camloc5 = mkdir_camloc(base_url, cameras5)
#camloc6 = mkdir_camloc(base_url, cameras6)
#camloc7 = mkdir_camloc(base_url, cameras7)
#camloc8 = mkdir_camloc(base_url, cameras8)
#camloc9 = mkdir_camloc(base_url, cameras9)
#camloc10 = mkdir_camloc(base_url, cameras10)
#camloc11 = mkdir_camloc(base_url, cameras11)
#camloc12 = mkdir_camloc(base_url, cameras12)
#camloc13 = mkdir_camloc(base_url, cameras13)


if __name__ == '__main__':
    start = time.time()
    crawl_timer()
#    time.sleep(12)
#    timer.cancel()

