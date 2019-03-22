#!/bin/bash
date | tee -a blackbox_results.txt
python3 03_agent_dqn_black_box.py | tee -a blackbox_results.txt
