from PIL import Image
from PIL import ImageDraw
from google.appengine.api import images
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import base64
import os





class Faces:
    DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

    def get_vision_service(self):


        credentials = GoogleCredentials.get_application_default()
        return discovery.build('vision', 'v1', credentials=credentials,
                               discoveryServiceUrl=self.DISCOVERY_URL)

    def detect_face(self, face_file, max_results=4):

        """Uses the Vision API to detect faces in the given file.

        Args:
            face_file: A file-like object containing an image with faces.

        Returns:
            An array of dicts with information about the faces in the picture.
        """
        image_content = face_file
        batch_request = [{
            'image': {
                'content': base64.b64encode(image_content.open().read())
                },
            'features': [{
                'type': 'FACE_DETECTION',
                'maxResults': max_results,
                }]
            }]

        service = self.get_vision_service()
        request = service.images().annotate(body={
            'requests': batch_request,
            })
        response = request.execute()

        return response['responses'][0]['faceAnnotations']


    def highlight_faces(self, blob_info, faces):
        """Draws a polygon around the faces, then saves to output_filename.

        Args:
          image: a file containing the image with the faces.
          faces: a list of faces found in the file. This should be in the format
              returned by the Vision API.
          output_filename: the name of the image file to be created, where the faces
              have polygons drawn around them.
        """
        #from StringIO import StringIO
        #image_string = StringIO(base64.b64decode(image))
        #image_string.seek(0)
        im = Image.open(blob_info.open())
        draw = ImageDraw.Draw(im)

        for face in faces:
            box = [(v['x'], v['y']) for v in face['fdBoundingPoly']['vertices']]
            draw.line(box + [box[0]], width=5, fill='#00ff00')

        del draw
        return im

    def process_pic(self, blob_info):
        from StringIO import StringIO
        faces = self.detect_face(blob_info)
        #blob_info.open().seek(0)
        #print('Found %s face%s' % (len(faces), '' if len(faces) == 1 else 's'))

        text_img = self.highlight_faces(blob_info, faces)
        output = StringIO()
        text_img.save(output, format="png")
        text_layer = output.getvalue()
        output.close()

        return text_layer