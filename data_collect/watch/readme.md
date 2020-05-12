# Watch Data Processing

## Pull data from server

Requirement: Access to server (very limited number of accounts currently permitted for security)

1. Log in the server, `ssh root@174.138.56.143`, go to the data folder `cd /var/www/html/OPTRAServer/storage/app/csvs/` and `tar -czf myfolder.tar.gz myfolder`.
2. Exit server, go to the local data storage folder, and `scp root@174.138.56.143:/var/www/html/OPTRAServer/storage/app/csvs/[target file] .`.


## Process data

Run script `backend_unzip.py`, `backend_concat.py`, `calc_reliability.py`, `score_reliability.py`, and `split_by_hour.py` one by one.
