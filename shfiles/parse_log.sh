<<<<<<< HEAD
#Get the apache access file and save it in get_req.txt
curl -o get_req.txt  https://raw.githubusercontent.com/raj-nvidia/interviews/master/access.log
#grep for all GET requests
cat get_req.txt | grep GET >all_gets.txt
#get the count and store in a variable
all_get_count=`cat all_gets.txt  | wc -l`
echo Total GET count: $all_get_count
#Get the unique count and save in a file all_uniq_ip.txt
cat get_req.txt | grep GET | awk '{print $1}' | sort | uniq > all_uniq_ip.txt
#save the count in a 
uniq_ip_count=`cat all_uniq_ip.txt | wc -l`
echo Total Uniq IP  count: $uniq_ip_count

#For loop to get the number of GET's a unique IP does and store in a file ip_occur_count.txt
=======
curl -o get_req.txt  https://raw.githubusercontent.com/raj-nvidia/interviews/master/access.log
cat get_req.txt | grep GET >all_gets.txt
all_get_count=`cat all_gets.txt  | wc -l`
echo Total GET count: $all_get_count
cat get_req.txt | grep GET | awk '{print $1}' | sort | uniq > all_uniq_ip.txt
uniq_ip_count=`cat all_uniq_ip.txt | wc -l`
echo Total Uniq IP  count: $uniq_ip_count


>>>>>>> db35996846e395f5b444dbc06590501ab1670e8c
for i in `cat all_uniq_ip.txt`;do ip_count=`cat all_gets.txt | grep $i| wc -l`;echo $i $ip_count;done &>ip_occur_count.txt
