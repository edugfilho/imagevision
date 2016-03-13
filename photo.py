import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from src.py.faces import Faces


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
            blobinfo = blobstore.get(blob_key=photo_key)
            faces = Faces()
            type = 'TEXT_DETECTION'
            self.response.headers['Content-Type'] = {
                'FACE_DETECTION' : "image/png",
                'TEXT_DETECTION' : "text",
            }[type]
            #self.response.out.write(faces.process_pic(blobinfo, 'FACE_DETECTION'))
            self.response.out.write(faces.process_pic(blobinfo, type))

# [END download_handler]


app = webapp2.WSGIApplication([
    ('/photo/upload', PhotoUploadHandler),
    ('/photo/view/([^/]+)?', ViewPhotoHandler),
], debug=True)
# [END all]