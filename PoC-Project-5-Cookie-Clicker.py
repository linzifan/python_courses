"""
Cookie Clicker Simulator
"""
http://www.codeskulptor.org/#user39_CCxO5JObUb_2.py


import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return " ".join(["\ntotal cookies:", str(self._total_cookies), 
                         "\ncurrent cookies:", str(self._current_cookies), 
                         "\ncurrent time:", str(self._current_time), 
                         "\nCurrent CPS:", str(self._current_cps)])
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        waittime = math.ceil((cookies - self._current_cookies) / self._current_cps)
        if waittime > 0.0:
            return waittime
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._total_cookies += self._current_cps * time
            self._current_cookies += self._current_cps * time
            self._current_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._history.append((self._current_time,
                                  item_name,
                                  cost,
                                  self._total_cookies))
            self._current_cookies -= cost
            self._current_cps += additional_cps
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_info_clone = build_info.clone()
    clickerstate = ClickerState()
    while clickerstate.get_time() < duration:
        choice = strategy(clickerstate.get_cookies(),
                          clickerstate.get_cps(),
                          clickerstate.get_history(),
                          duration - clickerstate.get_time(),
                          build_info_clone)
        if choice == None:
            clickerstate.wait(duration - clickerstate.get_time())
        else:
            if clickerstate.get_time() + clickerstate.time_until(build_info_clone.get_cost(choice)) <= duration:
                clickerstate.wait(clickerstate.time_until(build_info_clone.get_cost(choice)))
                clickerstate.buy_item(choice, build_info_clone.get_cost(choice), build_info_clone.get_cps(choice))
                build_info_clone.update_item(choice)
            else:
                clickerstate.wait(duration - clickerstate.get_time())
    while clickerstate.get_time() == duration:
        choice = strategy(clickerstate.get_cookies(),
                          clickerstate.get_cps(),
                          clickerstate.get_history(),
                          0,
                          build_info_clone)
        if choice == None:
            break
        else:
            if build_info_clone.get_cost(choice) <= clickerstate.get_cookies():
                clickerstate.buy_item(choice, build_info_clone.get_cost(choice), build_info_clone.get_cps(choice))
                build_info_clone.update_item(choice)
            else:
                break

    return clickerstate


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    pricelist = {}
    for item in build_info.build_items():
        pricelist[build_info.get_cost(item)] = item
    if build_info.get_cost(pricelist[min(pricelist)]) <= cookies + cps * time_left:
        return pricelist[min(pricelist)]
    else:
        return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    pricelist = {}
    fund = cookies + cps * time_left
    for item in build_info.build_items():
        if build_info.get_cost(item) <= fund:
            pricelist[build_info.get_cost(item)] = item
    if len(pricelist) > 0:
        return pricelist[max(pricelist)]
    else:
        return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    pricelist = {}
    cpslist = {}
    for item in build_info.build_items():
        pricelist[build_info.get_cost(item)] = item
        cpslist[build_info.get_cps(item) / build_info.get_cost(item)] = item
    if build_info.get_cost(pricelist[min(pricelist)]) <= cookies + cps * time_left:
        # in order to get as many cookies as possible, at the beginning 1.5% and 
        # at the end 30% of simulation time, choose the item with lowest price,
        # other time choose the item with highest cps/cost
        if time_left > SIM_TIME / 100 * 98.5 or time_left < SIM_TIME / 100 * 30:
            return pricelist[min(pricelist)]
        else:
            return cpslist[max(cpslist)]
    else:
        return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

