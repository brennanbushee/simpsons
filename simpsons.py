#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import openpyxl
from dataclasses import make_dataclass


# In[3]:


Episode = make_dataclass("Episode", [("rating", float), ("name", str), ("number", int), ("season", int)])


# In[4]:


#https://www.imdb.com/title/tt0096697/episodes?season=33
show_id = 'tt0096697'
number_of_seasons = 33
episode_list = []
for i in range(1, number_of_seasons + 1):
    url = f'https://www.imdb.com/title/{show_id}/episodes?season={i}'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    
    episode_tag = soup.find('div', class_='list detail eplist')
    episodes = episode_tag.find_all('div', class_='list_item odd')
    even_episodes = episode_tag.find_all('div', class_='list_item even')
    episodes.extend(even_episodes)
    for ep in episodes:
        meta_content = ep.find('meta')
        episode_number = meta_content.attrs['content']
        rating = float(ep.find('span', class_='ipl-rating-star__rating').get_text())
        title = ep.find('strong').find('a').attrs['title']
        episode_list.append(Episode(season=i,name=title, number=episode_number, rating=rating))
    
    


# In[5]:


episode_list


# In[77]:


episodes[0]


# In[6]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[7]:


episode_df = pd.DataFrame(episode_list)


# In[23]:


episode_df.head(5)


# In[115]:


#Five best and five worst episodes of all time
episode_df.sort_values('rating')


# In[22]:


#Last episode that was rated as highly as "A Serious Flanders" in season 33.
episode_df.sort_values(['season', 'number'], inplace=True)
episode_df[episode_df['season'] == 3 ]


# In[32]:


episode_df[:708][episode_df[:708]['rating'] >= 8.3].sort_values(['season', 'number'])


# In[ ]:


episode_df['number'].dtype


# In[19]:


episode_df['number'] = episode_df['number'].astype(int)


# In[24]:


ratings_by_season = episode_df.groupby('season').mean('rating')
plt.plot(ratings_by_season)


# In[129]:


plt.show()

