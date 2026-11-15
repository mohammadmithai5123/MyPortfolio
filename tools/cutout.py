import sys, time
from PIL import Image
from rembg import remove, new_session

src, out, model = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else 'u2net_human_seg')
t = time.time()
sess = new_session(model)
im = Image.open(src).convert('RGB')
res = remove(im, session=sess, alpha_matting=True,
             alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15,
             alpha_matting_erode_size=8)
res.save(out)
print('ok', model, res.size, round(time.time() - t, 1), 's')
