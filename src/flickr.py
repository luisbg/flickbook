import flickrapi
import urllib
import random

api_key = '045379bc5368502f749af23d95a17c83'
flickr = flickrapi.FlickrAPI(api_key)

def search_photo(tag_list):
    tag_number = random.randint(0, len(tag_list.photo[0].tags[0].tag) - 1)
    tag = tag_list.photo[0].tags[0].tag[tag_number]['raw']
    print tag
    explore = flickr.photos_search(tags=tag, sort='interestingness-desc')
    return explore
   
explore = flickr.interestingness_getList(api_key = api_key)
id = ''

c = 0
while c < 10:
    photo_number = random.randint(0, len(explore.photos[0].photo) - 1)
    while id == explore.photos[0].photo[photo_number]['id']:
        explore = search_photo(tag_list)
        photo_number = random.randint(0, len(explore.photos[0].photo) - 1)

    id = explore.photos[0].photo[photo_number]['id']
    print id
    photos = flickr.photos_getSizes(photo_id=id)

    bigger = len(photos.sizes[0].size) - 1
    source = photos.sizes[0].size[bigger]['source']
    print source

    file = '%d.jpg' % c
    urllib.urlretrieve(source, file)

    tag_list = flickr.tags_getListPhoto(photo_id=id)
    explore = search_photo(tag_list)

    c = c + 1
