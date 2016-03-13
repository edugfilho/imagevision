from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
import logging
from model import Document
import traceback

from src.py.faces import Faces


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            doc_id = upload.md5_hash
            doc = Document.UserDoc.get_by_id(id=doc_id)
            if not doc:
                #blobinfo = blobstore.get(blob_key=upload.key())
                type = 'TEXT_DETECTION'
                requester = users.get_current_user()
                faces = Faces()
                if requester:
                    requester_id = requester.user_id()
                else:
                    requester_id = 'anonymous'

                trans = faces.process_pic(upload, type)#'TRANSLATED DOC FOR USER %s' % requester_id
                doc = Document.UserDoc(
                    id = doc_id,
                    user_id = requester_id,
                    doc_key = upload.key(),
                    doc_lang = trans[0]['locale'].encode('utf8'),
                    doc_ocr = trans[0]['description'].encode('utf8'))
                doc.put()

            self.redirect('/photo/view/%s' % doc_id)

        except:
            stacktrace = traceback.format_exc()
            logging.error("%s", stacktrace)
            self.error(500)


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, doc_id):
        doc = Document.UserDoc.get_by_id(doc_id)
        self.response.headers['Content-Type'] = "text"
        #self.response.out.write(faces.process_pic(blobinfo, 'FACE_DETECTION'))
        self.response.out.write(doc.doc_ocr)


