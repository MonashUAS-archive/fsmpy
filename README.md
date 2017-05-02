# fsmpy
Library for creating Finite State Machines.

## Basic Components
<img width="200" alt="State" src="https://cloud.githubusercontent.com/assets/1896389/25605803/df0a14b2-2f50-11e7-9496-cc69a5a66148.png">

A State represents a single task to be completed.

<img width="200" alt="Watcher" src="https://cloud.githubusercontent.com/assets/1896389/25605836/1df8d9e2-2f51-11e7-81ba-fa79a464ff67.png">

A Watcher represents a single event that causes a transition between states. 

<img width="200" alt="untitled" src="https://cloud.githubusercontent.com/assets/1896389/25605856/3d081cf8-2f51-11e7-9f35-9ddb54ff519e.png">

A Transition groups a single Watcher (`watcher`) and a signle State (`next_state`) together such that if `watcher` triggers, then the State Machine's state is set to `next_state`.

## State Machine Construction

1. Instantiate an FSM.
2. Instantiate all States.
3. Instantiate all Watchers.
4. Instantiate all Transitions.
5. Add Transitions to States.
6. Set the FSM's Reset State.
7. Start the FSM.
