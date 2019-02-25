# Generate a mask that includes the pictures that 
# should be considered in any of the analysis
# A. Kopmann, 13.10.18
#

from PIL import Image

imagemask = Image.new('L', (1280,720), 1)
pix = imagemask.load()

# Create a mask that exludes the three label fields

# Top left 324 x 20 (Aragats <date string>)
for x in range(324):
   for y in range(20):
      pix[x,y] = 0

# Bottom left 202 x 20 (Aragats Camera 1)
for x in range(202):
   for y in range(20):
      pix[x,719-y] = 0

# Bottom right 140 x 38 (Date string in two lines)
for x in range(140):
   for y in range(38):
      pix[1279-x,719-y] = 0

imagemask.save("imagemask.png")



