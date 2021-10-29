import os 


#os.chdir("collectedNews/CH/RTS/")
os.system("ls")
for nation in os.listdir("collectedNews/"):
    for source in os.listdir("collectedNews/" + nation):
        for edition in os.listdir("collectedNews/" + nation + "/" + source):
            #print("collectedNews/" + nation + "/" + source + "/" + edition)
            os.system("sed -i 's/news_news_url/news_url/' " + "collectedNews/" + nation + "/" + source + "/" + edition) 
