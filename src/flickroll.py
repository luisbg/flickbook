#!/usr/bin/python
#
#  Copyright Andrew Hunter, Luis de Bethencourt Guimera 2008
#
#    This program is free software; you may redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the Free 
#    Software Foundation; either version 2 of the License, or (at your option) 
#    any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
#    more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import flickrapi
import urllib
import random
import threading
import download

class FlickRoll(threading.Thread):
    def __init__(self):
        self.api_key = '2215f6cfeb48da6ef0e01f80c24ef039'
        self.flickr_api = flickrapi.FlickrAPI(self.api_key)
        self.id = ''
        self.tag = ''
        self.explore = self.flickr_api.interestingness_getList(api_key = self.api_key)
        threading.Thread.__init__(self)

    def search_photo(self):
        tag_number = random.randint(0, len(self.tag_list.photo[0].tags[0].tag) - 1)
        self.tag = self.tag_list.photo[0].tags[0].tag[tag_number]['raw']
        self.explore = self.flickr_api.photos_search(tags = self.tag, \
            sort = 'interestingness-desc', \
            content_type = 'photos')

    def get_first_photo(self):
        def get_first_photo_in_thread():
            self.explore = self.flickr_api.interestingness_getList(api_key = self.api_key)
        threading.Thread(target=get_first_photo_in_thread).start()

    def get_next_photo(self, filename):
        def get_next_photo_in_thread():
            try:
                photo_number = random.randint(0, len(self.explore.photos[0].photo) - 1)
                while self.id == self.explore.photos[0].photo[photo_number]['id']:
                    self.explore = self.search_photo()
                    photo_number = random.randint(0, len(self.explore.photos[0].photo) - 1)

                self.id = self.explore.photos[0].photo[photo_number]['id']
                photos = self.flickr_api.photos_getSizes(photo_id=self.id)

                medium = len(photos.sizes[0].size) - 1
                source = photos.sizes[0].size[medium]['source']
                download.Download(source, filename).run()

                self.tag_list = self.flickr_api.tags_getListPhoto(photo_id=self.id)
                self.search_photo()
            except AttributeError:
                self.get_first_photo()
            except FlickrError:
                self.get_first_photo()
        threading.Thread(target=get_next_photo_in_thread).start()

if __name__ == "__main__":
    flickroll = FlickRoll() 
    flickroll.get_first_photo()
    for element in (range(42)):
        flickroll.get_next_photo('%d.jpg' % element)
        print element
