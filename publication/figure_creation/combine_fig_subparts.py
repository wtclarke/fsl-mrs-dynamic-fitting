from PIL import Image
from PIL import ImageDraw, ImageFont

im1 = Image.open('../figures/fig2ab_fmrs_tal.png')
im2 = Image.open('../figures/fig2cd_spectrum_ratios.png')

h = im1.size[1] + im2.size[1]
w = max(im1.size[0], im2.size[0])
im = Image.new("RGBA", (w, h))

im.paste(im1)
im.paste(im2, (45, im1.size[1]))

font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
I1 = ImageDraw.Draw(im)
I1.text((60, 0), "A", fill=(0, 0, 0), font=font)
I1.text((1800, 0), "B", fill=(0, 0, 0), font=font)
I1.text((60, 1450), "C", fill=(0, 0, 0), font=font)
I1.text((1800, 1450), "D", fill=(0, 0, 0), font=font)


im.save('../figures/fig2_combined.png')
