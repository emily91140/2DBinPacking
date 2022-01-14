from PIL import Image, ImageDraw

def plot_one_bin(data, solution, b_no = 0, show_switch = True, save_switch = False):
    im = Image.new('RGB', (data.WBIN, data.HBIN), (128, 128, 128))
    draw = ImageDraw.Draw(im)
    for job_sol in solution:
        if job_sol[1] == 0:
            print("draw job {}".format(job_sol[0]))
            draw.rectangle((job_sol[3], data.HBIN - job_sol[4], job_sol[5], data.HBIN - job_sol[6]), fill=(0, 192, 192), outline=(255, 255, 255))
    if show_switch:
        im.show()
    if save_switch:
        im.save('./pillow_imagedraw.jpg', quality=95)
