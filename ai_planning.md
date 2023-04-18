Consideration Types:
- Duration
- Distance
- Line of Sight
- Angle Facing Away/Towards  
- Count

Actions:
- Take cover
- Peek
- Shoot
- Move to location
- Face towards player?


AI options implementation plan:
Player facing away -> Peek, Shoot
Duration (hidden) -> Peek
Duration (at same cover) -> Move to new cover | level 1 priority
Ammo Threshold Below 1 -> Take cover, Reload
Duration (line of sight to player) -> shoot
Count()