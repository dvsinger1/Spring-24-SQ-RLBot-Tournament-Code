# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    
    def run(self):
        if self.intent is not None:
            self.set_intent(atba())
            return
        distance1 = abs(self.ball.location.y - self.foe_goal.location.y)
        distance2 = abs(self.me.location.y - self.foe_goal.location.y)
        distance3 = abs(self.ball.location.y - self.friend_goal.location.y)
        distance4 = abs(self.me.location.y - self.ball.location.y)
        is_in_front_of_ball = distance1 > distance2
        is_behind_ball = distance1 < distance2
        
        if self.kickoff_flag:
        # set_intent tells the bot what it's trying to do
            self.set_intent(kickoff())
            return
        if self.me.boost > 90:
            self.set_intent(drive(4000))
            self.set_intent(short_shot(self.foe_goal.location))
        else:
            open_boost = [boost for boost in self.boosts if boost.active]
            nearest_boost = None
            nearest_trek = 1000
            self.set_intent(goto(self.me.boost))
            for boost in open_boost:
                trek = (self.me.location - boost.location)
                if nearest_boost is None or nearest_trek < trek:
                    nearest_boost = boost
                    nearest_trek = trek

            if nearest_boost is not None:
                self.set_intent(goto_boost(nearest_boost.location))
        if is_in_front_of_ball:
            self.set_intent(goto(self.foe_goal.location))
            self.set_intent(flip(self.ball.location))
        if is_behind_ball:
            self.set_intent(goto(self.foe_goal.location))
            self.set_intent(short_shot(self.foe_goal.location))   
            return 