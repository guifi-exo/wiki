access via ssh (from debian)

    ssh -o KexAlgorithms=diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-dss admin@10.x.x.x

as bash alias to use as `ssh-mikrotik admin@10.x.x.x`:

    alias ssh-mikrotik='function _ssh-mikrotik() { ssh -o KexAlgorithms=diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-dss $1; }; _ssh-mikrotik'

