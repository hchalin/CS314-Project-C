# initialize variables that everyone will use

current_x = 0
current_y = 0
energy = 10000
supplies = 1000
supply_useage = 2
# currently "basic", "upgraded", and "pro"
starting_engine = "basic"
set_wormhole = "no" # no or anything but that
set_position = [0, 0]
# "regular play" or "never dies"
playstyle = "regular play"
max = 127
starting_cash = 10000
sensor_cost = 2

# --- Gameplay mode: "player" (default) or "qe"
MODE = "player"                 # ← default when running main.py
QE_PASS = "spicerack"           # 
def is_qe_mode() -> bool:
    return MODE.lower() == "qe"

def is_player_mode() -> bool:
    return not is_qe_mode()
