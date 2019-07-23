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
