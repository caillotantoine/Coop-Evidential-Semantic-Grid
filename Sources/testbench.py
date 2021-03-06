from platform import python_branch
from tqdm import tqdm
import matplotlib.pyplot as plt
from cwrap.merger import mean_merger_fast, DST_merger
from cwrap.decision import cred2pign
from os import path, makedirs 
from metrics import create_diffmap, save_map
from global_var import *
from pipeline import *
from recorder import *
from agents2maps import readFE
from threading import Thread, Lock
from copy import deepcopy
import time
import scipy.ndimage as ndimage

import matplotlib.pyplot as plt


# for dubug only 
import pandas as pd
import os
from pathlib import Path  
OUT_DETAILS = False

class GUI_State:
    mutex: Lock
    quit:bool
    pause:bool
    gnd_map:np.ndarray
    mean_map:np.ndarray
    dst_map:np.ndarray
    evid_raw:np.ndarray
    pov:np.ndarray
    pov_id:int
    history:dict
    

    def __init__(self) -> None:
        self.mutex = Lock()
        self.quit = False
        self.pause = False
        self.gnd_map = None
        self.mean_map = None
        self.dst_map = None
        self.evid_raw = None
        self.history = dict()
        self.pov = None
        self.pov_id = 0
        for decis in DECIS_LUT:
            self.history[decis] = []

    def set_pov(self, image:np.ndarray):
        self.mutex.acquire()
        self.pov = deepcopy(image)
        self.mutex.release()

    def get_pov(self) -> np.ndarray:
        self.mutex.acquire()
        image = self.pov
        self.mutex.release()
        return image


    def update(self, gnd_map, mean_map, dst_map, evid_raw):
        self.mutex.acquire()
        self.gnd_map = deepcopy(gnd_map)
        self.mean_map = deepcopy(mean_map)
        self.dst_map = deepcopy(dst_map)
        self.evid_raw = deepcopy(evid_raw)
        self.mutex.release()
    
    def update_history(self, key, value):
        self.mutex.acquire()
        self.history[key].append(value)
        self.mutex.release()

    def get_history(self):
        self.mutex.acquire()
        history = self.history
        self.mutex.release()
        return history
    
    def quit_gui(self, event):
        print('Stopping')
        self.mutex.acquire()
        self.quit = True
        self.mutex.release()

    def togglePlayPause_gui(self):
        self.mutex.acquire()
        self.pause = not self.pause
        self.mutex.release()

    def is_quit(self):
        self.mutex.acquire()
        quit = self.quit
        self.mutex.release()
        return quit

    def is_pause(self):
        self.mutex.acquire()
        pause = self.pause
        self.mutex.release()
        return pause


def pipeline(state:GUI_State):
    init_out_file() # Initialize the metrics file
    (every_agents, agents2gndtruth) = read_dataset() # Read the dataset
    active_agents = get_active_agents(every_agents) # Get the active agents
    mapcenter = get_mapcenter(every_agents) # Get the map center

    with open(args.json_path) as json_file:
        data = json.load(json_file)

    bbox_pose = data['bbox']['pose']
    bbox_size = data['bbox']['size']
    bbox_class = data['bbox']['class']
    bbox_drop = data['bbox']['drop']
    bbox_noise = (bbox_pose, bbox_size, bbox_class, bbox_drop)

    loopback_evid = None

    for frame in tqdm(range(args.start, args.end)): # for each frame
        # print(f"pipeline frame {frame}")
        while state.is_pause():
            time.sleep(0.1)
            if state.is_quit():
                print('quitted')
                return
        if state.is_quit():
            print('quitted')
            return

        (mask_GND, _, _) = get_gnd_mask(frame, agents2gndtruth, mapcenter=mapcenter) # Get the ground truth mask
        (mask, evid_maps, images) = get_local_maps(frame=frame, agents=active_agents, mapcenter=mapcenter, bbox_noise=bbox_noise) # Get the local maps
        #================== Start debug VY76R5FGY876T574EFU6
        #   Role of debug : print 3D bounding boxes + projected footprints in an image. 
        #                   The image will then be transfered to 

        state.set_pov(images[3])

        #================== End debug VY76R5FGY876T574EFU6
        observed_mask = get_nObserved_mask(frame, mask) # Get the observed mask

        for i, m in enumerate(mask):
            save_map(f'{SAVE_PATH}/RAW_PoV/Agent{i}/', f'{frame:06d}.png', m)

        if CPT_MEAN: # If we want to compute the mean method
            save_map(f'{SAVE_PATH}/GND/', f'{frame:06d}.png', mask_GND, args.save_img) # Save the ground truth map (so we just need to save it once)
            mean_map = mean_merger_fast(mask, gridsize=GRIDSIZE, FE=readFE()) # Compute the mean map
            sem_map_mean = cred2pign(mean_map, method=-1) # Compute the semantic map from the mean map
            save_to_file(frame, 'avg', mask_GND, sem_map_mean, observed_mask) # Save the metrics of the mean method
            if args.gui:
                state.update_history('Avg_Max', (frame, record(mask_GND, sem_map_mean, observed_mask, args.cooplvl, GRIDSIZE, frame)['mIoU'])) # Update the history of the mean method

            # save the maps
            if args.save_img: # If we want to save the maps
                diff = create_diffmap(mask_GND, sem_map_mean) # Compute the difference map
                save_map(f'{SAVE_PATH}/Mean/RAW/', f'{frame:06d}.png', mean_map)
                save_map(f'{SAVE_PATH}/Mean/SEM/', f'{frame:06d}.png', sem_map_mean)
                save_map(f'{SAVE_PATH}/Mean/Dif/', f'{frame:06d}.png', diff)

        evid_maps = list(evid_maps) # Convert the evidence maps to a list
        if args.loopback_evid: 
            evid_buffer = DST_merger(evid_maps=evid_maps, gridsize=GRIDSIZE, CUDA=False, method=ALGOID)
            # insert the loopback as first element
            if type(loopback_evid) != type(None):
                evid_out = DST_merger(evid_maps=[loopback_evid, evid_buffer], gridsize=GRIDSIZE, CUDA=False, method=ALGOID)
            else:
                evid_out = evid_buffer
            # ======================================================= ADD NOISE  jhcvhjebqchbjhqsdcbjhbvcqazxc

            # mass_check = np.sum(evid_buffer, axis=2)
            # save_map(f'{SAVE_PATH}/{ALGO}/RAW/sum_evid/', f'{frame:06d}.png', mass_check, args.save_img)

            evid_blured = np.zeros(evid_buffer.shape, dtype=np.float32)
            for i in range(evid_buffer.shape[2]):
                evid_blured[:,:,i] = ndimage.gaussian_filter(evid_buffer[:,:,i], sigma=5.0)

            save_map(f'{SAVE_PATH}/{ALGO}/RAW/V-P-T_blur/', f'{frame:06d}.png', evid_blured[:,:,[1, 2, 4]], args.save_img)
            evid_normalizer = np.sum(evid_blured, axis=2)

            for i in range(evid_blured.shape[2]):
                evid_blured[:,:,i] = evid_blured[:,:,i] / evid_normalizer

            # evid_normalizer2 = np.sum(evid_blured, axis=2)

            loopback_evid = evid_blured

            # ======================================================= ADD NOISE  jhcvhjebqchbjhqsdcbjhbvcqazxc
        else:
# ====================================================================== BUG: merging results mass sum != 0 jnhqd4fd4v55grd4sv4qbvsrwdf
            # Merge the evidential map for a given algorithm
            evid_out = DST_merger(evid_maps=evid_maps, gridsize=GRIDSIZE, CUDA=False, method=ALGOID)
            # mass_check = np.sum(evid_out, axis=2)
            # save_map(f'{SAVE_PATH}/{ALGO}/RAW/debug/{frame}/', f'{frame:06d}.png', mass_check, args.save_img)

        if OUT_DETAILS:
            DST_LUT = ['??', "V", "P", "VP", "T", "VT", "PT", "VTP"]
            for i in range(evid_out.shape[0]):
                for j in range(evid_out.shape[1]):
                    if evid_out[i,j, 0] > 0:
                        out_info = {'frame': frame, 'x': i, 'y': j, 'mass_sum': evid_out[i,j]}
                        for k in range(evid_out.shape[2]):
                            out_info[f'evid_{DST_LUT[k]}'] = evid_out[i,j,k]
                        df = pd.DataFrame(out_info)
                        filepath = Path(f'{SAVE_PATH}/{ALGO}/RAW/debug/{frame}/info.csv')  
                        filepath.parent.mkdir(parents=True, exist_ok=True)  
                        df.to_csv(filepath, mode='a', index=False, header=not os.path.exists(filepath))

                        out_dst = {}
                        for name in DST_LUT:
                            out_dst[name] = []
                        
                        for emap in evid_maps:
                            for k in range(emap.shape[2]):
                                out_dst[DST_LUT[k]].append(emap[i,j,k])
                        df = pd.DataFrame(out_dst)
                        filepath = Path(f'{SAVE_PATH}/{ALGO}/RAW/debug/{frame}/dst/{i}-{j}.csv')  
                        filepath.parent.mkdir(parents=True, exist_ok=True)  
                        df.to_csv(filepath, index=False)


            # for i in range(evid_out.shape[2]):
            #     evid_out[:,:,i] = np.divide(evid_out[:,:,i], mass_check)
            # mass_check = np.sum(evid_out, axis=2)
            # save_map(f'{SAVE_PATH}/{ALGO}/RAW/sum_evid_norm/', f'{frame:06d}.png', mass_check, args.save_img)

# ====================================================================== BUG: merging results mass sum != 0 jnhqd4fd4v55grd4sv4qbvsrwdf
        # Save the maps      
        save_map(f'{SAVE_PATH}/{ALGO}/RAW/V-P-T/', f'{frame:06d}.png', evid_out[:,:,[1, 2, 4]], args.save_img)
        save_map(f'{SAVE_PATH}/{ALGO}/RAW/VP-VT-PT/', f'{frame:06d}.png', evid_out[:,:,[3, 5, 6]], args.save_img)
        save_map(f'{SAVE_PATH}/{ALGO}/RAW/VPT/', f'{frame:06d}.png', evid_out[:,:,7], args.save_img)
        save_map(f'{SAVE_PATH}/{ALGO}/RAW/O/', f'{frame:06d}.png', evid_out[:,:,0], args.save_img)

        # Test every decision taking algorithm except average max
        for decision_maker in DECIS_LUT:
            if decision_maker == 'Avg_Max':
                continue

            # fix the global evid. map to a semantic map with a given algoritm
            sem_map = cred2pign(evid_out, method=DECIS_LUT[decision_maker])
            save_to_file(frame, f'{ALGO}_{decision_maker}', mask_GND, sem_map, observed_mask)
            if args.gui:
                state.update_history(decision_maker, (frame, record(mask_GND, sem_map, observed_mask, args.cooplvl, GRIDSIZE, frame)['mIoU'])) # Update the history

            if args.save_img:
                diff = create_diffmap(mask_GND, sem_map)
                save_map(f'{SAVE_PATH}/{ALGO}/{decision_maker}/', f'{frame:06d}.png', sem_map)
                save_map(f'{SAVE_PATH}/{ALGO}/{decision_maker}/Dif/', f'{frame:06d}.png', diff)

    state.quit_gui(None)



if __name__ == '__main__':
    state = GUI_State()
    if args.gui:
        # fig = plt.figure()
        fig, axes = plt.subplots(2) # (2, 3)
        plt.ion()
        fig.canvas.mpl_connect('close_event', state.quit_gui)

    if not path.isdir(SAVE_PATH):
        makedirs(SAVE_PATH)
    pipeline_p = Thread(target=pipeline, args=(state,))
    pipeline_p.start()

    while not state.is_quit():
        try:
            hist = state.get_history()
            axes[0].cla()
            for decis in DECIS_LUT:
                (f, curve) = zip(*hist[decis])
                axes[0].plot(f, curve, label=decis)
                axes[0].legend(loc='lower left')
        except Exception as e:
            pass

        try:
            axes[1].cla()
            axes[1].imshow(state.get_pov())
            axes[1].set_title('Point of view from agent 0')
            axes[1].get_xaxis().set_visible(False)
            axes[1].get_yaxis().set_visible(False)
        except Exception as e:
            pass


        plt.draw()
        try:
            plt.pause(0.5)
        except Exception as e:
            pass

    pipeline_p.join()
    plt.close('all')



# # FOR EACH FRAME OF A SELECTION
# for frame in tqdm(range(args.start, args.end)):

#     # Manage the GUI
#     if args.gui:
#         if CPT_MEAN:
#             axes[0, 0].imshow(mask[0])
#             axes[0, 0].set_title('Mean map')
#             axes[1, 1].imshow(mask[1])
#             axes[1, 1].set_title('Sem map mean')
#         else:
#             axes[0, 0].imshow(np.array(mask)[[0, 1, 2]].transpose(1, 2, 0))
#             axes[0, 0].set_title('Mask')
#             if type(loopback_evid) != type(None):
#                 axes[1, 1].imshow(loopback_evid[:,:,[1, 2, 4]])
#                 axes[1, 1].set_title('Loopback')
#             else:
#                 axes[1, 1].imshow(toOccup(sem_map, GRIDSIZE))
#                 axes[1, 1].set_title('Occupancy grid')
#         axes[0, 1].imshow(evid_out[:,:,[1, 2, 4]])
#         axes[0, 1].set_title('V, P, T')
#         axes[0, 2].imshow(evid_out[:,:,[3, 5, 6]])
#         axes[0, 2].set_title('VP, VT, PT')
#         axes[1, 0].imshow(mask_GND)
#         axes[1, 0].set_title('Ground truth')
#         axes[1, 2].imshow(sem_map)
#         axes[1, 2].set_title('sem_map evid')
#         fig.suptitle(f'Frame {frame}')
#         plt.pause(0.01)