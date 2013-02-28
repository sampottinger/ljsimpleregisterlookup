#! /bin/bash

echo "This is a hack. To be polite, we should probably just buy a Heroku web dyno"
echo "http://www.heroku.com/pricing#0-0"
echo
GO="crontab prevent_heroku_idling_cron"
echo "Executing: $ ${GO}"
$GO

if [ $? -ne 0 ]; then
	echo
	echo "Failure"
fi