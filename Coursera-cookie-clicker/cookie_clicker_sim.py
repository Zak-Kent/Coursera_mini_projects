"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
#SIM_TIME = 10000000000.0

SIM_TIME = 100000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_produced = 0.0 
        self._current_cookies = 0.0
        self._current_time = 0.0 
        self._cps = 1.0 
        self._history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        total_cookies = "Total cookies: " + str(self._total_cookies_produced) + ' ' 
        current_cookies = "Current cookies: " + str(self._current_cookies) + ' '
        current_time = "Current time: " + str(self._current_time) + ' '
        cookies_per_sec = "CPS: " + str(self._cps)
        
        return total_cookies + current_cookies + current_time + cookies_per_sec
        
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
        return self._cps
    
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
        history = self._history_list[:]
        
        return history  

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """        
        cookies_needed = cookies - self.get_cookies()        
        
        if cookies_needed < 0:
            return 0.0        
        else: 
            time = cookies_needed / self._cps        
            return math.ceil(float(time))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            cookies_prod = time * self._cps 
            self._total_cookies_produced += cookies_prod
            self._current_cookies += cookies_prod
            self._current_time += time 
          
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost: 
            self._current_cookies -= cost
            self._cps += additional_cps
            
            snapshot = (self.get_time(), item_name, cost, self._total_cookies_produced)
            self._history_list.append(snapshot)
            
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    build_clone = build_info.clone()
    click = ClickerState()
    
    while click.get_time() <= duration:
        item = strategy(click.get_cookies(), click.get_cps(), click.get_history(), 
                 (duration - click.get_time()), build_clone)
        
        if item == None:
            break 
        
        item_cost = build_clone.get_cost(item)
        time_until = click.time_until(item_cost)
        
        if time_until + click.get_time() <= duration: 
            click.wait(time_until)
            click.buy_item(item, item_cost, build_clone.get_cps(item))
            build_clone.update_item(item)
        else: 
            break
            
    click.wait((duration - click.get_time()))
       
    return click 

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
    item_list = build_info.build_items()
    items_costs = map(build_info.get_cost, item_list) 
    
    indv_cost = min(items_costs)
    choice = items_costs.index(indv_cost)
    final_choice = item_list[choice]
    
    
    if time_left >= (indv_cost - cookies / cps):
        return final_choice
    else: 
        return None     

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    total_cookies = (time_left * cps + cookies)
    item_list = build_info.build_items()
    items_costs = map(build_info.get_cost, item_list) 
    
    current_choice = 0
    max_choice = ''
       
    for item in items_costs: 
        if item > current_choice and item <= total_cookies: 
            current_choice = item
            choice = items_costs.index(item)
            max_choice = item_list[choice]  
            
    if time_left >= (current_choice - cookies / cps):
        return max_choice
    else: 
        return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_list = build_info.build_items()
    items_costs = map(build_info.get_cost, item_list) 
    
    indv_cost = min(items_costs)
    choice = items_costs.index(indv_cost)
    final_choice = item_list[choice]
    
    
    if time_left >= (indv_cost - cookies / cps):
        return final_choice
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
    run_strategy("Cursor", SIM_TIME, strategy_expensive)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

