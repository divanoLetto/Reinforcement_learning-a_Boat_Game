from settings import GRIDWIDTH, GRIDHEIGHT, TILESIZE

num_actions = 6 #4
max_episode_timesteps = 30
with_property_embedding = True

scale_global_view = [int(GRIDWIDTH / TILESIZE), int(GRIDHEIGHT / TILESIZE)]
num_local_views = 2
scales_local_views = [3, 5]
num_channels_map = 1
nums_values_channel = [6]  # massimo valore che posso trovare nelle mappe

num_property_views = 2
scales_property_views = [3, 3]  # due array di tre elementi
nums_values_property = [18, 18]  # massimi valori presenti nelle proprietà

print_map_during_steps = False
print_info_during_steps = False
