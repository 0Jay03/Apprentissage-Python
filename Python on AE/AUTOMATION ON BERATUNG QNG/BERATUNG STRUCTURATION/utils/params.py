
# Constants
IMAGE_EXTENSIONS = [
    'jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic', 'heif', 'raw', 'psd', 'ai', 'eps',
    'indd', 'cdr', 'dds', 'exr', 'hdr', 'jp2', 'j2k', 'pbm', 'pgm', 'ppm', 'xbm', 'xpm', 'cr2', 'nef', 'orf', 'sr2',
    'arw', 'dng', 'raf', 'rw2', 'pef', 'srf', 'mrw', 'dcr', 'kdc', 'erf', '3fr', 'mef', 'mos', 'nrw', 'ptx', 'r3d',
    'rwl', 'srw', 'x3f', 'icns', 'tga', 'pcx', 'pict', 'pct', 'wmf', 'emf', 'ani', 'cur', 'djvu', 'djv', 'ps', 'svgz',
    'apng', 'avif', 'jxl', 'qoi', 'bpg', 'flif', 'jxr', 'wdp', 'jpf', 'jpx', 'jpm', 'jxs', 'jbig2', 'jng', 'mng', 'spi',
    'xcf', 'ora', 'kra', 'clip', 'cpt', 'pdn', 'sai', 'xar', 'zif', 'psb', 'pns', 'jps', 'mpo', 'thm', 'dib', 'hdp',
    'wmp', 'jfif', 'jpe', 'jif', 'jfi', 'jpc', 'j2c', 'mj2'
]


# API endpoint
url = "https://api.beratung-qng.com/api/materials"

# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlIjoiVVNSLUhJWFRYNSIsImlhdCI6MTczOTQ0MzE0MywiZXhwIjoxNzcwOTc5MTQzfQ.DgYc3XIZbM2bjC8VPK2C4ZOUwUI-G28arDfK7rTYRw8'  # Replace with your actual authorization token
}


IMAGE_EXTENSIONS_PDF = [
    'pdf'
]
