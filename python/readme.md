# IP Generator

Generate Ips for a given subnet and list the pingable ips with RTT



### Prerequisites
```
Install pip3
apt-get install python-pip3
apt-get install fping
pip3 install netaddr

```
 

### How to Run


```
python3 classAIP.py
cat classAip_pingable.txt
cat classAip.txt
```

### Brief Explanation of the program
```
########
#This program takes in a network  defind in the properties.ini
#It will then split it into smaller subnets
#Based on the thread count, it will spawn that many threads and each thread will
#generate all ips as well as find out the pingable ips and the RTT for each pingable ip
#fping linux command  is used for pinging a subnet of ip's in parallel
#The program will generate tmp files along the way
#In the end all the tmp files are concatonated and will be left with files
#classAip.txt --> lists all the IP's
#classAip_pingable.txt --> lists all the pingable ips and the RTT etc
#fping', '-c 1' ,'-a','-g','%s' %subnetstring  --> sends only 1 packet for each ip in the subnet

#To address the question asked, do the following setting
#[default]
#network=0.0.0.0/1
#prefix=8
#subnet_count=128
#threads=128


#Class A ip's are in the range
#0.0.0.0 to 127.255.255.255
#we split it in /8 subnet, 2^7 will give 128 subnets
#each /8 will give out 16 million ip's


#Program was tested with this setting
#[default]
#network=74.125.194.0/22
#prefix=24
#subnet_count=4
#threads=4

#The outfile ares in git classAIP.txt and classAip_pingable.txt
```

