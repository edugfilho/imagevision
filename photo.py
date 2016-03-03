from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from faces import Faces


# This datastore model keeps track of which users uploaded which photos.
class UserPhoto(ndb.Model):
    user = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()


# [START upload_handler]
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            user_photo = UserPhoto(
                user= "Eduardo",#users.get_current_user().user_id(),
                blob_key=upload.key())
            user_photo.put()

            self.redirect('/photo/view/%s' % upload.key())

        except:
            self.error(500)
# [END upload_handler]


# [START download_handler]
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            base64Img = blobstore.fetch_data(photo_key, 0, blobstore.MAX_BLOB_FETCH_SIZE - 1)
            Faces.process_pic(base64Img)
            self.response.out.write(base64Img)
            #self.send_blob(photo_key)
# [END download_handler]


app = webapp2.WSGIApplication([
    ('/photo/upload', PhotoUploadHandler),
    ('/photo/view/([^/]+)?', ViewPhotoHandler),
], debug=True)
# [END all]