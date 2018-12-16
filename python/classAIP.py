from netaddr import IPNetwork
from config import config
import os
import threading
import os.path
import subprocess


class IPAclass(object):


    def split_array(self,subnets,split_count):
        for i in range(0,len(subnets),split_count):
            yield subnets[i:i + split_count]


    def concat_file(self,source_file,add_file):
        output_file=open(source_file,"a+")
        with open(add_file) as append_file:
            for line in append_file:
                output_file.write(line)
        output_file.close()


    def write_subnet(self,subnets):
        for subnet in subnets:
            output_file=open(str(subnet.ip),"w")
            for ip in IPNetwork(subnet):
                output_file.write(str(ip)+'\n')
            output_file.close()
        self.write_pingable_ips(subnets)



    def generate_ips(self):

        network=config.get('default','network')
        prefix=int(config.get('default','prefix'))
        subnet_count=int(config.get('default','subnet_count'))
        thread_count=int(config.get('default','threads'))
        ipNetwork=IPNetwork(network)
        ip_subnets =list(ipNetwork.subnet(prefix,count=subnet_count))

        subnetlist=None
        if thread_count>subnet_count:
            thread_count=subnet_count

        if(thread_count <subnet_count):
            subnetlist=list(self.split_array(ip_subnets,thread_count))
        if (thread_count ==subnet_count):
            subnetlist=list(self.split_array(ip_subnets,1))


        threads = []

        for subnets in subnetlist:

            thread = threading.Thread(target=self.write_subnet,args=(subnets,))
            thread.start()
            threads.append(thread)




        for thread in threads:
            thread.join()

        path=os.path.exists("classAip.txt")


        if path:
            os.remove("classAip.txt")

        for subnet in ip_subnets:
            ip_path=os.path.exists(str(subnet.ip))
            if(ip_path):
                self.concat_file("classAip.txt",str(subnet.ip))
                os.remove(str(subnet.ip))

        path=os.path.exists("classAip_pingable.txt")

        if path:
            os.remove("classAip_pingable.txt")

        for subnet in ip_subnets:
            ip_path=os.path.exists(str(subnet.ip)+"_pingable")
            if(ip_path):
                self.concat_file("classAip_pingable.txt",str(subnet.ip)+"_pingable")
                os.remove(str(subnet.ip)+"_pingable")

    def write_pingable_ips(self,subnets):

        for subnet in subnets:
            subnetstring=str(subnet)
            p = subprocess.Popen(['fping', '-c 1' ,'-a','-g','%s' %subnetstring], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out, err = p.communicate()
            output_file=open(str(subnet.ip)+"_pingable","w")
            for line in err.decode('utf-8').split('\n'):
                if "100%" not in line:
                    output_file.write(line+'\n')
            output_file.close()




if __name__ == '__main__':
    IPAclass().generate_ips()
