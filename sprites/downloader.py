import base64
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
import pickle

slice_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


def prepare_tensor(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img = np.array(img)
    actions = {
        'walk': {
            'range': [(9, 10), (10, 11), (11, 12)],  # row
            'frames': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)]  # col
        },
        'spellcast': {
            'range': [(1, 2), (2, 3), (3, 4)],
            'frames': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (6, 7)]
        },
        'slash': {
            'range': [(13, 14), (14, 15), (15, 16)],
            'frames': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 6), (5, 6)]
        }
    }
    slices = []
    for action, params in actions.items():
        for row in params['range']:
            sprite = []
            for col in params['frames']:
                sprite.append(slice_transform(img[64 * row[0]:64 * row[1], 64 * col[0]:64 * col[1], :]))
            slices.append(torch.stack(sprite))
    return slices


driver = webdriver.Firefox()
driver.get("http://gaurav.munjal.us/Universal-LPC-Spritesheet-Character-Generator/")
driver.maximize_window()

bodies = ['light', 'dark2']
shirts = ['longsleeve_brown', 'longsleeve_teal']
hairstyles = ['green', 'pink']
pants = ['red', 'teal']

train = 0
test = 0
states = []
ids= []
for id0, body in enumerate(bodies):
    driver.execute_script("return arguments[0].click();", driver.find_element_by_id('body-' + body))
    time.sleep(0.5)
    for id1, shirt in enumerate(shirts):
        driver.execute_script("return arguments[0].click();", driver.find_element_by_id('clothes-' + shirt))
        time.sleep(0.5)
        for id2, pant in enumerate(pants):
            if pant == 'robe_skirt':
                driver.execute_script("return arguments[0].click();", driver.find_element_by_id('legs-' + pant))
            else:
                driver.execute_script("return arguments[0].click();", driver.find_element_by_id('legs-pants_' + pant))
            time.sleep(0.5)
            for id3, hair in enumerate(hairstyles):
                driver.execute_script("return arguments[0].click();", driver.find_element_by_id('hair-plain_' + hair))
                time.sleep(0.5)
                name = body + "_" + shirt + "_" + pant + "_" + hair
                print("Creating character: " + "'" + name)
                canvas = driver.find_element_by_id('spritesheet')#
                canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                                      canvas)
                canvas_png = base64.b64decode(canvas_base64)
                with open(str(name) + ".png", "wb") as f:
                    f.write(canvas_png)
                slices = prepare_tensor(str(name) + ".png")
                print("Dimension is {}".format(slices[0].shape))
                p = torch.rand(1).item() <= 0.1  # Randomly add 10% of the characters created in the test set
                
                id_ = [id0, id1, id2, id3]
                for state in slices:
                    states.append(state.numpy())
                    ids.append(id_)

states = np.asarray(states)
actions = np.zeros_like(states) # dummy
ids = np.asarray(ids)
with open('lpc3.pickle', 'wb') as f:
    pickle.dump([states, actions, ids], f)

# data[0].shape = [batch, seq, dim] state
# data[1].shape = zero and same shape as state. action is dummy
# data[2].shape= [batch, id_] action

                
print("Dataset is Ready.Training Set Size : %d. Test Set Size : %d " % (train, test))

