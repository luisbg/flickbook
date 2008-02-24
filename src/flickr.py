import flickrapi
import urllib
import random

class Flickr:
    def __init__(self):
        self.api_key = '045379bc5368502f749af23d95a17c83'
        self.flickr_api = flickrapi.FlickrAPI(self.api_key)
        self.id = ''

    def search_photo(self):
        tag_number = random.randint(0, len(self.tag_list.photo[0].tags[0].tag) - 1)
        tag = self.tag_list.photo[0].tags[0].tag[tag_number]['raw']
        print tag
        self.explore = self.flickr_api.photos_search(tags = tag, \
            sort = 'interestingness-desc', \
            content_type = 'photos')

    def get_first_photo(self):
        self.explore = self.flickr_api.interestingness_getList(api_key = self.api_key)

    def get_next_photo(self, filename):
        photo_number = random.randint(0, len(self.explore.photos[0].photo) - 1)
        while self.id == self.explore.photos[0].photo[photo_number]['id']:
            self.explore = self.search_photo()
            photo_number = random.randint(0, len(self.explore.photos[0].photo) - 1)

        self.id = self.explore.photos[0].photo[photo_number]['id']
        photos = self.flickr_api.photos_getSizes(photo_id=self.id)

        medium = len(photos.sizes[0].size) - 2
        source = photos.sizes[0].size[medium]['source']
        urllib.urlretrieve(source, filename)

        self.tag_list = self.flickr_api.tags_getListPhoto(photo_id=self.id)
        self.search_photo()

if __name__ == "__main__":
    flickr = Flickr() 
    explore = flickr.get_first_photo()
    c = 0
    while c < 20:
        filename = '%d.jpg' % c
        flickr.get_next_photo(filename)
        print c
        c = c + 1
