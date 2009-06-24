from zope.interface import Interface

class IHumanatorView(Interface):
    """Human style question generating and verifying view
        
    Usage: 
        
        - Use the view from a page to generate a question.
                
        - The user will answer the question
        
        - Use the user input to verify.
        

        
    """
    
    def question(self):
        """Generate a question"""
    
    
    def verify(self, input):
        """Verify the user-supplied input.
        
        Returns a boolean value indicating if the input matched
        
        """
