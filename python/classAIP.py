from netaddr import IPNetwork
from config import config
import os
import threading
import os.path
import subprocess


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
#network=10.148.144.0/22
#prefix=26
#subnet_count=16
#threads=8

#The outfile ares in git classAIP.txt and classAip_pingable.txt



############


class IPAclass(object):


    ##This method will split the main subnets into chuncks for each thread based on the properties.ini
    ##


    def split_array(self,subnets,split_count):
        for i in range(0,len(subnets),split_count):
            yield subnets[i:i + split_count]

    #This is utility method to append each tmp file to the source_file


    def concat_file(self,source_file,add_file):
        output_file=open(source_file,"a+")
        with open(add_file) as append_file:
            for line in append_file:
                output_file.write(line)
        output_file.close()


    #This method writes the subnets each ip to a tmp file and names the file with the subnet ip without the prefix

    def write_subnet(self,subnets):
        for subnet in subnets:
            output_file=open(str(subnet.ip),"w")
            for ip in IPNetwork(subnet):
                output_file.write(str(ip)+'\n')
            output_file.close()

    #This function  is called to find the pingable ip's per subnet
        self.write_pingable_ips(subnets)

    #This method will check for each ip is pingable and records the result in a tmp file
    def write_pingable_ips(self,subnets):

        for subnet in subnets:
            subnetstring=str(subnet)
            #Uses python subprocess to call fping
            p = subprocess.Popen(['fping', '-c 1' ,'-a','-g','%s' %subnetstring], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out, err = p.communicate()
            #Shell command details is stored in err as bytes
            output_file=open(str(subnet.ip)+"_pingable","w")
            #read each line and remove the 100% failed lines and write to a tmp file
            for line in err.decode('utf-8').split('\n'):
                if "100%" not in line:
                    output_file.write(line+'\n')
            output_file.close()


    #Main calls this method to generate the ip's for each subnet.



    def generate_ips(self):

        ###Get the details from the properties.ini file

        network=config.get('default','network')
        prefix=int(config.get('default','prefix'))
        subnet_count=int(config.get('default','subnet_count'))
        thread_count=int(config.get('default','threads'))

        ####
        ##netaddr python package is used to deal with handling network, subnet etc
        #Reads the network
        ipNetwork=IPNetwork(network)
        #Splits it into smaller subnet based on the subnet_count
        ip_subnets =list(ipNetwork.subnet(prefix,count=subnet_count))

        #Logic to decide the threadcount
        #Its assumed thread_count is equal or less than the subnet_count
        subnetlist=None
        if thread_count>subnet_count:
            thread_count=subnet_count

        #This will chunk the network into smaller subnet for each thread
        if(thread_count <subnet_count):
            subnetlist=list(self.split_array(ip_subnets,thread_count))
        if (thread_count ==subnet_count):
            subnetlist=list(self.split_array(ip_subnets,1))


        #Holds the thread spawned
        threads = []

        #Spawns each thread

        for subnets in subnetlist:

            thread = threading.Thread(target=self.write_subnet,args=(subnets,))
            thread.start()
            threads.append(thread)



        #Waits for each thread to finish
        for thread in threads:
            thread.join()


        #Delete any old run file
        path=os.path.exists("classAip.txt")
        if path:
            os.remove("classAip.txt")


        #Append all the tmp classAip txt files and delete all the tmp files

        for subnet in ip_subnets:
            ip_path=os.path.exists(str(subnet.ip))
            if(ip_path):
                self.concat_file("classAip.txt",str(subnet.ip))
                os.remove(str(subnet.ip))

        #Delete any old ping run file

        path=os.path.exists("classAip_pingable.txt")

        if path:
            os.remove("classAip_pingable.txt")

        #Append all the tmp classAip pingable  txt files and delete all the tmp files
        for subnet in ip_subnets:
            ip_path=os.path.exists(str(subnet.ip)+"_pingable")
            if(ip_path):
                self.concat_file("classAip_pingable.txt",str(subnet.ip)+"_pingable")
                os.remove(str(subnet.ip)+"_pingable")






if __name__ == '__main__':
    IPAclass().generate_ips()