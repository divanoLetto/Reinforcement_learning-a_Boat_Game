from deepcrawl.environment.game import Game
from BoatGame import BoatGame


class BoatGameEnvironment(Game):

    def __init__(self, state, num_actions, _max_episode_timesteps, game_name="BoatGameEnvironment",
                 input_mode='dense_embedding', no_graphics=False, seed=False, verbose=False, manual_input=False):
        """
        :param state: (State, *required*) the State of the game, one of DenseEmbeddingState or TransformerState;
        :param num_actions: (int > 0, *required*) the number of discrete action NPC has;
        :param _max_episode_timesteps: (int > 0, required) the number of timesteps within an episode of the game;
        :param no_graphics: (bool, default False) if true, you can see the game while npc is training;
        :param seed: (int >= 0, default None) the seed used to reset the game;
        :param input_mode: (string, one of ['dense_embedding', 'transformer'], *required*) the input mode of NPC.
        """

        self.game_name = game_name
        self.game = BoatGame(on_play_mode=False)
        self.inpute_mode = input_mode
        self.no_graphics = no_graphics
        self.seed = seed

        super(BoatGameEnvironment, self).__init__(state, num_actions, _max_episode_timesteps,
                                                    use_double_agent=False, double_agent=None,
                                                    verbose=verbose, manual_input=manual_input)

    # Method that closes the game
    def close(self):
        self.game.close()

    # Method that resets the game to a new episode. It returns a state dict.
    def reset(self):
        map_dim = self.config["map_dimentions"]
        observation = self.game.reset(map_dim)
        return observation

    # Method that make a step in the game. It takes an action and returns (state, done, reward).
    def execute(self, actions):
        actions = self.get_manual_input(actions)
        observation, reward, done = self.game.step(actions)
        return (observation, done, reward)

    def command_to_action(self, command):
        print(command)
        return int(command)