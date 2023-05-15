from PIL import Image

im1 = Image.open('figures/fig3ab_fmrs_tal.png')
im2 = Image.open('figures/fig3cd_spectrum_ratios.png')

h = im1.size[1] + im2.size[1]
w = max(im1.size[0], im2.size[0])
im = Image.new("RGBA", (w, h))

im.paste(im1)
im.paste(im2, (45, im1.size[1]))

im.save('figures/fig3_combined.png')
