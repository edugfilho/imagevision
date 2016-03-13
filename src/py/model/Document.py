from google.appengine.ext import ndb

class UserDoc(ndb.Model):
    user_id = ndb.StringProperty()
    doc_key = ndb.BlobKeyProperty()
    doc_lang = ndb.StringProperty()
    doc_ocr = ndb.TextProperty()

    def get_by_user(self, user_id):
        return UserDoc.gql("WHERE user_id = :1", user_id)