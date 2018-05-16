export SUMO_HOME=/usr/lib/sumo/
sumo-gui --time-to-teleport 300 --no-internal-links true --ignore-junction-blocker 1 --random true -c sathorn_w.sumo.cfg -a sathon_wide_tls_20160418_edited.add.xml --summary summary.xml
