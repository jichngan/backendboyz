'''
This code takes in image file from static/images/new_plot.png directory and outputs a dictionary with width and height of image
This is so that the web app can resize the picture accordingly 
@param_in: Graph plotted 
@return: Dictionary with height and width as keys
'''


from PIL import Image
def image_info():
  output = {}
  image_file = "static/images/new_plot.png"
  im =Image.open(image_file)
  output = {
    "Height": im.size[0],
    "Width": im.size[1]
  }
return output
