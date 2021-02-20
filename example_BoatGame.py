from deepcrawl.net_structures.net import *
from deepcrawl.state.dense_embedding_state import DenseEmbeddingState
from deepcrawl.agents.npc import NPC
from BoatGameEnviroment import BoatGameEnvironment
from deepcrawl.trainers.deepcrawl_trainer import DCTrainer
from reinforcements_settings import num_actions, max_episode_timesteps, with_property_embedding, num_local_views
from reinforcements_settings import num_channels_map, num_property_views, scale_global_view, scales_local_views
from reinforcements_settings import scales_property_views, nums_values_channel, nums_values_property

state = DenseEmbeddingState(scale_global_view=scale_global_view, scales_local_views=scales_local_views, num_channels=num_channels_map,
                            scales_property_views=scales_property_views, nums_values_channel=nums_values_channel,
                            nums_values_property=nums_values_property, num_actions=num_actions, with_property_embedding=with_property_embedding)

game = BoatGameEnvironment(state, num_actions=num_actions, _max_episode_timesteps=max_episode_timesteps, manual_input=False)

# Create the net and the baseline
net = Net(embedding_mode='dense_embedding', num_local_views=num_local_views, num_property_views=num_property_views, num_actions=num_actions, with_property_embedding=with_property_embedding)
baseline = Baseline(embedding_mode='dense_embedding', num_local_views=num_local_views, num_property_views=num_property_views, num_actions=num_actions, with_property_embedding=with_property_embedding)

# Create the NPC
npc = NPC(action=dict(type='int', num_values=6), state=state.get_state_dict(), net=net, baseline=net, name='BoatGame NPC')

# Create the trainer
trainer = DCTrainer(game=game, npc=npc, curriculum=None)

# Start the training
trainer.start_training()