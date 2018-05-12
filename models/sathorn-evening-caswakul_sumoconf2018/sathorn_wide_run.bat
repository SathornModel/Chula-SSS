export SUMO_HOME=/usr/local/src/sumo-0.25.0/
sumo-gui --time-to-teleport 300 --lanechange.allow-swap true --no-internal-links true --ignore-junction-blocker 1 --random true -c sathorn_w.sumo.cfg -a sathon_wide_tls_20160418_edited.add.xml --summary summary.xml
