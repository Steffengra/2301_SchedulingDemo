
from numpy import (
    array,
    newaxis,
    zeros,
)
from keras.models import (
    load_model,
)
from pathlib import (
    Path,
)

from src.config.config import (
    Config,
)
from src.data.scheduling_data import (
    SchedulingData,
)
from src.models.soft_actor_critic import (
    SoftActorCritic,
)
from src.models.td3 import (
    TD3ActorCritic,
)


def main():

    cfg = Config()
    test = SchedulingData(cfg)
    test_ml = SchedulingData(cfg)
    test_ml.import_state(state=test.export_state())
    ml_sched = load_model(Path(cfg.models_path, 'test', 'policy'))

    next_state = test.get_state()
    sim_length = 100_000
    rewards = zeros(sim_length)
    for iter_id in range(sim_length):
        state = next_state.copy()
        print(state)

        action_ml = ml_sched.call(state[newaxis]).numpy().squeeze()
        reward_ml, reward_components_ml = test_ml.step(percentage_allocation_solution=action_ml)

        input1 = float(input('in1: '))
        input2 = float(input('in2: '))
        input3 = float(input('in3: '))
        input4 = float(input('in4: '))
        action = array([
            input1,
            input2,
            input3,
            input4
        ], dtype='float32')
        reward, reward_components = test.step(percentage_allocation_solution=action)

        test_ml.import_state(state=test.export_state())

        print('de', reward)
        print('ml', reward_ml)

        next_state = test.get_state()


if __name__ == '__main__':
    main()
