# Modular AI Project

Python top-down shooter game made from scratch to demonstrate **modular AI** for enemy behavior, allowing for configurable options and considerations.

<br>

## Summary
- Modular AI Configuration Options
  - **Options**: Define specific enemy actions.
  - **Considerations**: Evaluate game conditions (e.g., ammo, line of sight).
  - **Actions**: Triggered when considerations are met.

- Current AI Configuration:
  - **Shoot on Sight**
    - Conditions: Line of sight + ready to shoot.
    - Action: Enemy shoots at player.
    
  - **Reload on Empty**
    - Conditions: No ammo + not reloading.
    - Action: Enemy reloads.
  
  - **Peek After Duration**
    - Conditions: Delay, player nearby, can shoot.
    - Actions: Enemy peek and shoot.
  
  - **Take Cover if Spotted**
    - Conditions: Player watching for >2 seconds.
    - Action: Enemy takes cover.
  
  - **Take Cover While Reloading**
    - Conditions: Enemy is reloading.
    - Action: Enemy takes cover.
  
  - **Change Cover**
    - Conditions: In cover for too long, arrived at cover.
    - Action: Enemy changes cover.
<br>

## Image Gallery

<!--
### Placeholder Image (This is the image's caption/label)  
![Please end my suffering... (This is the image's alt text)](https://github.com/a-dubs/github-project-template/blob/master/image_gallery/Please_replace_me_I_am_begging_you.jpg)
-->
<br>

## Project Metadata  

**Project Status** : Archived  
**Project Progress** : Functional  
**Project dates** : Feb '23 - Apr '23  

