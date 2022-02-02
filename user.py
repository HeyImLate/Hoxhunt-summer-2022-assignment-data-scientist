import random
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import names

from simulation import SIMULATION_OUTCOMES, SimulationResult


class User(metaclass=ABCMeta):
    """The abstract baseclass for a user, please don't use this directly.

    Create your own subclass(es) with a '_get_simulation_outcome' private method.

    DummyUser is an example of how to do this.
    """

    def __init__(self, type: str = "Base") -> None:
        """Init the object."""
        self.id: str = uuid4().hex
        self.type: str = type
        self.name: str = names.get_first_name()
        self.history: List[Optional[SimulationResult]] = []

    @abstractmethod
    def _get_simulation_outcome() -> str:
        """Implement this method in your own subclass.

        It should always return one of the possible SIMULATION_OUTCOMES
        """
        pass

    def complete_simulation(self, timestamp: datetime) -> None:
        """Complete a simulation and store it in the user's history."""
        outcome = self._get_simulation_outcome()
        assert (
            outcome in SIMULATION_OUTCOMES
        ), "The outcome from your logic is not a valid simulation outcome."

        self.history.append(
            SimulationResult(
                timestamp=datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S"),
                user_id=self.id,
                type=self.type,
                name=self.name,
                outcome=outcome,
            )
        )

    def non_missed_simulations_completed(self) -> int:
        """Return amount of non-missed simulations user has completed"""
        count = 0
        for i in self.history:
            if (i.outcome != 'MISS'):
                count += 1
        return count

    @property
    def simulations_completed(self) -> int:
        """Return amount of simulations user has completed."""
        return len(self.history)

    def __repr__(self) -> str:
        """Update the representation of a class object."""
        return (
            f"User(id={self.id}, name={self.name}, type={self.type} "
            f"simulations_completed={self.simulations_completed})"
        )


# (Task 1): Implement your own user classes.
# All classes should be inherited from the above User class.
# See the DummyUser class below user for an example.
class DummyUser(User):
    """Dummy user class."""

    def __init__(self) -> None:
        """Init the object."""
        super(DummyUser, self).__init__(type="Dummy")

    def _get_simulation_outcome(self) -> str:
        """
        Implement a dummy simulation completion logic.

        Please write your own classes and make the logic smarter! :)
        """
        # In your solution, tweak this logic to mimick your chosen user types instead
        # of picking a random simulation outcome
        return random.choice(SIMULATION_OUTCOMES)


class QuickLearner(User):
    """QuickLearner user class."""

    def __init__(self) -> None:
        """Init the object."""
        super(QuickLearner, self).__init__(type="QuickLearner")

    def _get_simulation_outcome(self) -> str:

        def success_chance() -> float:
            """
            The percentage chance of successfully detecting a phishing email.
            Follows the logistic function (x+1)/(x+10), where in this case x = non-missed simulations.
            This way the initial chance of success is 0.1, after which it keeps rising yet never reaches 1
            """
            return (self.non_missed_simulations_completed() + 1) / (self.non_missed_simulations_completed() + 10)

        # 10% chance to miss the email
        if random.random() < 0.1:
            return SIMULATION_OUTCOMES[1]  # MISS
        elif random.random() < success_chance():
            return SIMULATION_OUTCOMES[0]  # SUCCESS
        else:
            return SIMULATION_OUTCOMES[2]  # FAIL


class SlowLearner(User):
    """SlowLearner user class."""

    def __init__(self) -> None:
        """Init the object."""
        super(SlowLearner, self).__init__(type="SlowLearner")

    def _get_simulation_outcome(self) -> str:

        def success_chance() -> float:
            """
            The percentage chance of successfully detecting a phishing email.
            Follows the logistic function (x+3)/(x+30), where in this case x = non-missed simulations.
            This way the initial chance of success is 0.1, after which it keeps rising yet never reaches 1
            SlowLearners are 3 times slower than QuickLearners.
            """
            return (self.non_missed_simulations_completed() + 3) / (self.non_missed_simulations_completed() + 30)

        # 10% chance to miss the email
        if random.random() < 0.1:
            return SIMULATION_OUTCOMES[1]  # MISS
        elif random.random() < success_chance():
            return SIMULATION_OUTCOMES[0]  # SUCCESS
        else:
            return SIMULATION_OUTCOMES[2]  # FAIL


class BusyQuickLearner(User):
    """
    BusyQuickLearner user class.
    BusyQuickLearners are the same as QuickLearners, but have a 50% chance to miss the email instead of 10%.
    """

    def __init__(self) -> None:
        """Init the object."""
        super(BusyQuickLearner, self).__init__(type="BusyQuickLearner")

    def _get_simulation_outcome(self) -> str:

        def success_chance() -> float:
            return (self.non_missed_simulations_completed() + 1) / (self.non_missed_simulations_completed() + 10)

        # 50% chance to miss the email
        if random.random() < 0.5:
            return SIMULATION_OUTCOMES[1]  # MISS
        elif random.random() < success_chance():
            return SIMULATION_OUTCOMES[0]  # SUCCESS
        else:
            return SIMULATION_OUTCOMES[2]  # FAIL


class BusySlowLearner(User):
    """
    BusySlowLearner user class.
    BusySlowLearners are the same as SlowLearners, but have a 50% chance to miss the email instead of 10%.
    """

    def __init__(self) -> None:
        """Init the object."""
        super(BusySlowLearner, self).__init__(type="BusySlowLearner")

    def _get_simulation_outcome(self) -> str:

        def success_chance() -> float:
            return (self.non_missed_simulations_completed() + 3) / (self.non_missed_simulations_completed() + 30)

        # 50% chance to miss the email
        if random.random() < 0.5:
            return SIMULATION_OUTCOMES[1]  # MISS
        elif random.random() < success_chance():
            return SIMULATION_OUTCOMES[0]  # SUCCESS
        else:
            return SIMULATION_OUTCOMES[2]  # FAIL
