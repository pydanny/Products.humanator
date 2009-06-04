from zope.interface import Interface

class IHumanatorView(Interface):
    """Human style question generating and verifying view
        
    Usage: 
        
        - Use the view from a page to generate an image tag and/or an audio
          URL. Use the 'image_tag' and 'audio_url' methods for these.
        
        - Place the image tag and/or audio url in the page
        
        - The image tag will load the captcha for the user, or the user will
          use the audio url to listen to the aural captcha.
        
        - The user will identify the word, and tell the server through a form
          submission.
        
        - Use the user input to verify.
        
    The view will ensure that captcha state is preserved until verification
    has taken place. The image tag and audio url for a given instance of the
    captcha view will give the same word.
        
    """
    
    def question(self):
        """Generate a question"""
    
    
    def verify(self, input):
        """Verify the user-supplied input.
        
        Returns a boolean value indicating if the input matched
        
        """
