import numpy as np
import math
import cv2
import os
from shutil import copyfile

def create_DOTA(filename, input_dir, output_dir):
    ''' filename: _pkw.samp 
        i.e 'Train/2012-04-26-Muenchen-Tunnel_4K0G0020_pkw.samp'
    '''
    print ('Processing: ', filename)
    label_dir = os.path.join(output_dir, 'labelTxt/')
    image_dir = os.path.join(output_dir, 'images/')
    
    with open (input_dir + filename, 'r') as f:
        x = f.readlines()
        out_txt = filename.replace('_pkw.samp', '.txt')
        f_out = open(label_dir + out_txt, 'w')
        # skip the unnecessary headers
        for item in x[6:]:
            id, typez, center_x, center_y, width, height, angle = [float(itemz) for itemz in item.split(' ')]
            
            x1, x2, x3, x4 = center_x - width, center_x + width, center_x + width, center_x - width,
            y1, y2, y3, y4 = center_y + height, center_y + height, center_y - height, center_y - height
            
            
            vx1, vx2, vx3, vx4 = x1-center_x, x2-center_x, x3-center_x, x4-center_x
            vy1, vy2, vy3, vy4 = y1-center_y, y2-center_y, y3-center_y, y4-center_y
            angle = math.pi * -angle / 180
            
            vertices = np.array([[x1,x2,x3,x4],
                                [y1,y2,y3,y4]])
            
            vector = np.array([[vx1,vx2,vx3,vx4],
                                [vy1,vy2,vy3,vy4]])
            
            rotation_matrix = np.array([
                                        [math.cos(angle), -math.sin(angle)],
                                        [math.sin(angle), math.cos(angle)]
                                        ])
            
            ans = np.matmul(rotation_matrix, vector)        
            center_vertices = np.array([[center_x]*4,
                                        [center_y]*4])
            
            # add back 
            ans = center_vertices + ans
            f_out.write(' '.join([str(float(item)) for item in list(ans.flatten('F'))]))
            f_out.write(' vehicle 0')
            f_out.write('\n')

        f_out.close()
        image_name = filename.replace('_pkw.samp', '.JPG')
        copyfile(input_dir + image_name, image_dir + image_name)
        
    return

if __name__ == '__main__':    
    path_dir = 'Train/'
    output_dir= 'DOTA/'

    files = os.listdir(path_dir)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir + 'labelTxt', exist_ok=True)
    os.makedirs(output_dir + 'images', exist_ok=True)

    samp_files = [item for item in files if '_pkw.samp' in item]
    for item in samp_files:
        create_DOTA(item, input_dir=path_dir, output_dir=output_dir)