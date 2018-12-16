curl -o get_req.txt  https://raw.githubusercontent.com/raj-nvidia/interviews/master/access.log
cat get_req.txt | grep GET >all_gets.txt
all_get_count=`cat all_gets.txt  | wc -l`
echo Total GET count: $all_get_count
cat get_req.txt | grep GET | awk '{print $1}' | sort | uniq > all_uniq_ip.txt
uniq_ip_count=`cat all_uniq_ip.txt | wc -l`
echo Total Uniq IP  count: $uniq_ip_count


for i in `cat all_uniq_ip.txt`;do ip_count=`cat all_gets.txt | grep $i| wc -l`;echo $i $ip_count;done &>ip_occur_count.txt
