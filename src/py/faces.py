from PIL import Image
from PIL import ImageDraw
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import base64

class Faces:
    DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

    def get_vision_service(self):


        credentials = GoogleCredentials.get_application_default()
        return discovery.build('vision', 'v1', credentials=credentials,
                               discoveryServiceUrl=self.DISCOVERY_URL)

    def detect(self, face_file, type, max_results=4, num_retries=3):

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
                'type': type,
                'maxResults': max_results,
                }]
            }]

        service = self.get_vision_service()
        request = service.images().annotate(body={
            'requests': batch_request,
            })
        responses = request.execute(num_retries=num_retries)

        return responses['responses'][0]['textAnnotations']
        # {
        #     'TEXT_DETECTION' : responses['responses'][0]['textAnnotations'],
        #     'FACE_DETECTION' : responses['responses'][0]['faceAnnotations'],
        # }[type]

    # def text_response(self, responses, image):
    #     if 'responses' not in responses:
    #         return {}
    #     text_response = {}
    #     for filename, response in zip(images, responses['responses']):
    #         if 'error' in response:
    #             print("API Error for %s: %s" % (
    #                     filename,
    #                     response['error']['message']
    #                     if 'message' in response['error']
    #                     else ''))
    #             continue
    #         if 'textAnnotations' in response:
    #             text_response[filename] = response['textAnnotations']
    #         else:
    #             text_response[filename] = []
    #     return text_response


    def highlight_faces(self, blob_info, faces):
        """Draws a polygon around the faces, then saves to output_filename.

        Args:
          image: a file containing the image with the faces.
          faces: a list of faces found in the file. This should be in the format
              returned by the Vision API.
          output_filename: the name of the image file to be created, where the faces
              have polygons drawn around them.
        """
        im = Image.open(blob_info.open())
        draw = ImageDraw.Draw(im)

        for face in faces:
            box = [(v['x'], v['y']) for v in face['fdBoundingPoly']['vertices']]
            draw.line(box + [box[0]], width=5, fill='#00ff00')

        del draw
        return im

    def process_pic(self, blob_info, type):
        return self.detect(blob_info, type)
        # processed = self.detect(blob_info, type)
        # return {
        #     'TEXT_DETECTION' : processed,
        #     'FACE_DETECTION' : self.return_faces(blob_info, processed),
        # }[type]

    def return_faces(self, blob_info, processed):
        from StringIO import StringIO
        text_img = self.highlight_faces(blob_info, processed)
        output = StringIO()
        text_img.save(output, format="png")
        text_layer = output.getvalue()
        output.close()

        return text_layer