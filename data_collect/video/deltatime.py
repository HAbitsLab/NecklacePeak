from datetime import datetime, timedelta, date



def parse_timestamp_tz_naive(string):
    STARTTIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    dt = datetime.strptime(string, STARTTIME_FORMAT)

    return dt
def main():
	start = parse_timestamp_tz_naive('2019-01-04 17:45:38')
	end = parse_timestamp_tz_naive('2019-01-04 20:31:28')

	print(end-start)



if __name__ == '__main__':
	main()