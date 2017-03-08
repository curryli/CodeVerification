"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

from PIL import Image
import subprocess

#由于都是数字    
#对于识别成字母的 采用该表进行修正    
rep={'O':'0',    
    'I':'1',
    'L':'1',    
    'Z':'2',    
    'S':'5',
    'Q':'0',
    '}':'1',
    'E':'6',
    ']':'1',
    'B':'8'
    };  
    
    
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation
tesseract_exe_name = 'tesseract' # Name of executable to be called at command line

def call_tesseract(input_filename, output_filename):
    args = [tesseract_exe_name, input_filename, output_filename]
    proc = subprocess.Popen(args)
    retcode = proc.wait()

    
def	retrieve_text(scratch_text_name_root):
	inf = file(scratch_text_name_root + '.txt')
	text = inf.read()
	inf.close()
	return text

def  getverify1(name):          
    #打开图片    
    im = Image.open(name)    
    call_tesseract(name, scratch_text_name_root)
    text = retrieve_text(scratch_text_name_root)
    print text  
    #识别对吗    
    text = text.strip()    
    text = text.upper();      
    for r in rep:    
        text = text.replace(r,rep[r])     
    #out.save(text+'.jpg')    
    print text    
    return text
    
if __name__=='__main__':
    getverify1('sd1_new.jpg')
	

