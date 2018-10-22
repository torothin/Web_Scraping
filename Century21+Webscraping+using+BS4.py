
# coding: utf-8

# In[38]:

import requests, pandas
from bs4 import BeautifulSoup


r=requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c=r.content
soup=BeautifulSoup(c,"html.parser")
all=soup.find_all("div",{"class":"propertyRow"})
all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
page_nr=soup.find_all("a",{"class":"Page"})[-1].text
    

base_url="http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
l=[]
for page in range(0,int(page_nr)*10,10):
    r=requests.get(base_url+str(page)+".html")
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
    
    for item in all:
        d={}
        d["Price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        d["Address1"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        d["Address2"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        try:
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Area"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["FullBath"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["FullBath"]=None
        try:
            d["HalfBath"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["HalfBath"]=None

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["LotSize"]=feature_name.text
                    
        l.append(d)

df=pandas.DataFrame(l)
df.to_csv("Housing.csv")


# In[ ]:



